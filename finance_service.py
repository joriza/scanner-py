import yfinance as yf
import pandas as pd
import pandas_ta as ta
from datetime import datetime, timedelta
from database import db, Ticker, Price
import time
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FinanceService:
    @staticmethod
    def normalize_symbol(symbol):
        # Convert BCBA:TICKER to TICKER.BA
        if symbol.startswith('BCBA:'):
            symbol = symbol.replace('BCBA:', '') + '.BA'
        # Normalize for yfinance (e.g., BRK.B -> BRK-B)
        return symbol.replace('.', '-')

    @staticmethod
    def sync_ticker_data(ticker_obj, max_retries=3, retry_delay=2):
        symbol = FinanceService.normalize_symbol(ticker_obj.symbol)
        logger.info(f"Syncing {symbol}...")
        
        last_price = Price.query.filter_by(ticker_id=ticker_obj.id).order_by(Price.date.desc()).first()
        
        # Intentar descargar datos usando el método más confiable
        data = None
        for attempt in range(max_retries):
            try:
                # Usar period para obtener datos más confiablemente
                # Descargar datos de los últimos 2 años si no hay datos previos
                if last_price:
                    # Calcular días desde la última sincronización
                    days_since_last = (datetime.now().date() - last_price.date).days
                    if days_since_last <= 30:
                        period = "1mo"
                    elif days_since_last <= 90:
                        period = "3mo"
                    elif days_since_last <= 180:
                        period = "6mo"
                    else:
                        period = "2y"
                else:
                    period = "2y"
                
                data = yf.download(symbol, period=period, progress=False, timeout=30)
                if not data.empty:
                    break
                logger.warning(f"  {symbol}: Intento {attempt + 1}/{max_retries} - Datos vacíos con period={period}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
            except Exception as e:
                logger.warning(f"  {symbol}: Intento {attempt + 1}/{max_retries} - Error: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
        
        if data is None or data.empty:
            logger.error(f"  {symbol}: No se pudieron obtener datos después de {max_retries} intentos")
            return 0
            
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        # Optimización: Usar set para verificar duplicados (1 query en lugar de N)
        existing_dates = set(
            p.date for p in Price.query
            .with_entities(Price.date)
            .filter_by(ticker_id=ticker_obj.id)
            .all()
        )
        
        count = 0
        for row in data.itertuples():
            date_val = row.Index.date()
            if date_val not in existing_dates:
                try:
                    price = Price(
                        ticker_id = ticker_obj.id,
                        date = date_val,
                        open = float(row.Open),
                        high = float(row.High),
                        low = float(row.Low),
                        close = float(row.Close),
                        volume = int(row.Volume)
                    )
                    db.session.add(price)
                    count += 1
                except Exception as e:
                    logger.error(f"  {symbol}: Error procesando fecha {date_val}: {str(e)}")
                    continue
        
        ticker_obj.last_sync = datetime.now()
        db.session.commit()
        logger.info(f"  {symbol}: {count} nuevos registros agregados")
        return count

    @staticmethod
    def get_signals(ticker_obj, strategy='rsi_macd'):
        # Optimización: Cargar solo campos necesarios
        prices = Price.query.with_entities(
            Price.date, Price.open, Price.high,
            Price.low, Price.close, Price.volume
        ).filter_by(ticker_id=ticker_obj.id).order_by(Price.date.asc()).all()
        
        if not prices or len(prices) < 30:
            return None
            
        df = pd.DataFrame([{
            'date': p.date,
            'open': p.open,
            'high': p.high,
            'low': p.low,
            'close': p.close,
            'volume': p.volume
        } for p in prices])
        
        df.set_index('date', inplace=True)
        fmt_date = lambda d: d.strftime('%y-%m-%d') if d else None
        
        result = {
            'symbol': ticker_obj.symbol,
            'price': float(df['close'].iloc[-1]),
            'price_date': fmt_date(df.index[-1]),
            'last_sync': ticker_obj.last_sync.strftime('%y-%m-%d %H:%M') if ticker_obj.last_sync else 'Never'
        }

        if strategy == 'rsi_macd':
            df['RSI'] = ta.rsi(df['close'], length=14)
            df['RSI_SMA'] = ta.sma(df['RSI'], length=14)
            macd = ta.macd(df['close'])
            df = pd.concat([df, macd], axis=1)
            
            one_year_ago = datetime.now().date() - timedelta(days=365)
            last_year_df = df[df.index >= one_year_ago].copy()
            rsi_under_30 = last_year_df[last_year_df['RSI'] < 30]
            
            days_since_rsi_30 = None
            date_rsi_30 = None
            date_obj_rsi_30 = None
            if not rsi_under_30.empty:
                last_date = rsi_under_30.index[-1]
                date_obj_rsi_30 = last_date
                days_since_rsi_30 = (datetime.now().date() - last_date).days
                date_rsi_30 = fmt_date(last_date)
                
            days_since_rsi_bullish = None
            date_rsi_bullish = None
            if date_obj_rsi_30:
                post_oversold_df = last_year_df[last_year_df.index > date_obj_rsi_30]
                rsi_bullish_after = post_oversold_df[post_oversold_df['RSI'] > post_oversold_df['RSI_SMA']]
                if not rsi_bullish_after.empty:
                    first_date_after = rsi_bullish_after.index[0]
                    days_since_rsi_bullish = (datetime.now().date() - first_date_after).days
                    date_rsi_bullish = fmt_date(first_date_after)

            macd_col = 'MACD_12_26_9'
            signal_col = 'MACDs_12_26_9'
            thirty_days_ago = datetime.now().date() - timedelta(days=30)
            last_30_df = df[df.index >= thirty_days_ago].copy()
            last_30_df['cond'] = (last_30_df[macd_col] > last_30_df[signal_col]) & (last_30_df[macd_col] <= 0)
            
            macd_status = 'none'
            macd_date = None
            macd_days = None
            if not last_30_df.empty:
                is_active_today = last_30_df['cond'].iloc[-1]
                active_dates = last_30_df[last_30_df['cond']].index
                if is_active_today:
                    streak = last_30_df['cond'].tolist()
                    idx = len(streak) - 1
                    while idx >= 0 and streak[idx]: idx -= 1
                    start_date = last_30_df.index[idx + 1]
                    macd_status = 'active'
                    macd_date = fmt_date(start_date)
                    macd_days = (datetime.now().date() - start_date).days
                elif not active_dates.empty:
                    last_active_date = active_dates[-1]
                    macd_status = 'inactive'
                    macd_date = fmt_date(last_active_date)
                    macd_days = (datetime.now().date() - last_active_date).days

            result.update({
                'rsi': float(df['RSI'].iloc[-1]) if not pd.isna(df['RSI'].iloc[-1]) else None,
                'days_since_rsi_30': days_since_rsi_30,
                'date_rsi_30': date_rsi_30,
                'days_since_rsi_bullish': days_since_rsi_bullish,
                'date_rsi_bullish': date_rsi_bullish,
                'macd_status': macd_status,
                'macd_date': macd_date,
                'macd_days': macd_days
            })

        elif strategy == '3_emas':
            # DAILY
            df['EMA4_D'] = ta.ema(df['close'], length=4)
            df['EMA9_D'] = ta.ema(df['close'], length=9)
            df['EMA18_D'] = ta.ema(df['close'], length=18)
            df['emas_cond_d'] = (df['close'] > df['EMA4_D']) & (df['close'] > df['EMA9_D']) & (df['close'] > df['EMA18_D'])
            
            emas_d_active_today = bool(df['emas_cond_d'].iloc[-1])
            emas_d_date = None
            emas_d_days = None
            if not df[df['emas_cond_d']].empty:
                if emas_d_active_today:
                    streak = df['emas_cond_d'].tolist()
                    idx = len(streak) - 1
                    while idx >= 0 and streak[idx]: idx -= 1
                    d_start = df.index[idx + 1]
                    emas_d_date = fmt_date(d_start)
                    emas_d_days = (datetime.now().date() - d_start).days
                else:
                    d_last = df[df['emas_cond_d']].index[-1]
                    emas_d_date = fmt_date(d_last)
                    emas_d_days = (datetime.now().date() - d_last).days

            # Strategy 2: 3 EMAS (4, 9, 18) - WEEKLY (Resampled from Daily)
            df_w = df[['open', 'high', 'low', 'close', 'volume']].copy()
            df_w.index = pd.to_datetime(df_w.index)
            # Resample to weekly ending on Friday
            df_w = df_w.resample('W-FRI').agg({
                'open': 'first',
                'high': 'max',
                'low': 'min',
                'close': 'last',
                'volume': 'sum'
            })
            
            df_w['EMA4_W'] = ta.ema(df_w['close'], length=4)
            df_w['EMA9_W'] = ta.ema(df_w['close'], length=9)
            df_w['EMA18_W'] = ta.ema(df_w['close'], length=18)
            df_w['emas_cond_w'] = (df_w['close'] > df_w['EMA4_W']) & (df_w['close'] > df_w['EMA9_W']) & (df_w['close'] > df_w['EMA18_W'])
            
            emas_w_active_today = bool(df_w['emas_cond_w'].iloc[-1])
            emas_w_date = None
            emas_w_days = None
            
            today = datetime.now().date()
            
            if not df_w[df_w['emas_cond_w']].empty:
                if emas_w_active_today:
                    streak = df_w['emas_cond_w'].tolist()
                    idx = len(streak) - 1
                    while idx >= 0 and streak[idx]: idx -= 1
                    w_start_dt = df_w.index[idx + 1].date()
                    # Si el viernes de la racha aún no ha llegado, limitamos a hoy para el cálculo de días
                    w_start_capped = min(w_start_dt, today)
                    emas_w_date = fmt_date(w_start_capped)
                    emas_w_days = (today - w_start_capped).days
                else:
                    w_last_dt = df_w[df_w['emas_cond_w']].index[-1].date()
                    w_last_capped = min(w_last_dt, today)
                    emas_w_date = fmt_date(w_last_capped)
                    emas_w_days = (today - w_last_capped).days

            result.update({
                'emas_d_active': emas_d_active_today,
                'emas_d_date': emas_d_date,
                'emas_d_days': emas_d_days,
                'emas_w_active': emas_w_active_today,
                'emas_w_date': emas_w_date,
                'emas_w_days': emas_w_days,
                'ema4_d': float(df['EMA4_D'].iloc[-1]) if not pd.isna(df['EMA4_D'].iloc[-1]) else None,
                'ema9_d': float(df['EMA9_D'].iloc[-1]) if not pd.isna(df['EMA9_D'].iloc[-1]) else None,
                'ema18_d': float(df['EMA18_D'].iloc[-1]) if not pd.isna(df['EMA18_D'].iloc[-1]) else None
            })

        return result
