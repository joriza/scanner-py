# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Build/Run Commands

```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS / Linux

# Install dependencies
pip install -r requirements.txt

# Run development server
python app.py

# Run with debug mode
export FLASK_DEBUG=1      # macOS / Linux
set FLASK_DEBUG=1          # Windows
python app.py

# Sync ticker data from Yahoo Finance
python scripts/sync_data.py

# Check database status
python scripts/check_db.py

# Delete tickers without data
python scripts/delete_empty_tickers.py
```

## Code Style & Conventions

### Symbol Normalization (CRITICAL)
Always use `FinanceService.normalize_symbol()` before querying yfinance:
- `BCBA:TICKER` → `TICKER.BA`
- `BRK.B` → `BRK-B`
- This is handled automatically in `FinanceService.sync_ticker_data()`

### yfinance API Usage
- Use `period` parameter instead of `start`/`end` for reliability
- Period is selected based on days since last sync:
  - ≤ 30 days: `"1mo"`
  - ≤ 90 days: `"3mo"`
  - ≤ 180 days: `"6mo"`
  - > 180 days: `"2y"`
- Always set `progress=False` and `timeout=30`

### Database Operations
- Scripts accessing database MUST use `with app.app_context():`
- Price model has unique constraint on `(ticker_id, date)` - no duplicates allowed
- `get_signals()` returns `None` if ticker has < 30 price records (minimum requirement)

### Pandas MultiIndex Handling
After yfinance download, check for MultiIndex:
```python
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)
```

### Weekly Resampling
Always use `'W-FRI'` frequency for weekly data (resamples to Fridays)
Cap dates to today to prevent future labels:
```python
w_start_capped = min(w_start_dt, today)
```

### Error Handling
- Flasgger is OPTIONAL: use try/except on import, app continues without it
- Sync operations use 3 retries with 2-second delays
- Add 1-second delay between tickers in refresh loop to avoid API rate limits

### Git Workflow (Project-Specific)
- Branch naming: `YYYY-MM-DD-N` (e.g., `26-01-26-1`)
- Publish branches immediately after creation: `git push -u origin branch-name`
- Commit messages in Spanish, present tense, ≤72 chars subject
- Push after every relevant commit

### Database Location
- SQLite DB: `instance/scanner.db` (relative path, converted to absolute)
- Directory auto-created on `init_db()` if it doesn't exist

### Logging
- Use `logging` module (already configured at INFO level)
- Log format: `logger.info(f"  {symbol}: {count} nuevos registros agregados")`
