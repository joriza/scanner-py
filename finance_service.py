import yfinance as yf
import pandas as pd
import pandas_ta as ta
from datetime import datetime, timedelta
from database import db, Ticker, Price

class FinanceService:
    @staticmethod
    def normalize_symbol(symbol):
        # Normalize for yfinance (e.g., BRK.B -> BRK-B)
        return symbol.replace('.', '-')

    @staticmethod
    def sync_ticker_data(ticker_obj):
        symbol = FinanceService.normalize_symbol(ticker_obj.symbol)
        
        # Determine start date for incremental sync
        last_price = Price.query.filter_by(ticker_id=ticker_obj.id).order_by(Price.date.desc()).first()
        if last_price:
            start_date = (last_price.date + timedelta(days=1)).strftime('%Y-%m-%d')
        else:
            start_date = (datetime.now() - timedelta(days=365*2)).strftime('%Y-%m-%d') # 2 years for context
            
        now = datetime.now().strftime('%Y-%m-%d')
        
        if start_date >= now:
            return 0 # Already up to date
            
        data = yf.download(symbol, start=start_date, end=now, progress=False)
        
        if data.empty:
            return 0
            
        # If columns are MultiIndex (common in new versions of yfinance), flatten them
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        count = 0
        for index, row in data.iterrows():
            # Check if date is already in DB (safety check)
            date_val = index.date()
            existing = Price.query.filter_by(ticker_id=ticker_obj.id, date=date_val).first()
            if not existing:
                try:
                    price = Price(
                        ticker_id = ticker_obj.id,
                        date = date_val,
                        open = float(row['Open'].iloc[0] if isinstance(row['Open'], pd.Series) else row['Open']),
                        high = float(row['High'].iloc[0] if isinstance(row['High'], pd.Series) else row['High']),
                        low = float(row['Low'].iloc[0] if isinstance(row['Low'], pd.Series) else row['Low']),
                        close = float(row['Close'].iloc[0] if isinstance(row['Close'], pd.Series) else row['Close']),
                        volume = int(row['Volume'].iloc[0] if isinstance(row['Volume'], pd.Series) else row['Volume'])
                    )
                    db.session.add(price)
                    count += 1
                except Exception as e:
                    print(f"Error processing row for {symbol} at {date_val}: {e}")
                    continue
        
        ticker_obj.last_sync = datetime.now()
        db.session.commit()
        return count

    @staticmethod
    def get_signals(ticker_obj):
        # Load prices from DB
        prices = Price.query.filter_by(ticker_id=ticker_obj.id).order_by(Price.date.asc()).all()
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
        
        # Indicators
        df['RSI'] = ta.rsi(df['close'], length=14)
        df['RSI_SMA'] = ta.sma(df['RSI'], length=14)
        macd = ta.macd(df['close'])
        df = pd.concat([df, macd], axis=1)
        
        # Signal 1: RSI < 30 in last 365 days
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
            date_rsi_30 = last_date.strftime('%Y-%m-%d')
            
        # Signal 2: RSI > RSI_SMA (Bullish trend of RSI)
        # Requirement: Earliest date fulfilling RSI > RSI_SMA, but AFTER the last date where RSI was < 30
        days_since_rsi_bullish = None
        date_rsi_bullish = None
        
        if date_obj_rsi_30:
            # Look for RSI > SMA specifically after the oversold event
            post_oversold_df = last_year_df[last_year_df.index > date_obj_rsi_30]
            rsi_bullish_after = post_oversold_df[post_oversold_df['RSI'] > post_oversold_df['RSI_SMA']]
            
            if not rsi_bullish_after.empty:
                # Get the EARLIEST (farther in the past) date fulfilling the condition after the RSI < 30
                first_date_after = rsi_bullish_after.index[0]
                days_since_rsi_bullish = (datetime.now().date() - first_date_after).days
                date_rsi_bullish = first_date_after.strftime('%Y-%m-%d')

        # Signal 3: MACD Opportunity: MACD > Signal and MACD <= 0 in last 30 days
        macd_col = 'MACD_12_26_9'
        signal_col = 'MACDs_12_26_9'
        
        thirty_days_ago = datetime.now().date() - timedelta(days=30)
        last_30_df = df[df.index >= thirty_days_ago].copy()
        
        last_30_df['cond'] = (last_30_df[macd_col] > last_30_df[signal_col]) & (last_30_df[macd_col] <= 0)
        
        macd_opps = last_30_df[last_30_df['cond']]
        
        macd_first_date = None
        macd_is_active = False
        
        if not macd_opps.empty:
            macd_first_date = macd_opps.index[0].strftime('%Y-%m-%d')
            macd_is_active = bool(last_30_df['cond'].iloc[-1])

        return {
            'symbol': ticker_obj.symbol,
            'price': float(df['close'].iloc[-1]),
            'price_date': df.index[-1].strftime('%Y-%m-%d'),
            'rsi': float(df['RSI'].iloc[-1]) if not pd.isna(df['RSI'].iloc[-1]) else None,
            'days_since_rsi_30': days_since_rsi_30,
            'date_rsi_30': date_rsi_30,
            'days_since_rsi_bullish': days_since_rsi_bullish,
            'date_rsi_bullish': date_rsi_bullish,
            'macd_first_date': macd_first_date,
            'macd_is_active': macd_is_active,
            'last_sync': ticker_obj.last_sync.strftime('%Y-%m-%d %H:%M') if ticker_obj.last_sync else 'Never'
        }
