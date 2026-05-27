import yfinance as yf
import pandas_datareader as pdr
from bs4 import BeautifulSoup

def get_yf_latest(ticker):
    try:
        t = yf.Ticker(ticker)
        data = t.history(period="5d")
        if not data.empty:
            return f"{data['Close'].iloc[-1]:.2f}"
    except:
        pass
    return "N/A"

def get_fred_latest(series):
    try:
        data = pdr.get_data_fred(series)
        if not data.empty:
            return f"{data[series].dropna().iloc[-1]:.2f}"
    except:
        pass
    return "N/A"

def get_yf_ratio(t1, t2):
    try:
        data1 = yf.Ticker(t1).history(period="5d")['Close']
        data2 = yf.Ticker(t2).history(period="5d")['Close']
        val = data1.iloc[-1] / data2.iloc[-1]
        return f"{val:.4f}"
    except:
        return "N/A"

data_map = {
    # Yahoo Finance direct
    'WTICMD Index': lambda: get_yf_latest("CL=F"),
    'SPX Index': lambda: get_yf_latest("^GSPC"),
    'NDX Index': lambda: get_yf_latest("^NDX"),
    'RTO/RTY/R2K': lambda: get_yf_latest("^RUT"),
    'BTC1 Curncy': lambda: get_yf_latest("BTC-USD"),
    'S1 COMB COMDTY': lambda: get_yf_latest("ZS=F"),
    'ES1': lambda: get_yf_latest("ES=F"),
    'ARMS Index': lambda: get_yf_latest("^TRIN"),
    
    # Yahoo Finance Ratios
    'DOWGOLD U Index': lambda: get_yf_ratio("^DJI", "GC=F"),
    'FXISPY U Index': lambda: get_yf_ratio("FXI", "SPY"),
    'EEMSPY U Index': lambda: get_yf_ratio("EEM", "SPY"),
    'EFASPY U Index': lambda: get_yf_ratio("EFA", "SPY"),
    'RSPSPY': lambda: get_yf_ratio("RSP", "SPY"),
    'TRANUTY': lambda: get_yf_ratio("^DJT", "^DJU"),
    
    # FRED direct
    'CDTSPRD U Index': lambda: get_fred_latest("BAMLC0A0CMEY"),
    'TMNOXTM%': lambda: get_fred_latest("AMTMNO"),
    'DGNOXTCH%': lambda: get_fred_latest("ADXTNO"),
    'CGNOXA1%': lambda: get_fred_latest("NEWORDER"),
    'UX3 Index': lambda: get_fred_latest("DGS3MO"),
    'NFCIINDX': lambda: get_fred_latest("NFCI"),
    'JOLTHIRS': lambda: get_fred_latest("JTSHIL"),
    'JOLTLAYS': lambda: get_fred_latest("JTSLDL"),
    'JOLTQUTS': lambda: get_fred_latest("JTSQUL"),
    'USLFTTOT': lambda: get_fred_latest("CLF16OV"),
    
    # Proprietary / Proxy
    'SMVLG U Index': lambda: get_yf_ratio("IWN", "IWF"), # Proxy using iShares Russell 2000 Value / Growth
}

with open("impossiblelist.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

updated_count = 0

for row in soup.find_all("tr"):
    tds = row.find_all("td")
    if len(tds) >= 3:
        ticker = tds[0].text.strip()
        if ticker in data_map:
            print(f"Fetching {ticker}...")
            val = data_map[ticker]()
            if val != "N/A":
                tds[2].string = str(val)
                # Ensure the cell is formatted cleanly
                tds[2]['style'] = "padding: 12px 15px; color: var(--color-green); font-weight: 600;"
                updated_count += 1
        elif tds[2].text.strip() == "-":
            # For unmatched, we can mark as Proprietary
            tds[2].string = "N/A (Proprietary/Delayed)"
            tds[2]['style'] = "padding: 12px 15px; color: #9ca3af; font-style: italic;"

with open("impossiblelist.html", "w", encoding="utf-8") as f:
    f.write(str(soup))

print(f"Updated {updated_count} indicators with live data.")
