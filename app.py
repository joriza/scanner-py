from flask import Flask, render_template, jsonify, request
from flasgger import Swagger
from database import db, init_db, Ticker, Price
from finance_service import FinanceService
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scanner.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuración de Swagger
app.config['SWAGGER'] = {
    'title': 'Scanner Pro API',
    'uiversion': 3
}
swagger = Swagger(app)

init_db(app)

@app.route('/')
def index():
    """Página principal
    ---
    responses:
      200:
        description: Renderiza la página principal
    """
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/api/tickers', methods=['GET', 'POST'])
def handle_tickers():
    """Gestión de tickers
    ---
    get:
      description: Obtiene todos los tickers
      responses:
        200:
          description: Lista de tickers
          content:
            application/json:
              schema:
                type: array
                items:
                  type: object
                  properties:
                    id:
                      type: integer
                    symbol:
                      type: string
                    last_sync:
                      type: string
    post:
      description: Agrega un nuevo ticker
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                symbol:
                  type: string
                  example: TSLA
      responses:
        200:
          description: Ticker agregado exitosamente
        400:
          description: Error en la solicitud
    """
    if request.method == 'POST':
        data = request.json
        symbol = data.get('symbol').upper().strip()
        if not symbol:
            return jsonify({'error': 'Symbol is required'}), 400
        
        existing = Ticker.query.filter_by(symbol=symbol).first()
        if existing:
            return jsonify({'error': 'Ticker already exists'}), 400
            
        ticker = Ticker(symbol=symbol)
        db.session.add(ticker)
        db.session.commit()
        return jsonify({'message': 'Ticker added', 'id': ticker.id})
    
    tickers = Ticker.query.all()
    return jsonify([{
        'id': t.id,
        'symbol': t.symbol,
        'last_sync': t.last_sync.strftime('%Y-%m-%d %H:%M') if t.last_sync else 'Never'
    } for t in tickers])

@app.route('/api/tickers/<int:ticker_id>', methods=['DELETE'])
def delete_ticker(ticker_id):
    ticker = Ticker.query.get_or_404(ticker_id)
    Price.query.filter_by(ticker_id=ticker.id).delete()
    db.session.delete(ticker)
    db.session.commit()
    return jsonify({'message': 'Ticker deleted'})

@app.route('/api/seed', methods=['POST'])
def seed_tickers():
    initial_tickers = ['BRK.B', 'JPM', 'FDX', 'GLW', 'GS']
    count = 0
    for sym in initial_tickers:
        if not Ticker.query.filter_by(symbol=sym).first():
            ticker = Ticker(symbol=sym)
            db.session.add(ticker)
            count += 1
    db.session.commit()
    return jsonify({'message': f'Seeds added: {count}'})

@app.route('/api/refresh', methods=['POST'])
def refresh_data():
    tickers = Ticker.query.all()
    results = []
    for t in tickers:
        count = FinanceService.sync_ticker_data(t)
        results.append({'symbol': t.symbol, 'new_records': count})
    return jsonify(results)

@app.route('/api/scan', methods=['GET'])
def scan_tickers():
    strategy = request.args.get('strategy', 'rsi_macd')
    tickers = Ticker.query.all()
    signals = []
    for t in tickers:
        signal = FinanceService.get_signals(t, strategy=strategy)
        if signal:
            signals.append(signal)
    return jsonify(signals)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
