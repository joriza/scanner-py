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
    def get_signals(ticker_obj, strategy='rsi_macd'):
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
        fmt_date = lambda d: d.strftime('%y-%m-%d') if d else None
        
        result = {
            'symbol': ticker_obj.symbol,
            'price': float(df['close'].iloc[-1]),
            'price_date': fmt_date(df.index[-1]),
            'last_sync': ticker_obj.last_sync.strftime('%y-%m-%d %H:%M') if ticker_obj.last_sync else 'Never'
        }

        if strategy == 'rsi_macd':
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
                date_rsi_30 = fmt_date(last_date)
                
            # Signal 2: RSI > RSI_SMA posts-oversold
            days_since_rsi_bullish = None
            date_rsi_bullish = None
            if date_obj_rsi_30:
                post_oversold_df = last_year_df[last_year_df.index > date_obj_rsi_30]
                rsi_bullish_after = post_oversold_df[post_oversold_df['RSI'] > post_oversold_df['RSI_SMA']]
                if not rsi_bullish_after.empty:
                    first_date_after = rsi_bullish_after.index[0]
                    days_since_rsi_bullish = (datetime.now().date() - first_date_after).days
                    date_rsi_bullish = fmt_date(first_date_after)

            # Signal 3: Unified MACD Opportunity (12, 26, 9)
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
                    current_streak = last_30_df['cond'].tolist()
                    start_idx = len(current_streak) - 1
                    while start_idx >= 0 and current_streak[start_idx]: start_idx -= 1
                    start_date = last_30_df.index[start_idx + 1]
                    macd_status = 'active'; macd_date = fmt_date(start_date)
                    macd_days = (datetime.now().date() - start_date).days
                elif not active_dates.empty:
                    last_active_date = active_dates[-1]
                    macd_status = 'inactive'; macd_date = fmt_date(last_active_date)
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
            # Strategy 2: 3 EMAS (4, 9, 18)
            df['EMA4'] = ta.ema(df['close'], length=4)
            df['EMA9'] = ta.ema(df['close'], length=9)
            df['EMA18'] = ta.ema(df['close'], length=18)
            
            # Condition: Price > EMA4 AND Price > EMA9 AND Price > EMA18
            df['emas_cond'] = (df['close'] > df['EMA4']) & (df['close'] > df['EMA9']) & (df['close'] > df['EMA18'])
            
            # Find the most recent event where condition became true or is true
            emas_active = df[df['emas_cond']]
            
            emas_date = None
            emas_days = None
            emas_active_today = False

            if not emas_active.empty:
                emas_active_today = bool(df['emas_cond'].iloc[-1])
                if emas_active_today:
                    streak = df['emas_cond'].tolist()
                    idx = len(streak) - 1
                    while idx >= 0 and streak[idx]: idx -= 1
                    last_start_date = df.index[idx + 1]
                    emas_date = fmt_date(last_start_date)
                    emas_days = (datetime.now().date() - last_start_date).days
                else:
                    last_date = emas_active.index[-1]
                    emas_date = fmt_date(last_date)
                    emas_days = (datetime.now().date() - last_date).days

            result.update({
                'emas_active': emas_active_today,
                'emas_date': emas_date,
                'emas_days': emas_days,
                'ema4': float(df['EMA4'].iloc[-1]) if not pd.isna(df['EMA4'].iloc[-1]) else None,
                'ema9': float(df['EMA9'].iloc[-1]) if not pd.isna(df['EMA9'].iloc[-1]) else None,
                'ema18': float(df['EMA18'].iloc[-1]) if not pd.isna(df['EMA18'].iloc[-1]) else None
            })

        return result
