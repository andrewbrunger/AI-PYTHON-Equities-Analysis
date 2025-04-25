
# Install required packages
!pip install -q yfinance pandas matplotlib plotly colorama numpy termcolor

# Suppress warnings  
import warnings
warnings.filterwarnings('ignore')

# Import required libraries
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from colorama import Fore, Style
from dateutil.relativedelta import relativedelta
import numpy as np
from datetime import datetime, timedelta
from termcolor import colored
import locale
%matplotlib inline
plt.style.use('dark_background')

# DATE RANGE 1:  START YEAR 1999 to Last Trading Day YTD - QQQ Opened in March 1999 - So Starts on January 1, 1999

djia = yf.download("^DJI", start="1999-01-01", end=datetime.today().strftime('%Y-%m-%d'))  # ^DJI just used to check active trading days!
end_date_obj = pd.Timestamp(djia.index[-1])
start_date_obj = datetime(1999, 1, 1)
start_date = start_date_obj.strftime('%Y-%m-%d')
end_date = end_date_obj.strftime('%Y-%m-%d')

# DATE RANGE 1:  START YEAR 1990 to Last Trading Day YTD

#djia = yf.download("^DJI", start="1990-01-01", end=datetime.today().strftime('%Y-%m-%d'))  # ^DJI just used to check active trading days!
#end_date_obj = pd.Timestamp(djia.index[-1])
#start_date_obj = datetime(1990, 1, 1)
#start_date = start_date_obj.strftime('%Y-%m-%d')
#end_date = end_date_obj.strftime('%Y-%m-%d')


# DATE RANGE 2:  LAST 15, 10, 5 YEARS -  from Last Trading Day YTD

#djia = yf.download("^DJI", start="1990-01-01", end=datetime.today().strftime('%Y-%m-%d')) # ^DJI just used to check active trading days!
#end_date_obj = pd.Timestamp(djia.index[-1])
#start_date_obj = end_date_obj - relativedelta(years=10)
#temp_data = yf.download("^DJI", 
#                      start=(start_date_obj - timedelta(days=5)).strftime('%Y-%m-%d'),
#                      end=start_date_obj.strftime('%Y-%m-%d'))
#start_date_obj = pd.Timestamp(temp_data.index[-1])
#start_date = start_date_obj.strftime('%Y-%m-%d')
#end_date = end_date_obj.strftime('%Y-%m-%d')

# DATE RANGE 2:  CLOSED WINDOW - 1/1/1994 until 12/31/2023   -  30 YEARS FROM WORKSHEET

#start_date_obj = datetime(1994, 1, 1)
#end_date_obj = datetime(2023, 12, 31)  # Explicit end date of 2023-12-31
#start_date = start_date_obj.strftime('%Y-%m-%d')
#end_date = end_date_obj.strftime('%Y-%m-%d')


# CRITICAL FOR GRAPHS
# Define start and end year based on the date range
start_year = start_date_obj.year
end_year = end_date_obj.year

# Convert end_date_obj to a UTC-aware pandas Timestamp
full_end_date = pd.Timestamp(end_date_obj, tz="UTC")

# Convert full_end_date to a timezone-naive format if needed
full_end_date_naive = full_end_date.tz_localize(None)

# Calculate the full analysis duration
full_duration = end_date_obj - start_date_obj
full_years = full_duration.days // 365

# Calculate the duration of the full script
duration = end_date_obj - start_date_obj
years = duration.days // 365
months = (duration.days % 365) // 30
days = (duration.days % 365) % 30

# SYMBOLS LIBRARY

# QQQ is known for its high correlation with the Nasdaq-100 Index. In fact, it has delivered a total return of 724% over a specified period (March 1999 - Today), which translates to an annualized return of 14.57% compared to the Nasdaq-100's 14.80%. This small difference is primarily due to the fund's expense ratio and tracking error, which are minimal.

# VOOG is growth stocks in the S&P 500 ; but heavily weighted towards TECH.

symbol_info = {

    # US_INDICES GROUP

    '^GSPC': {'name': 'S&P 500', 'color': '#FFFFFF', 'group': 'US_INDICES', 'div_yield': None, 'starting_value': 1}, # WHITE
    '^IXIC': {'name': 'NASDAQ', 'color': '#00FFFF', 'group': 'US_INDICES', 'div_yield': None, 'starting_value': 1}, # AQUA
    '^NDX': {'name': 'NASDAQ 100', 'color': '#00CCFF', 'group': 'US_INDICES', 'div_yield': None, 'starting_value': 1}, # VIVID SKY BLUE
    'VOOG': {'name': 'VOOG', 'color': '#8AB646', 'group': 'US_INDICES', 'div_yield': None, 'starting_value': 1},
    'QQQ': {'name': 'QQQ - NSDQ 100 PROXY', 'color': '#E600EE', 'group': 'US_INDICES', 'div_yield': None, 'starting_value': 1}, # BRIGHT FUCIA   
    '^DJI': {'name': 'DJI', 'color': '#0680FF', 'group': 'US_INDICES', 'div_yield': None, 'starting_value': 1},  # BLUE

    # GLOBAL_INDICES GROUP
    '000300.SS': {'name': 'CSI 300 (China)', 'color': '#1E90FF', 'group': 'GLOBAL_INDICES', 'div_yield': None, 'starting_value': 1},
    '^N225': {'name': 'Nikkei 225 (Japan)', 'color': '#32CD32', 'group': 'GLOBAL_INDICES', 'div_yield': None, 'starting_value': 1},
    'EEM': {'name': 'MSCI (Emerging)', 'color': '#cd357a', 'group': 'GLOBAL_INDICES', 'div_yield': None, 'starting_value': 1},
    '^STOXX': {'name': 'STOXX 600 (Europe)', 'color': '#ffbb00', 'group': 'GLOBAL_INDICES', 'div_yield': None, 'starting_value': 1},

    # COMMODITIES GROUP
    'GC=F': {'name': 'Gold Price (USD)', 'color': '#FFD700', 'group': 'COMMODITIES', 'div_yield': None, 'starting_value': 1}, # GOLD  
    # Gold Futures, not Spot Price.  To Yr 2000 only.
    
    # REAL ESTATE GROUP
    'VNQ': {'name': 'Vngrd REIT-Partial', 'color': '#8aa6dd', 'group': 'REAL_ESTATE', 'div_yield': None, 'starting_value': 1}, # PALE BLUE

    # CUSTOM GROUPS (To add Universal Color only)
    'ALL_STOCKS': {'name': 'All Stocks', 'color': '#AAFF00', 'group': 'GROUP', 'div_yield': None, 'starting_value': 1},   # LIME GREEN
    'REFERENCE_EQUITIES': {'name': 'Reference Equities', 'color': '#F08080', 'group': 'GROUP', 'div_yield': None, 'starting_value': 1}, # L CORAL
    'GLOBAL_INDICES': {'name': 'Global Indices', 'color': '#FF00FF', 'group': 'GROUP', 'div_yield': None, 'starting_value': 1}, # FUCHSIA
    'COMMODITIES': {'name': 'Commodities', 'color': '#FFD700', 'group': 'GROUP', 'div_yield': None, 'starting_value': 1},       # GOLD
    'REAL_ESTATE': {'name': 'Real Estate', 'color': '#FFFF00', 'group': 'GROUP', 'div_yield': None, 'starting_value': 1},       # HIGHLIGHT YELLOW
    'US_INDICES': {'name': 'U.S. Indices', 'color': '#4EEEB7', 'group': 'GROUP', 'div_yield': None, 'starting_value': 1},       # MINT GREEN
    'TECHFAVS': {'name': 'Tech Favs', 'color': '#EE4B2B', 'group': 'GROUP', 'div_yield': None, 'starting_value': 1},       # CANDY RED

    # REFERENCE EQUITIES GROUP
    'BRK-A': {'name': 'Berkshire - Class A', 'color': '#EE9B4E', 'group': 'REFERENCE EQUITIES', 'div_yield': None, 'starting_value': 1}, # ORANGE

    # TECH FAVS GROUP
    'AMZN': {'name': 'Amazon', 'color': '#FF4500', 'group': 'TECHFAVS', 'div_yield': None, 'starting_value': 1},
    'MSFT': {'name': 'Microsoft', 'color': '#FFE800', 'group': 'TECHFAVS', 'div_yield': None, 'starting_value': 1},
    'GOOG': {'name': 'Google', 'color': '#9ACD32', 'group': 'TECHFAVS', 'div_yield': None, 'starting_value': 1},

    # STOCKS GROUP
    'EPD': {'name': 'Enterprise Products', 'color': '#FF4500', 'group': 'STOCKS', 'div_yield': None, 'starting_value': 1},
    'O': {'name': 'Realty Income', 'color': '#FFE800', 'group': 'STOCKS', 'div_yield': None, 'starting_value': 1},
    'WEC': {'name': 'WEC Energy', 'color': '#FFA500', 'group': 'STOCKS', 'div_yield': None, 'starting_value': 1},
    'PSA': {'name': 'Public Storage', 'color': '#9ACD32', 'group': 'STOCKS', 'div_yield': None, 'starting_value': 1},
    'KO': {'name': 'Coca-Cola', 'color': '#8B0000', 'group': 'STOCKS', 'div_yield': None, 'starting_value': 1},
    'JNJ': {'name': 'Johnson & Johnson', 'color': '#008000', 'group': 'STOCKS', 'div_yield': None, 'starting_value': 1},
    'PEP': {'name': 'PepsiCo', 'color': '#8B4513', 'group': 'STOCKS', 'div_yield': None, 'starting_value': 1},
    'LMT': {'name': 'Lockheed Mrt', 'color': '#9932CC', 'group': 'STOCKS', 'div_yield': None, 'starting_value': 1},
    'PG': {'name': 'Procter & Gamble', 'color': '#8AB646', 'group': 'STOCKS', 'div_yield': None, 'starting_value': 1},
    'CL': {'name': 'Colgate-Palmolive', 'color': '#FF1493', 'group': 'STOCKS', 'div_yield': None, 'starting_value': 1},
    'MCD': {'name': "McDonald's", 'color': '#615E82', 'group': 'STOCKS', 'div_yield': None, 'starting_value': 1},
    'WMT': {'name': "Walmart", 'color': '#00DD88', 'group': 'STOCKS', 'div_yield': None, 'starting_value': 1},
    'ABT': {'name': 'Abbott Labs', 'color': '#ADD8E6', 'group': 'STOCKS', 'div_yield': None, 'starting_value': 1},
    'ADP': {'name': 'ADP', 'color': '#800080', 'group': 'STOCKS', 'div_yield': None, 'starting_value': 1},
    'HRL': {'name': 'Hormel Foods', 'color': '#00EE77', 'group': 'STOCKS', 'div_yield': None, 'starting_value': 1},
    'CLX': {'name': 'Clorox', 'color': '#20B2AA', 'group': 'STOCKS', 'div_yield': None, 'starting_value': 1},
    'DG': {'name': 'Dollar General', 'color': '#FF69B4', 'group': 'STOCKS', 'div_yield': None, 'starting_value': 1},
    'HD': {'name': 'Home Depot', 'color': '#E46BC6', 'group': 'STOCKS', 'div_yield': None, 'starting_value': 1},
    'KR': {'name': 'Kroger', 'color': '#FF6347', 'group': 'STOCKS', 'div_yield': None, 'starting_value': 1},
    'BJ': {'name': "BJ's Wholesale", 'color': '#9944DD', 'group': 'STOCKS', 'div_yield': None, 'starting_value': 1},
    'UNH': {'name': 'United Hcare', 'color': '#00FF00', 'group': 'STOCKS', 'div_yield': None, 'starting_value': 1},
    'TGT': {'name': 'Target', 'color': '#CB6632', 'group': 'STOCKS', 'div_yield': None, 'starting_value': 1},
    'ORLY': {'name': "O'Reilly Auto", 'color': '#00C3EE', 'group': 'STOCKS', 'div_yield': None, 'starting_value': 1},
    'INTU': {'name': 'Intuit', 'color': '#FF00FF', 'group': 'STOCKS', 'div_yield': None, 'starting_value': 1},
    'LOW': {'name': 'Lowes  -New', 'color': '#9E6BDC', 'group': 'STOCKS', 'div_yield': None, 'starting_value': 1},
    'WM': {'name': 'Waste Mngmt  -1/3G', 'color': '#7161FB', 'group': 'STOCKS', 'div_yield': None, 'starting_value': 1},
    'CNI': {'name': 'Can Nat Rail  -1/3G', 'color': '#D1862C', 'group': 'STOCKS', 'div_yield': None, 'starting_value': 1},
    'NEE': {'name': 'NextEra Energy', 'color': '#BC3A48', 'group': 'STOCKS', 'div_yield': None, 'starting_value': 1},
    'DUK': {'name': 'Duke Energy', 'color': '#FF5733', 'group': 'STOCKS', 'div_yield': None, 'starting_value': 1},
    'PM': {'name': 'Philip Morris', 'color': '#DAF7A6', 'group': 'STOCKS', 'div_yield': None, 'starting_value': 1},
    'CDNS': {'name': 'Cadence Design', 'color': '#008B8B', 'group': 'STOCKS', 'div_yield': None, 'starting_value': 1},
}


# Create the Symbol Groups

# US_INDICES group
us_indices_group = []
for symbol in symbol_info:
    if symbol_info[symbol]['group'] == 'US_INDICES': 
        us_indices_group.append(symbol)

# GLOBAL_INDICES group
global_indices_group = []
for symbol in symbol_info:
    if symbol_info[symbol]['group'] == 'GLOBAL_INDICES': 
        global_indices_group.append(symbol)

# REFERENCE EQUITIES group
reference_equities_group = []
for symbol in symbol_info:
    if symbol_info[symbol]['group'] == 'REFERENCE EQUITIES':  
        reference_equities_group.append(symbol)

# STOCKS group
all_stocks_in_stock_group = []
for symbol in symbol_info:
    if symbol_info[symbol]['group'] == 'STOCKS':  
        all_stocks_in_stock_group.append(symbol)

# COMMODITIES group
commodities_group = []
for symbol in symbol_info:
    if symbol_info[symbol]['group'] == 'COMMODITIES':  
        commodities_group.append(symbol)

# REAL_ESTATE group
real_estate_group = []
for symbol in symbol_info:
    if symbol_info[symbol]['group'] == 'REAL_ESTATE':  
        real_estate_group.append(symbol)

# TECH_FAVS group
tech_favs_group = []
for symbol in symbol_info:
    if symbol_info[symbol]['group'] == 'TECHFAVS':  
        tech_favs_group.append(symbol)  

# Combine all groups into a single list
symbols = (
    us_indices_group +
    global_indices_group +
    reference_equities_group +
    all_stocks_in_stock_group +
    commodities_group +
    real_estate_group +
    tech_favs_group
)

############################################################

# Fixed calculate_total_annual_growth function
def calculate_total_annual_growth(stock_data):
    if stock_data.empty:
        return pd.Series()
    
    # Handle MultiIndex columns (This is the new part!)
    stock_data = stock_data.copy()
    stock_data.columns = stock_data.columns.get_level_values(0)
    
    annual_data = stock_data.groupby(stock_data.index.year).agg({
        'Open': 'first',
        'Close': 'last'
    })
    
    annual_growth = (annual_data['Close'] - annual_data['Open']) / annual_data['Open']
    return annual_growth

# Download data
print("Downloading stock data...")
data = {}
total_symbols = len(symbols)
for i, symbol in enumerate(symbols, 1):
    try:
        print(f"Downloading {symbol}... ({i}/{total_symbols})")
        data[symbol] = yf.download(symbol, start=start_date, end=end_date, progress=False)
        data[symbol] = data[symbol][(data[symbol]['Open'] != 0) & (data[symbol]['Close'] != 0)].dropna()
    except Exception as e:
        print(f"Error downloading {symbol}: {e}")

print("\n INITIAL DATA download complete. More symbol downloads for graphs.  Proceeding with initial analysis...")

# CRITICAL FOR GRAPHS

def calculate_yearly_growth(symbol):
    """
    Calculate yearly growth rates for a given stock or index symbol.
    """
    if symbol not in data or data[symbol].empty:
        print(f"Warning: No data available for symbol {symbol}")
        return pd.Series(index=range(start_year, end_year + 1), dtype=float)

    stock_data = data[symbol].copy()

    # Handle MultiIndex columns
    if isinstance(stock_data.columns, pd.MultiIndex):
        stock_data.columns = stock_data.columns.get_level_values(0)

    # Group data by year
    yearly_data = stock_data.groupby(stock_data.index.year).agg({
        'Open': 'first',
        'Close': 'last'
    })

    # Calculate yearly growth
    yearly_data = yearly_data.dropna()
    if yearly_data.empty:
        print(f"Warning: No valid yearly data for {symbol}")
        return pd.Series(index=range(start_year, end_year + 1), dtype=float)

    growth = ((yearly_data['Close'] - yearly_data['Open']) / yearly_data['Open']) * 100

    # Reindex to match the full range of years (e.g., 1990-2020)
    growth = growth.reindex(range(start_year, end_year + 1), fill_value=np.nan)
    return growth

#==================================================================================================
#                                                                            YIB
#==================================================================================================

print('\n\n')

# Draws from Combine all groups into a single list symbols 
# Counts from Current Year.

def find_earliest_year(symbols):
    earliest_years = {}
    today_year = datetime.now().year
    sum_years = 0
    num_symbols_with_data = 0

    # Define fixed column widths
    number_width = 5
    symbol_width = 12
    name_width = 30
    opened_width = 10
    years_width = 5

    # Print header
    print(f"\n{colored('Years in Business [ YIB ] Analysis', 'cyan', attrs=['bold'])}")
    print()
    print(f"{colored('#', 'cyan'):<{number_width}} {colored('SYMBOL', 'cyan'):<{symbol_width}} {colored('NAME', 'cyan'):<{name_width}} {colored('OPENED', 'cyan'):<{opened_width}} {colored('YEARS', 'cyan'):<{years_width}}")
    print(colored("-" * (number_width + symbol_width + name_width + opened_width + years_width + 4), 'cyan'))

    for index, symbol in enumerate(symbols, start=1):
        try:
            data = yf.download(symbol, start="1900-01-01", end=datetime.now(), progress=False)
            if not data.empty:
                earliest_data_date = data.index[0]
                earliest_year = earliest_data_date.year
                earliest_years[symbol] = earliest_year
                years_in_biz = today_year - earliest_year
                sum_years += years_in_biz
                num_symbols_with_data += 1

                # Print the information immediately after processing each symbol
                print(f"{colored(str(index), 'yellow'):<{number_width}} {colored(symbol, 'green'):<{symbol_width}} {colored(symbol_info.get(symbol, {}).get('name', 'N/A'), 'white'):<{name_width}} {colored(str(earliest_year), 'cyan'):<{opened_width}} {colored(str(years_in_biz), 'magenta'):<{years_width}}")
        except Exception as e:
            print(f"{colored(str(index), 'yellow'):<{number_width}} {colored(f'Error processing {symbol}: {str(e)}', 'red')}")

    average_years = sum_years / num_symbols_with_data if num_symbols_with_data > 0 else 0
    print(colored("-" * (number_width + symbol_width + name_width + opened_width + years_width + 4), 'cyan'))
    print(f"{colored('Average Years in Business - All Symbols:', 'cyan'):<{number_width+symbol_width+name_width+opened_width}} {colored(f'{average_years:.2f}', 'yellow', attrs=['bold'])}")

# Call the function with the symbols list
find_earliest_year(symbols)

#==================================================================================================
#                                                                  MATH CHECK :  SINGLE SYMBOL TABLE 1
#==================================================================================================

# SET BOLD AND YELLOW BACK
# 43 Darker Yellow
# 103 Brighter, Lighter Yellow.

# \033[1;103m
# 1 sets bold text
#  The ; separates the formatting parameters
# 43 sets yellow background
#  m ends the formatting sequence
#  \033[0m resets all formatting back to normal

# SET BOLD AND RED TEXT
# \033[1;91m
# 91 sets red text
#  m ends the formatting sequence
#  \033[0m resets all formatting back to normal


def create_math_check_table(symbol, stock_data, title):
    print(f'\nMATH CHECK TABLE for {title}: \033[1m\033[34m{symbol_info[symbol]["name"]}\033[0m')
    
    if stock_data.empty:
        print("No data available for this stock")
        return None
    
    stock_data = stock_data.copy()
    stock_data.columns = stock_data.columns.get_level_values(0)
    
    first_year = stock_data.index.year.min()
    starting_value = stock_data.loc[stock_data.index.year == first_year, 'Open'].iloc[0]
    
    yearly_data = stock_data.groupby(stock_data.index.year).agg({
        'Open': 'first',
        'Close': 'last'
    })
    
    yearly_data['Difference'] = yearly_data['Close'] - yearly_data['Open']
    yearly_data['%_Simp_Ann_Grwth'] = (yearly_data['Close'] - yearly_data['Open']) / yearly_data['Open'] * 100
    yearly_data['% AAGR'] = yearly_data['%_Simp_Ann_Grwth'].expanding().mean()
    yearly_data['% Cum Growth'] = ((yearly_data['Close'] - starting_value) / starting_value) * 100

    # HEADER ROW Adjust Column Width   
    print('{:<6} {:<12} {:<12} {:<12} {:<20} {:<12} {:<12}'.format(
        'Year', 'Open', 'Close', 'Difference', '% Simp Ann Grwth', '% AAGR', '% Cum Growth'))
    print('-' * 90)

    for year, row in yearly_data.iterrows():
        growth = row['%_Simp_Ann_Grwth']
        aagr = row['% AAGR']
        cum = row['% Cum Growth']
        
        is_last_row = year == yearly_data.index[-1]
        
        if growth < 0:
            growth_formatted = f'\033[0;91m{growth:>16.2f}\033[0m'
        else:
            growth_formatted = f'{growth:>16.2f}'
        
        aagr_formatted = f'{aagr:>12.2f}'
        if is_last_row:
            pad = ' ' * (12 - len(f'{aagr:.2f}'))
            aagr_formatted = f'{pad}\033[1;103m{aagr:.2f}\033[0m'

    # DATA ROWS Adjust Column Width        
        row_fmt = f'{year:<6} {row["Open"]:>12.2f} {row["Close"]:>12.2f} {row["Difference"]:>12.2f} {growth_formatted} {aagr_formatted} {cum:>12.2f}'
        print(row_fmt)

    print('\nNEGATIVE RETURNS:')
    negative_years = len(yearly_data[yearly_data['%_Simp_Ann_Grwth'] < 0])
    worst_loss = yearly_data['%_Simp_Ann_Grwth'].min()
    print(f"Number of Years Negative Growth: \033[91m{negative_years}\033[0m")
    print(f"Highest Loss in Period: \033[91m{worst_loss:.2f}%\033[0m")
    return yearly_data

# =============================================
# ABB SINGLE STOCK EXAMINE
# =============================================

print()

print('=' * 120)
print("\nABB SINGLE STOCKS EXAMINE\n")
print('=' * 120)

stock_symbol_to_analyze = 'UNH'  # UnitedHealth Group
if stock_symbol_to_analyze in data:
    stock_data = data[stock_symbol_to_analyze]
    math_check_table = create_math_check_table(stock_symbol_to_analyze, stock_data, "ABB MANUAL STOCK")

stock_symbol_to_analyze = 'CNI'  # Can Nat Rail  -1/3G
if stock_symbol_to_analyze in data:
    stock_data = data[stock_symbol_to_analyze]
    math_check_table = create_math_check_table(stock_symbol_to_analyze, stock_data, "ABB MANUAL STOCK")

stock_symbol_to_analyze = 'BRK-A'
if stock_symbol_to_analyze in data:
    stock_data = data[stock_symbol_to_analyze]
    math_check_table = create_math_check_table(stock_symbol_to_analyze, stock_data, "ABB MANUAL STOCK")

stock_symbol_to_analyze = 'GC=F'  # GOLD
if stock_symbol_to_analyze in data:
    stock_data = data[stock_symbol_to_analyze]
    math_check_table = create_math_check_table(stock_symbol_to_analyze, stock_data, "ABB MANUAL STOCK")

stock_symbol_to_analyze = 'APO'  # Apollo Global Management  APO
if stock_symbol_to_analyze in data:
    stock_data = data[stock_symbol_to_analyze]
    math_check_table = create_math_check_table(stock_symbol_to_analyze, stock_data, "ABB MANUAL STOCK")

stock_symbol_to_analyze = 'CDNS'  # CDNS
if stock_symbol_to_analyze in data:
    stock_data = data[stock_symbol_to_analyze]
    math_check_table = create_math_check_table(stock_symbol_to_analyze, stock_data, "ABB MANUAL STOCK")

stock_symbol_to_analyze = 'AMZN'  # AMAZON
if stock_symbol_to_analyze in data:
    stock_data = data[stock_symbol_to_analyze]
    math_check_table = create_math_check_table(stock_symbol_to_analyze, stock_data, "ABB MANUAL STOCK")

stock_symbol_to_analyze = 'MSFT'  # MICROSOFT
if stock_symbol_to_analyze in data:
    stock_data = data[stock_symbol_to_analyze]
    math_check_table = create_math_check_table(stock_symbol_to_analyze, stock_data, "ABB MANUAL STOCK")

stock_symbol_to_analyze = 'GOOG'  # GOOGLE
if stock_symbol_to_analyze in data:
    stock_data = data[stock_symbol_to_analyze]
    math_check_table = create_math_check_table(stock_symbol_to_analyze, stock_data, "ABB MANUAL STOCK")

stock_symbol_to_analyze = 'VOOG'  # VOOG
if stock_symbol_to_analyze in data:
    stock_data = data[stock_symbol_to_analyze]
    math_check_table = create_math_check_table(stock_symbol_to_analyze, stock_data, "ABB MANUAL STOCK")

stock_symbol_to_analyze = 'QQQ'  # QQQ
if stock_symbol_to_analyze in data:
    stock_data = data[stock_symbol_to_analyze]
    math_check_table = create_math_check_table(stock_symbol_to_analyze, stock_data, "ABB MANUAL STOCK")

# =============================================
# ABB STOCK GROUPS EXAMINE
# =============================================

print()

print('=' * 120)
print("\nABB STOCK GROUPS EXAMINE\n")
print('=' * 120)

def analyze_multiple_stocks():
    print('\n\nINDICES ANALYSIS:')
    for symbol in us_indices_group:
        if symbol in data:
            create_math_check_table(symbol, data[symbol], "INDICES")

    print('\n\nALL STOCKS ANALYSIS:')
    for symbol in all_stocks_in_stock_group:
        if symbol in data:
            create_math_check_table(symbol, data[symbol], "ALL STOCKS")

# Run the analysis            
analyze_multiple_stocks()

#==================================================================================================
#                                              SUMMARY ANAYSIS TABLES 
#==================================================================================================

# SET BOLD AND YELLOW BACK
# 43 Darker Yellow
# 103 Brighter, Lighter Yellow.

# \033[1;43m
# 1 sets bold text
#  The ; separates the formatting parameters
# 43 sets yellow background
#  m ends the formatting sequence
#  \033[0m resets all formatting back to normal

# SET BOLD AND RED TEXT

# \033[1;91m
# 91 sets red text
#  m ends the formatting sequence
#  \033[0m resets all formatting back to normal

# ================== GROUP SYMBOLS  ==================

#  The script uses yfinance library to fetch financial data directly from Yahoo Finance's API. 
#  These data are not ‘pulled from’ from earlier tables.
#  See “Calculations Detail”.txt for more info.

#  U.S. INDICES Summary Table (01/01/1990 to 11/29/2024):
#  REFERENCE EQUITIES Summary Table (01/01/1990 to 11/29/2024):
#  RECESSION RESISTANT Summary Table (01/01/1990 to 11/29/2024):
#  GLOBAL INDICES Summary Table (01/01/1990 to 11/29/2024):
#  GOLD Summary Table (01/01/1990 to 11/29/2024):
#  REAL ESTATE Summary Table (01/01/1990 to 11/29/2024):


# Groups INCLUDED
tech_favs_group = [symbol for symbol, info in symbol_info.items() if info['group'] == 'TECHFAVS']
us_indices_group = [symbol for symbol, info in symbol_info.items() if info['group'] == 'US_INDICES']
reference_equities_group = [symbol for symbol, info in symbol_info.items() if info['group'] == 'REFERENCE EQUITIES']
all_stocks_in_stock_group = [symbol for symbol, info in symbol_info.items() if info['group'] == 'STOCKS']
global_indices_group = [symbol for symbol, info in symbol_info.items() if info['group'] == 'GLOBAL_INDICES']
gold_symbol = [symbol for symbol, info in symbol_info.items() if info['group'] == 'COMMODITIES']
real_estate_proxy = [symbol for symbol, info in symbol_info.items() if info['group'] == 'REAL_ESTATE']


# ================== SUMMARY TABLE FUNCTION  ==================

def create_summary_table(symbols, group_name, start_date, end_date):
   summary_data = []
   
   for symbol in symbols:
       if symbol not in data or data[symbol].empty:
           continue
       
       # Filter stock data based on the given start and end dates
       stock_data = data[symbol]
       stock_data = stock_data[(stock_data.index >= start_date) & (stock_data.index <= end_date)]
       
       # Handle MultiIndex columns
       stock_data = stock_data.copy()
       stock_data.columns = stock_data.columns.get_level_values(0)
       
       # Calculate metrics based on the filtered data
       first_year = stock_data.index.year.min()
       starting_value = stock_data.loc[stock_data.index.year == first_year, 'Open'].iloc[0]
       
       yearly_data = stock_data.groupby(stock_data.index.year).agg({
           'Open': 'first',
           'Close': 'last'
       })
       
       yearly_growth = ((yearly_data['Close'] - yearly_data['Open']) / yearly_data['Open'] * 100)
       cum_growth = ((yearly_data['Close'].iloc[-1] - starting_value) / starting_value * 100)
       aagr = yearly_growth.mean()
       negative_years = len(yearly_growth[yearly_growth < 0])
       worst_loss = yearly_growth.min()
       
       div_yield = symbol_info[symbol].get('div_yield', 0) or 0
       total_return = aagr + div_yield
       
       summary_data.append({
           'Name': symbol_info[symbol]['name'],
           '% Cum Growth': cum_growth,
           '% AAGR': aagr,
           '% Ann Div': div_yield,
           'POS TOT RET': total_return,
           '# Yrs Below 0': negative_years,
           'Loss Hi': worst_loss
       })
   
   if not summary_data:
       print(f"No data available for {group_name}")
       return None
   
   # Create DataFrame and sort by Cumulative Growth
   df = pd.DataFrame(summary_data)
   df = df.sort_values('% AAGR', ascending=False)
   
   # Calculate averages for summary row
   avg_row = {
       'Name': "AVG >>",
       '% Cum Growth': df['% Cum Growth'].mean(),
       '% AAGR': df['% AAGR'].mean(),
       '% Ann Div': df['% Ann Div'].mean(),
       'POS TOT RET': df['POS TOT RET'].mean(),
       '# Yrs Below 0': df['# Yrs Below 0'].mean(),
       'Loss Hi': df['Loss Hi'].mean()
   }
   
   # Add average row
   df = pd.concat([df, pd.DataFrame([avg_row])], ignore_index=True)
   
   # Format dates
   formatted_start_date = datetime.strptime(start_date, "%Y-%m-%d").strftime("%m/%d/%Y")
   formatted_end_date = datetime.strptime(end_date, "%Y-%m-%d").strftime("%m/%d/%Y")
   
   # Print formatted table with bold group name
   print(f"\n\033[1m{group_name}\033[0m Summary Table ({formatted_start_date} to {formatted_end_date}):")
   print('=' * 120)
   print('{:<20} {:>15} {:>10} {:>13} {:>14} {:>13} {:>10}'.format(
       'Name', 'Cum Growth%', 'AAGR%', 'Ann Div%', 'POS TOT RET', 'Yrs Below 0', 'Loss Hi%'
   ))
   print('-' * 120)
   
   for i, row in df.iterrows():
       name = row['Name']
       is_avg = "AVG >>" in name
       aagr_value = float(row['% AAGR'])
       
       if is_avg:
           # Format for average row with colors
           print('{:<20} {:>12.2f} {:>8}\033[1;103m{:>6.2f}\033[0m {:>10.2f} {:>12.2f} {:>12d} \033[1;91m{:>12.2f}\033[0m'.format(
               name,
               float(row['% Cum Growth']),
               '',  # spacing before AAGR
               aagr_value,
               float(row['% Ann Div']),
               float(row['POS TOT RET']),
               int(row['# Yrs Below 0']),
               float(row['Loss Hi'])
           ))
       else:
           # Format for regular rows with red Loss Hi% but no other colors
           print('{:<20} {:>12.2f} {:>8}{:>6.2f} {:>10.2f} {:>12.2f} {:>12d} \033[91m{:>12.2f}\033[0m'.format(
               name,
               float(row['% Cum Growth']),
               '',  # spacing before AAGR
               aagr_value,
               float(row['% Ann Div']),
               float(row['POS TOT RET']),
               int(row['# Yrs Below 0']),
               float(row['Loss Hi'])
           ))
   
   print('=' * 120)
   return df

def validate_symbols(symbols):
   for symbol in symbols:
       if symbol not in symbol_info:
           print(f"Warning: Symbol {symbol} not found in symbol_info!")

# ================== MAIN PROCESS  ==================

# Print individual tables
print('\n\n')
print('=' * 120)
print("\nSUMMARY TABLES\n")
print('=' * 120)



# Ensure symbols are valid

validate_symbols(symbols)
validate_symbols(us_indices_group)
validate_symbols(tech_favs_group)
validate_symbols(reference_equities_group)
validate_symbols(all_stocks_in_stock_group)
validate_symbols(global_indices_group)
validate_symbols(gold_symbol)
validate_symbols(real_estate_proxy)


# Indices Summary
indices_summary = create_summary_table(us_indices_group, "U.S. INDICES", start_date, end_date)

# Tech Favs Summary
tech_favs_summary = create_summary_table(tech_favs_group, "TECH FAVS", start_date, end_date)

# Reference Equities Summary
ref_equities_summary = create_summary_table(reference_equities_group, "REFERENCE EQUITIES", start_date, end_date)

# All Stocks Summary
all_stocks_summary = create_summary_table(all_stocks_in_stock_group, "RECESSION RESISTANT", start_date, end_date)

# Global Indices Summary
global_indices_summary = create_summary_table(global_indices_group, "GLOBAL INDICES", start_date, end_date)

# Gold Futures Summary
gold_summary = create_summary_table(gold_symbol, "GOLD", start_date, end_date)

# Real Estate Proxy Summary
real_estate_summary = create_summary_table(real_estate_proxy, "REAL ESTATE", start_date, end_date)



#==================================================================================================
#                                                                            SORTED TABLE
#==================================================================================================

#  SORTED TABLE (01/01/1990 to 11/29/2024):

# 	The Sorted Table gathers its data from the Summary Tables.
# 	It does NOT calculate these data within the script.
#	Your approach of using the data from the Summary Tables for the Sorted Table, 
#	rather than recalculating the values, is generally a smart approach .

# Data Set Inclusion:
#	Dynamically gathers all names included in SUMMARY TABLES and lists these. 
#     (For now: U.S. INDICES, REFERENCE EQUITIES, RECESSION RESISTANT stocks, GLOBAL INDICES, GOLD, and REAL ESTATE.)

# Averages:
# Extracts the last row  (‘AVG >>') for each record and appends it to the sorted_data table.

# Index Stocks:
#	Dynamically gathers all names included in U.S. INDICES Summary Table and adds these. 
#     (For now: NASDAQ, NASDAQ 100, S&P 500, and DJI.)
#     (Then I Added QQQ.)

def create_sorted_table(summary_tables, start_date, end_date, indices_summary):
    """
    Create a sorted summary table based on the final row ('AVG >>') of each group summary,
    including specific rows dynamically extracted from the U.S. INDICES table.
    :param summary_tables: List of tuples containing (table_name, table_df)
    :param start_date: Start date for formatting
    :param end_date: End date for formatting
    :param indices_summary: DataFrame containing the U.S. INDICES summary
    :return: Sorted DataFrame
    """
    sorted_data = []
    
    # Add average rows from summary tables
    for table_name, table_df in summary_tables:
        if table_df is not None and not table_df.empty:
            avg_row = table_df.iloc[-1].to_dict()
            avg_row['Name'] = table_name  # Replace 'AVG >>' with the table name
            sorted_data.append(avg_row)
    
    # Dynamically extract rows for THESE INDICES in SUMMARY TABLES ABOVE >> NASDAQ, NASDAQ 100, VOOG, S&P 500, DJI
    if indices_summary is not None and not indices_summary.empty:
        indices_to_add = ["NASDAQ", "NASDAQ 100", "QQQ - NSDQ 100 PROXY", "VOOG", "S&P 500", "DJI",] # The TEXT NAMES in the Table.
        for symbol in indices_to_add:
            if symbol in indices_summary['Name'].values:
                row = indices_summary[indices_summary['Name'] == symbol].iloc[0].to_dict()
                sorted_data.append(row)
    
    if not sorted_data:
        print("\n\033[1mNo data available for SORTED TABLE\033[0m")
        return None
    
    # Create DataFrame and sort by AAGR% in descending order
    sorted_df = pd.DataFrame(sorted_data)
    sorted_df = sorted_df.sort_values('% AAGR', ascending=False)
    
    # Format dates
    formatted_start_date = datetime.strptime(start_date, "%Y-%m-%d").strftime("%m/%d/%Y")
    formatted_end_date = datetime.strptime(end_date, "%Y-%m-%d").strftime("%m/%d/%Y")
    
    # Print formatted table with bold heading
    print(f"\n\033[1mSORTED TABLE ({formatted_start_date} to {formatted_end_date}):\033[0m")
    print('=' * 120)
    print('{:<20} {:>15} {:>10} {:>13} {:>14} {:>13} {:>10}'.format(
        'Name', 'Cum Growth%', 'AAGR%', 'Ann Div%', 'POS TOT RET', 'Yrs Below 0', 'Loss Hi%'
    ))
    print('-' * 120)
    
    for _, row in sorted_df.iterrows():
        name = row['Name']
        aagr_value = float(row['% AAGR'])
        
        # Highlight the AAGR% and make Loss Hi% bold red
        print('{:<20} {:>12.2f} {:>8}\033[1;103m{:>6.2f}\033[0m {:>10.2f} {:>12.2f} {:>12d} \033[1;91m{:>12.2f}\033[0m'.format(
            name,
            float(row['% Cum Growth']),
            '',  # spacing before AAGR
            aagr_value,
            float(row['% Ann Div']),
            float(row['POS TOT RET']),
            int(row['# Yrs Below 0']),
            float(row['Loss Hi'])
        ))
    
    print('=' * 120)
    return sorted_df

# ================== ADD SORTED TABLE TO MAIN PROCESS ==================

    # Dynamically extract rows for THESE GROUPS >> 
summary_tables = [
    ("U.S. INDICES", indices_summary),
    ("REFERENCE EQUITIES", ref_equities_summary),
    ("RECESSION RESISTANT", all_stocks_summary),
    ("GLOBAL INDICES", global_indices_summary),
    ("GOLD", gold_summary),
    ("REAL ESTATE", real_estate_summary),
    ("TECH FAVS", tech_favs_summary),
]

# Create and display the SORTED TABLE
sorted_table = create_sorted_table(summary_tables, start_date, end_date, indices_summary)

#==================================================================================================
#                                                                            WEIGHTED TABLES
#==================================================================================================

# ABB

print()
print()

# Print individual tables and collect averages
print('=' * 120)
print("\nWEIGHTED TABLES\n")
print('=' * 120)

print()
print()

import pandas as pd
from datetime import datetime
import yfinance as yf
import numpy as np

# Define tables with their components and weights
tables = {
    "\033[1mEXCEL # 6- Original 60, 0 , 20, 20\033[0m": {  # Bold the title
        'NASDAQ 100': {'symbols': ['^NDX'], 'weight': 60},
        'S&P 500': {'symbols': ['^GSPC'], 'weight': 20},
        'DOW JONES': {'symbols': ['^DJI'], 'weight': 20},
    },
    "\033[1mTable 1- Artificial Intelligence Calculated Optimal\033[0m": {  # Bold the title
        'NASDAQ 100': {'symbols': ['^NDX'], 'weight': 30},
        'RECESSION RESISTANT': {'symbols': all_stocks_in_stock_group, 'weight': 50},  # Group Linked
        'GOLD': {'symbols': ['GC=F'], 'weight': 20},
    },
    "\033[1mEXCEL # 2- 50/50 Nasdaq 100 and Brk-A\033[0m": {  # Bold the title
        'NASDAQ 100': {'symbols': ['^NDX'], 'weight': 50},
        'BRK A/B': {'symbols': ['BRK-A'], 'weight': 50},
    },
    "\033[1mEXCEL # 3- 40/40 Nasdaq 100 and Brk-A 10 Gold, 10 UNH\033[0m": {  # Bold the title
        'NASDAQ 100': {'symbols': ['^NDX'], 'weight': 40},
        'UNH': {'symbols': ['UNH'], 'weight': 10},
        'BRK A/B': {'symbols': ['BRK-A'], 'weight': 40},
        'GOLD': {'symbols': ['GC=F'], 'weight': 10},
    },
    "\033[1mEXCEL # 1- 40/40 Nasdaq 100 and Brk-A 10 Gold, 10 CNI (Bill Gates 1/3)\033[0m": {  # Bold the title
        'NASDAQ 100': {'symbols': ['^NDX'], 'weight': 40},
        'CNI': {'symbols': ['CNI'], 'weight': 10},
        'BRK A/B': {'symbols': ['BRK-A'], 'weight': 40},
        'GOLD': {'symbols': ['GC=F'], 'weight': 10},
    },
    "\033[1mEXCEL # 5- 40/40 Nasdaq 100 and Brk-A 10 Gold, 10 S&P\033[0m": {  # Bold the title
        'NASDAQ 100': {'symbols': ['^NDX'], 'weight': 40},
        'S&P 500': {'symbols': ['^GSPC'], 'weight': 10},
        'BRK A/B': {'symbols': ['BRK-A'], 'weight': 40},
        'GOLD': {'symbols': ['GC=F'], 'weight': 10},
    },
    "\033[1mTable 3- 30/30 Nasdaq 100 and Brk-A + 30 Elsewhere\033[0m": {  # Bold the title
        'NASDAQ 100': {'symbols': ['^NDX'], 'weight': 30},
        'S&P 500': {'symbols': ['^GSPC'], 'weight': 20},
        'BRK A/B': {'symbols': ['BRK-A'], 'weight': 30},
        'GOLD': {'symbols': ['GC=F'], 'weight': 10},
    },
    "\033[1mTable 4- 30/30 Nasdaq 100 and Brk-A + 35 Elsewhere\033[0m": {  # Bold the title
        'NASDAQ 100': {'symbols': ['^NDX'], 'weight': 30},
        'S&P 500': {'symbols': ['^GSPC'], 'weight': 25},
        'BRK A/B': {'symbols': ['BRK-A'], 'weight': 30},
        'GOLD': {'symbols': ['GC=F'], 'weight': 15},
    },
    "\033[1mEXCEL # 4- A Unique Mix\033[0m": {  # Bold the title
        'NASDAQ 100': {'symbols': ['^NDX'], 'weight': 40},
        'BRK A/B': {'symbols': ['BRK-A'], 'weight': 40},
        'APO': {'symbols': ['APO'], 'weight': 2.5},
        'CDNS': {'symbols': ['CDNS'], 'weight': 2.5},
        'UNH': {'symbols': ['UNH'], 'weight': 2.5},
        'CNI': {'symbols': ['CNI'], 'weight': 2.5},
        'GOLD': {'symbols': ['GC=F'], 'weight': 10}
    }
}

# Fetch all required data once
weighted_data = {}
symbols = set()
for table in tables.values():
    for component in table.values():
        symbols.update(component['symbols'])

for symbol in symbols:
    try:
        df = yf.download(symbol, start=start_date, end=end_date, progress=False)
        df.columns = df.columns.get_level_values(0)
        weighted_data[symbol] = df
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")

# Add these two lines HERE
formatted_start_date = start_date_obj.strftime('%m/%d/%Y')
formatted_end_date = end_date_obj.strftime('%m/%d/%Y')

# METRIC CALCULATIONS:
# AAGR (Annual Average Growth Rate)
# - Only uses years where stock was actively trading (valid, non-zero prices)
# - Based on actual trading years within date range

# Years < 0 (Negative Years)
# - Counts negative return years within script's full date range
# - Zero price periods are excluded from count
# - Shows total downside occurrence frequency

# Loss Hi% (Highest Loss)
# - Worst single-year performance within script's date range
# - Only considers valid trading periods
# - Represents maximum downside risk

# Cumulative Growth%
# - Based on full script date range
# - Calculated from first valid trading price to last
# - Shows total return over analysis period

def calculate_metrics(components):
    """Calculate all metrics for a table configuration"""
    component_metrics = {}
    weighted_yearly_returns = pd.Series(dtype=float)

    # Validate total weights sum to 100
    total_weight = sum(info['weight'] for info in components.values())
    if not np.isclose(total_weight, 100, rtol=1e-5):
        print(f"Warning: Weights sum to {total_weight}, not 100")

    for component_name, info in components.items():
        symbols = info['symbols']
        weight = info['weight']
        
        # Calculate returns for component
        all_returns = pd.DataFrame()
        for symbol in symbols:
            if symbol in weighted_data and not weighted_data[symbol].empty:
                stock_data = weighted_data[symbol]
                # Find first valid data point (non-zero open price)
                valid_data = stock_data[stock_data['Open'] > 0]
                if valid_data.empty:
                    continue
                    
                yearly_data = valid_data.groupby(valid_data.index.year).agg({
                    'Open': 'first',
                    'Close': 'last'
                })
                
                # Calculate returns only for valid years
                yearly_returns = ((yearly_data['Close'] - yearly_data['Open']) / yearly_data['Open'] * 100)
                # Clip extreme values to prevent infinity
                yearly_returns = yearly_returns.clip(-1000, 1000)
                all_returns[symbol] = yearly_returns

        if not all_returns.empty:
            try:
                component_returns = all_returns.mean(axis=1)
                active_years = len(component_returns)
                aagr = component_returns.mean()  # Average of actual trading years

                # More stable cumulative growth calculation
                cumulative_returns = (1 + component_returns/100)
                cumulative_growth = (cumulative_returns.prod() - 1) * 100
                
                neg_years = len(component_returns[component_returns < 0])
                worst_loss = component_returns.min()

                component_metrics[component_name] = {
                    'returns': component_returns,
                    'cum_growth': cumulative_growth,
                    'aagr': aagr,
                    'neg_years': neg_years,
                    'worst_loss': worst_loss,
                    'weight': weight,
                    'active_years': active_years
                }

                # Add weighted returns to total
                if weight > 0:
                    weighted_returns = component_returns * (weight / 100)
                    weighted_yearly_returns = weighted_yearly_returns.add(weighted_returns, fill_value=0)
            except Exception as e:
                print(f"Error calculating metrics for {component_name}: {e}")

    return component_metrics, weighted_yearly_returns

def calculate_table_metrics(table_config):
    """Calculate and store all metrics for a table"""
    component_metrics, weighted_returns = calculate_metrics(table_config)

    # Calculate weighted metrics
    total_neg_years = sum(
        component['neg_years'] * component['weight'] / 100
        for component in component_metrics.values()
    )

    total_active_years = len(weighted_returns.dropna())
    
    # Calculate total metrics with error handling
    try:
        total_cum_growth = ((1 + weighted_returns / 100).prod() - 1) * 100
    except Exception:
        total_cum_growth = float('inf')
        
    total_aagr = sum(
        component_metrics[name]['aagr'] * table_config[name]['weight'] / 100
        for name in table_config if name in component_metrics
    )
    
    total_worst_loss = sum(
        component_metrics[name]['worst_loss'] * table_config[name]['weight'] / 100
        for name in table_config if name in component_metrics
    )
    
    gut_check = total_aagr / abs(total_worst_loss) if total_worst_loss != 0 else float('inf')

    return {
        'component_metrics': component_metrics,
        'weighted_returns': weighted_returns,
        'total_cum_growth': total_cum_growth,
        'total_aagr': total_aagr,
        'total_neg_years': total_neg_years,
        'total_worst_loss': total_worst_loss,
        'gut_check': gut_check
    }

# Calculate metrics for all tables and sort by gut check ratio
table_results = []
for table_name, config in tables.items():
    metrics = calculate_table_metrics(config)
    table_results.append((table_name, config, metrics))

table_results.sort(key=lambda x: x[2]['gut_check'], reverse=True)

# Print sorted tables
print("\nTABLES SORTED BY GUT CHECK RATIO (HIGHEST TO LOWEST):")

for rank, (table_name, config, metrics) in enumerate(table_results, 1):
    print(f"\nRank {rank}: {table_name} - Time Period: {formatted_start_date} to {formatted_end_date}")
    print("\nWEIGHTED TABLE")
    print("-" * 123)
    print("{:<25} {:>12} {:>15} {:>12} {:>12} {:>14} {:>10} {:>15}".format(
        'Name', 'Weighting', 'Cum Growth%', 'AAGR%', 'Ann Div%', 'POS TOT RET', 'Yrs < 0', 'Loss Hi%'
    ))
    print("-" * 123)
    
    # Print component rows
    for component_name, info in config.items():
        if component_name in metrics['component_metrics']:
            m = metrics['component_metrics'][component_name]
            print("{:<25} \033[94m{:>9}%\033[0m {:>15.2f} {:>12.2f} {:>12.2f} {:>14.2f} {:>10d} \033[91m{:>15.2f}\033[0m".format(
                component_name, m['weight'], m['cum_growth'], m['aagr'],
                0.00, m['aagr'], m['neg_years'], m['worst_loss']
            ))
    
    print("-" * 123)
    print("{:<25} \033[94m{:>9}%\033[0m {:>15.2f} \033[1;103m{:>12.2f}\033[0m {:>12.2f} {:>14.2f} {:>10.1f} \033[91m\033[1m{:>15.2f}\033[0m".format(
        "Weighted Results >>", 100,
        metrics['total_cum_growth'],
        metrics['total_aagr'],
        0.00,
        metrics['total_aagr'],
        metrics['total_neg_years'],
        metrics['total_worst_loss']
    ))
    
    if rank == 1:
        print(f"\033[48;2;220;88;42m\033[97mGut Check Ratio (AAGR / Hi Loss%): {metrics['gut_check']:.2f}\033[0m")
    else:
        print(f"Gut Check Ratio (AAGR / Hi Loss%): {metrics['gut_check']:.2f}")



#==================================================================================================
#                                                                            SCATTER CHART
#==================================================================================================

# The scatter chart gets its data from the sorted_table.

print()
print()

import matplotlib.pyplot as plt

def create_scatter_plot(sorted_table):
    try:
        # Prepare data for plotting
        x = sorted_table['Loss Hi'].tolist()  # Changed from 'Loss Hi%' to 'Loss Hi'
        y = sorted_table['% AAGR'].tolist()
        sizes = [yr * 20 for yr in sorted_table['# Yrs Below 0'].tolist()]
        labels = sorted_table['Name'].tolist()

        # Dynamic color assignment
        unique_labels = set(labels)
        color_map = {label: plt.cm.tab10(i/len(unique_labels)) for i, label in enumerate(unique_labels)}
        colors = [color_map[label] for label in labels]

        # Sort data by Loss Hi in ascending order
        sorted_indices = sorted(range(len(x)), key=lambda k: x[k])
        x_sorted = [x[i] for i in sorted_indices]
        y_sorted = [y[i] for i in sorted_indices]
        sizes_sorted = [sizes[i] for i in sorted_indices]
        colors_sorted = [colors[i] for i in sorted_indices]
        labels_sorted = [labels[i] for i in sorted_indices]

        # Create the scatter plot
        plt.figure(figsize=(12, 8), facecolor='black')
        plt.scatter(x_sorted, y_sorted, s=sizes_sorted, c=colors_sorted, alpha=0.8, edgecolors="w", linewidth=1.2)

        # Add labels to the points
        for i, label in enumerate(labels_sorted):
            plt.text(x_sorted[i], y_sorted[i], f"{label}\n({y_sorted[i]:.2f}%)", fontsize=9, color="white", ha='right', va='bottom')

        # Add titles and labels
        plt.title("Scatter Plot: AAGR vs. Loss Hi with Bubble Size as Yrs Below 0", fontsize=16, color="white")
        plt.xlabel("Loss Hi (Worst Loss %)", fontsize=12, color="white")
        plt.ylabel("AAGR (%)", fontsize=12, color="white")
        plt.grid(alpha=0.3, color="gray")
        plt.axhline(0, color='white', linewidth=0.8, linestyle='--')

        # Set plot background color to black
        plt.gca().set_facecolor("black")

        # Add padding each side of X and reverse X-axis limits
        x_padding = (max(x_sorted) - min(x_sorted)) * 0.08
        plt.xlim([max(x_sorted) + x_padding, min(x_sorted) - x_padding])

        # Display the plot
        plt.show()

    except Exception as e:
        print(f"Error creating scatter plot: {e}")
        print("Available columns:", sorted_table.columns.tolist())

# Call the function with the actual sorted table
create_scatter_plot(sorted_table)

#==================================================================================================
#                                                                   DESIRABILITY LIST - LINKED TO SORTED TABLE
#==================================================================================================

#	AAGR:  15.32%

#	HI LO (Highest Loss): Divide highest loss by the worst loss in the group (31.88 / 41.99 = 0.7592). 
#	This is a valid approach to scale the losses relative to the worst performer.

#	YRS BEL (Years Below Zero): Divide Years Below Zero  by the worst in the group (6 / 10 = 0.6). 
#	This is also a reasonable approach.

#	Volatility Measure: Combine the normalized HI LO and YRS BEL (0.7592 + 0.6 = 1.359). 
#	This gives a composite measure of volatility and downside risk.

#	Final Score: You're dividing the AAGR by the Volatility Measure (15.32 / 1.359 = 11.273).

print()

import pandas as pd

def calculate_desirability(sorted_table):
    worst_loss = sorted_table['Loss Hi'].abs().max()
    worst_years_below = sorted_table['# Yrs Below 0'].max()

    sorted_table['Normalized Loss'] = sorted_table['Loss Hi'].abs() / worst_loss
    sorted_table['Normalized Years Below'] = sorted_table['# Yrs Below 0'] / worst_years_below
    sorted_table['Volatility Measure'] = sorted_table['Normalized Loss'] + sorted_table['Normalized Years Below']
    sorted_table['Desirability Score'] = sorted_table['% AAGR'] / sorted_table['Volatility Measure']

    return sorted_table

def main(sorted_table):
    # Convert '# Yrs Below 0' to integer
    sorted_table['# Yrs Below 0'] = sorted_table['# Yrs Below 0'].astype(int)
    desirable_table = calculate_desirability(sorted_table)
    desirability_sorted = desirable_table.sort_values('Desirability Score', ascending=False)
    
    print("\nDesirability Scores (SORTED TABLE):")
    print('-' * 85)
    print('{:<25} {:>12} {:>12} {:>15} {:>15}'.format(
        'Name', 'AAGR%', 'Loss Hi', 'Yrs Below 0', 'Desirability'
    ))
    print('-' * 85)
    
    for _, row in desirability_sorted.iterrows():
        print('{:<25} {:>12.2f} {:>12.2f} {:>12d} {:>15.2f}'.format(
            row['Name'],
            row['% AAGR'],
            row['Loss Hi'],
            row['# Yrs Below 0'],
            row['Desirability Score']
        ))
    
    print('-' * 85)

# This line assumes 'sorted_table' is already defined elsewhere in your code
main(sorted_table)

#==================================================================================================
#                                                                   COST OF RECESSION BASKET
#==================================================================================================

print()
print()

# Print individual tables and collect averages
print('=' * 120)
print("\nCOST OF RECESSION BASKET (Not Equal Dollar Invested- Instead 1 Share Per)\n")
print('=' * 120)

print()
print()

import yfinance as yf
import pandas as pd

# Function to fetch the latest stock price
def fetch_latest_price(symbol):
    try:
        # Fetch the last available close price
        data = yf.download(symbol, period="5d", interval="1d", progress=False)
        if not data.empty:
            return float(data['Close'].iloc[-1])  # Ensure scalar value
        return None
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

# Function to calculate the total cost and percentage of total
def calculate_cost_and_percentage(all_stocks):
    investment_data = []

    for symbol in all_stocks:
        latest_price = fetch_latest_price(symbol)
        if latest_price is not None and latest_price > 0:  # Ensure valid scalar value
            investment_data.append({
                'Symbol': symbol,
                'Price': round(latest_price, 2)  # Round to 2 decimal places
            })

    # Create DataFrame
    investment_df = pd.DataFrame(investment_data)

    # Add row numbers starting from 1
    investment_df.index += 1

    # Calculate the total cost
    total_cost = investment_df['Price'].sum()

    # Add a percentage of total column, rounded to 2 decimal places
    investment_df['% Total'] = round((investment_df['Price'] / total_cost) * 100, 2)

    # Format all numerical columns with commas
    investment_df['Price'] = investment_df['Price'].apply(lambda x: f"{x:,.2f}")
    investment_df['% Total'] = investment_df['% Total'].apply(lambda x: f"{x:,.2f}")

    return investment_df, f"{total_cost:,.2f}"

# Specify the stock group (replace with your actual list of stocks)
all_stocks_in_stock_group = [symbol for symbol, info in symbol_info.items() if info['group'] == 'STOCKS']

# Generate the table and calculate total cost
investment_table, total_cost = calculate_cost_and_percentage(all_stocks_in_stock_group)

# Display the table and total cost
from IPython.display import display
print("Stock Prices and Percentages:")
display(investment_table)
print(f"\nTotal Cost of Buying 1 Share of Each Stock: ${total_cost}")



#==================================================================================================
#                                                                            LINE GRAPHS
#==================================================================================================

print()
print()

# Print individual tables and collect averages
print('=' * 120)
print("\nLINE GRAPHS\n")
print('=' * 120)

print()
print()


# Function to calculate metrics for plotting
def calculate_metrics_for_period(symbol, start_date, end_date):
    if symbol not in data or data[symbol].empty:
        return None
    
    # Convert to pandas Timestamp and make timezone naive
    start_ts = pd.Timestamp(start_date).tz_localize(None)
    end_ts = pd.Timestamp(end_date).tz_localize(None)
    
    # Get stock data and make its index timezone naive
    period_data = data[symbol].copy()
    period_data.index = period_data.index.tz_localize(None)
    
    # Apply date mask
    mask = (period_data.index >= start_ts) & (period_data.index <= end_ts)
    period_data = period_data[mask]
    
    if period_data.empty:
        return None
    
    # Handle MultiIndex columns
    period_data.columns = period_data.columns.get_level_values(0)
    
    yearly_data = period_data.groupby(period_data.index.year).agg({
        'Open': 'first',
        'Close': 'last'
    })
    
    growth = ((yearly_data['Close'] - yearly_data['Open']) / yearly_data['Open'] * 100)
    return growth

#-------------------------------------------------------------
# Rolling AAGR Graph
#-------------------------------------------------------------

##########################################################################

#######  Some Symbols   #######################################################

# 7 Custom GROUPS

# ('US_INDICES', U.S. Indices)
# ('GLOBAL_INDICES', Global Indices)
# ('ALL_STOCKS', All Stocks)
# ('REFERENCE_EQUITIES', Reference Equities)
# ('COMMODITIES', Commodities)
# ('REAL_ESTATE', Real Estate)

# 3 U.S Indices

# ('^GSPC', S&P 500)
# ('^IXIC', NASDAQ)
# ('^DJI', DJI)

# Single Stocks

# ('BRK-A', Berkshire - Class A)
# ('EPD', Enterprise Products)
# ('O', Realty Income)

# Commodities

# ('GC=F', Gold Price (USD))

# Real Estate

# ('VNQ', Vngrd REIT-Partial)

# 4 Global Indices

# ('000300.SS', CSI 300 (China))
# ('^N225', Nikkei 225 (Japan))
# ('EEM', MSCI (Emerging))
# ('^STOXX', STOXX 600 (Europe))

#######  Some Symbols   #######################################################

# ALSO ADD GROUPS BELOW AT END.

# Define toggleable datasets by symbol or group
dataset_inclusion = {

    'VOOG': True,               						# VOOG
    'QQQ': True,               						# QQQ                                              
    '^GSPC': True,               						# S&P 500                                                1.  
    '^IXIC': True,               						# NASDAQ                                               2.  
    '^DJI': True,                						# DJI                                                         3. 
    'all_stocks_in_stock_group': False,  			# Group: All Stocks                                  4.
    'global_indices_group': False,       			# Group: Global Indices                           5.
    'us_indices_group': False,           				# Group: U.S. Indices                                6.
    'reference_equities_group': False,   			# Group: Reference Equities                     7.
    'commodities_group': False,          			# Group: Commodities                               8.
    'real_estate_group': False,          				# Group: Real Estate                                  9.
    'BRK-A': True,               						# Berkshire - Class A                               10.  
    'EPD': False,                 						# Enterprise Products                              11.  
    'O': False,                   						# Realty Income                                        12.  
    'GC=F': False,                						# Gold Price (USD)                                    13.  
    'VNQ': False,                 						# Vngrd REIT-Proxy                                 14.  
    '000300.SS': False,           					# CSI 300 (China)                                       15.  
    '^N225': False,               						# Nikkei 225 (Japan)                                   16.  
    'EEM': False,                 						# MSCI (Emerging Markets)                       17.  
    '^STOXX': False               					# STOXX 600 (Europe)                               18.   
}

# MUST USE DECIMAL FRACTION.
# CANNOT USE DATETIME.
# Recessions FOLLOW the market drop typically….

recession_periods = [
    (1990.5, 1991.25),  # Early 1990s Recession: July 1990 – March 1991
    (2001, 2001.75),    # Early 2000s Recession: March 2001 – November 2001
    (2007.92, 2009.5),  # Great Recession: December 2007 – June 2009
    (2020.1, 2020.33)   # COVID-19 Recession: February 2020 – April 2020
]

# Function to calculate AAGR for a single symbol
def calculate_aagr(symbol):
    if symbol not in data or data[symbol].empty:
        return None

    stock_data = data[symbol].copy()

    # Handle MultiIndex columns
    if isinstance(stock_data.columns, pd.MultiIndex):
        stock_data.columns = stock_data.columns.get_level_values(0)

    # Group data by year
    yearly_data = stock_data.groupby(stock_data.index.year).agg({'Close': 'last'})
    
    # Calculate AAGR for each year from the start
    start_price = yearly_data['Close'].iloc[0]
    years = yearly_data.index - yearly_data.index[0] + 1  # Years since the start
    aagr = ((yearly_data['Close'] / start_price) ** (1 / years) - 1) * 100  # Convert to percentage

    # Reindex to match the full range of years
    aagr = aagr.reindex(range(start_year, end_year + 1), fill_value=np.nan)
    return aagr

# Function to calculate AAGR for a group of symbols
def calculate_group_aagr(group_symbols):
    group_aagr = pd.DataFrame()
    for symbol in group_symbols:
        aagr = calculate_aagr(symbol)
        if aagr is not None:
            group_aagr = pd.concat([group_aagr, aagr], axis=1)
    avg_aagr = group_aagr.mean(axis=1, skipna=True)
    return avg_aagr

# Plotting AAGR Graph
plt.figure(figsize=(15, 8))
plt.style.use('dark_background')

for symbol_or_group, include in dataset_inclusion.items():
    if not include:
        continue

# Setting Plot Line Widths and Solid/Dash

# Anything NOT referred to gets DASHED line.

    if symbol_or_group in data:  # Single Stock Symbols
        linestyle = "solid"
        linewidth = 1  # Single stocks: Solid, 1 pt   ( ABOVE )
    elif symbol_or_group == "all_stocks_in_stock_group":  
        linestyle = "solid"
        linewidth = 2  # ALL STOCKS Group: Solid, 2 pt  ( ABOVE )
    elif symbol_or_group in [
        "us_indices_group",
        "global_indices_group",
        "reference_equities_group",
        "commodities_group",
        "real_estate_group",
    ]:  # Custom Groups
        linestyle = "dashed"
        linewidth = 1  # Custom Groups: Dashed, 1 pt  ( ABOVE )

    # Handle individual stock data
    if symbol_or_group in data:
        aagr = calculate_aagr(symbol_or_group)
        plt.plot(
            aagr.index,
            aagr.values,
            label=symbol_info[symbol_or_group]["name"],
            color=symbol_info[symbol_or_group]["color"],
            linestyle=linestyle,
            linewidth=linewidth,
        )

# ADD GROUPS HERE TO BE HANDLED:  7 for Now

    elif symbol_or_group == "all_stocks_in_stock_group":
        aagr = calculate_group_aagr(all_stocks_in_stock_group)
        plt.plot(
            aagr.index,
            aagr.values,
            label="All Stocks",
            color=symbol_info["ALL_STOCKS"]["color"],
            linestyle=linestyle,
            linewidth=linewidth,
        )
    elif symbol_or_group == "global_indices_group":
        aagr = calculate_group_aagr(global_indices_group)
        plt.plot(
            aagr.index,
            aagr.values,
            label="Global Indices",
            color=symbol_info["GLOBAL_INDICES"]["color"],
            linestyle=linestyle,
            linewidth=linewidth,
        )
    elif symbol_or_group == "us_indices_group":
        aagr = calculate_group_aagr(us_indices_group)
        plt.plot(
            aagr.index,
            aagr.values,
            label="U.S. Indices",
            color=symbol_info["US_INDICES"]["color"],
            linestyle=linestyle,
            linewidth=linewidth,
        )
    elif symbol_or_group == "reference_equities_group":
        aagr = calculate_group_aagr(reference_equities_group)
        plt.plot(
            aagr.index,
            aagr.values,
            label="Reference Equities",
            color=symbol_info["REFERENCE_EQUITIES"]["color"],
            linestyle=linestyle,
            linewidth=linewidth,
        )
    elif symbol_or_group == "commodities_group":
        aagr = calculate_group_aagr(commodities_group)
        plt.plot(
            aagr.index,
            aagr.values,
            label="Commodities",
            color=symbol_info["COMMODITIES"]["color"],
            linestyle=linestyle,
            linewidth=linewidth,
        )
    elif symbol_or_group == "real_estate_group":
        aagr = calculate_group_aagr(real_estate_group)
        plt.plot(
            aagr.index,
            aagr.values,
            label="Real Estate",
            color=symbol_info["REAL_ESTATE"]["color"],
            linestyle=linestyle,
            linewidth=linewidth,
        )

# Right before recession shading section, add:
filtered_recession_periods = [
    (start, end) for start, end in recession_periods 
    if end >= start_date_obj.year and start <= end_date_obj.year
]

# Then modify the shading code:
for start, end in filtered_recession_periods:  # Changed from recession_periods
    plt.axvspan(
        start, end,
        color="red",
        alpha=0.2,
        edgecolor="red",
        linewidth=1
    )

# Add reference line, title, and legend
plt.axhline(y=0, color="white", linestyle="-", linewidth=1, alpha=0.3)
plt.title("AAGR Comparison: US Indices vs. Recession Resistant Stock Basket", size=14, pad=20)
plt.xlabel("Year", size=12)
plt.ylabel("AAGR (%)", size=12)
plt.grid(True, alpha=0.2)
plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
plt.xticks(ticks=range(start_date_obj.year, end_date_obj.year + 1, 2), rotation=45)
plt.tight_layout()
plt.show()


#-------------------------------------------------------------
# Annual GROWTH % Comparison Graph
#-------------------------------------------------------------

print("\n\n")

#######  Some Symbols   #######################################################

# 6 Custom GROUPS

# ('US_INDICES', U.S. Indices)
# ('GLOBAL_INDICES', Global Indices)
# ('ALL_STOCKS', All Stocks)
# ('REFERENCE_EQUITIES', Reference Equities)
# ('COMMODITIES', Commodities)
# ('REAL_ESTATE', Real Estate)

# 3 U.S Indices

# ('^GSPC', S&P 500)
# ('^IXIC', NASDAQ)
# ('^DJI', DJI)

# Single Stocks

# ('BRK-A', Berkshire - Class A)
# ('EPD', Enterprise Products)
# ('O', Realty Income)

# Commodities

# ('GC=F', Gold Price (USD))

# Real Estate

# ('VNQ', Vngrd REIT-Partial)

# 4 Global Indices

# ('000300.SS', CSI 300 (China))
# ('^N225', Nikkei 225 (Japan))
# ('EEM', MSCI (Emerging Markets))
# ('^STOXX', STOXX 600 (Europe))

#######  Some Symbols   #######################################################

# Function to calculate group growth for specified group
def calculate_group_growth(group_symbols):
    group_growth = pd.DataFrame()
    for symbol in group_symbols:
        growth = calculate_yearly_growth(symbol)  # Ensure calculate_yearly_growth is defined
        if not growth.empty:
            group_growth = pd.concat([group_growth, growth], axis=1)
    avg_growth = group_growth.mean(axis=1, skipna=True)
    return avg_growth.sort_index()

# Define toggleable datasets by symbol
dataset_inclusion = {


    'VOOG': True,               						# VOOG
    'QQQ': True,               						# QQQ                             
    '^GSPC': True,               						# S&P 500                                                1.  
    '^IXIC': True,               						# NASDAQ                                               2.  
    '^DJI': True,                						# DJI                                                         3. 
    'all_stocks_in_stock_group':  False,  			# Group: All Stocks                                  4.
    'global_indices_group': False,       			# Group: Global Indices                           5.
    'us_indices_group': False,           				# Group: U.S. Indices                                6.
    'reference_equities_group': False,   			# Group: Reference Equities                     7.
    'commodities_group': False,          			# Group: Commodities                               8.
    'real_estate_group': False,          				# Group: Real Estate                                  9.
    'BRK-A': True,               						# Berkshire - Class A                               10.  
    'EPD': False,                 						# Enterprise Products                              11.  
    'O': False,                   						# Realty Income                                        12.  
    'GC=F': False,                						# Gold Price (USD)                                    13.  
    'VNQ': False,                 						# Vngrd REIT-Proxy                                 14.  
    '000300.SS': False,           					# CSI 300 (China)                                       15.  
    '^N225': False,               						# Nikkei 225 (Japan)                                   16.  
    'EEM': False,                 						# MSCI (Emerging Markets)                       17.  
    '^STOXX': False               					# STOXX 600 (Europe)                               18.   
}

# Define Recessions.  
# MUST USE DECIMAL FRACTION.
# CANNOT USE DATETIME.
# Recessions FOLLOW the market drop typically….

recession_periods = [
    (1990.5, 1991.25),  # Early 1990s Recession: July 1990 – March 1991
    (2001, 2001.75),    # Early 2000s Recession: March 2001 – November 2001
    (2007.92, 2009.5),  # Great Recession: December 2007 – June 2009
    (2020.1, 2020.33)   # COVID-19 Recession: February 2020 – April 2020
]

# Plotting Section
plt.figure(figsize=(15, 8))
plt.style.use('dark_background')

for symbol_or_group, include in dataset_inclusion.items():
    if not include:
        continue

# Setting Plot Line Widths and Solid/Dash

# Anything NOT referred to gets DASHED line.

    if symbol_or_group in data:  # Single Stock Symbols
        linestyle = "solid"
        linewidth = 1  # Single stocks: Solid, 1 pt   ( ABOVE )
    elif symbol_or_group == "all_stocks_in_stock_group":  
        linestyle = "solid"
        linewidth = 2  # ALL STOCKS Group: Solid, 2 pt  ( ABOVE )
    elif symbol_or_group in [
        "us_indices_group",
        "global_indices_group",
        "reference_equities_group",
        "commodities_group",
        "real_estate_group",
    ]:  # Custom Groups
        linestyle = "dashed"
        linewidth = 1  # Custom Groups: Dashed, 1 pt  ( ABOVE )

    # Handle individual stock data
    if symbol_or_group in data:
        growth = calculate_yearly_growth(symbol_or_group)
        plt.plot(
            growth.index,
            growth.values,
            label=symbol_info[symbol_or_group]["name"],
            color=symbol_info[symbol_or_group]["color"],
            linestyle=linestyle,
            linewidth=linewidth,
        )

# ADD GROUPS HERE TO BE HANDLED:  6 for Now

    elif symbol_or_group == "all_stocks_in_stock_group":
        growth = calculate_group_growth(all_stocks_in_stock_group)
        plt.plot(
            growth.index,
            growth.values,
            label="All Stocks",
            color=symbol_info["ALL_STOCKS"]["color"],
            linestyle=linestyle,
            linewidth=linewidth,
        )
    elif symbol_or_group == "global_indices_group":
        growth = calculate_group_growth(global_indices_group)
        plt.plot(
            growth.index,
            growth.values,
            label="Global Indices",
            color=symbol_info["GLOBAL_INDICES"]["color"],
            linestyle=linestyle,
            linewidth=linewidth,
        )
    elif symbol_or_group == "us_indices_group":
        growth = calculate_group_growth(us_indices_group)
        plt.plot(
            growth.index,
            growth.values,
            label="U.S. Indices",
            color=symbol_info["US_INDICES"]["color"],
            linestyle=linestyle,
            linewidth=linewidth,
        )
    elif symbol_or_group == "reference_equities_group":
        growth = calculate_group_growth(reference_equities_group)
        plt.plot(
            growth.index,
            growth.values,
            label="Reference Equities",
            color=symbol_info["REFERENCE_EQUITIES"]["color"],
            linestyle=linestyle,
            linewidth=linewidth,
        )
    elif symbol_or_group == "commodities_group":
        growth = calculate_group_growth(commodities_group)
        plt.plot(
            growth.index,
            growth.values,
            label="Commodities",
            color=symbol_info["COMMODITIES"]["color"],
            linestyle=linestyle,
            linewidth=linewidth,
        )
    elif symbol_or_group == "real_estate_group":
        growth = calculate_group_growth(real_estate_group)
        plt.plot(
            growth.index,
            growth.values,
            label="Real Estate",
            color=symbol_info["REAL_ESTATE"]["color"],
            linestyle=linestyle,
            linewidth=linewidth,
        )

# Right before recession shading section, add:
filtered_recession_periods = [
    (start, end) for start, end in recession_periods 
    if end >= start_date_obj.year and start <= end_date_obj.year
]

# Then modify the shading code:
for start, end in filtered_recession_periods:  # Changed from recession_periods
    plt.axvspan(
        start, end,
        color="red",
        alpha=0.2,
        edgecolor="red",
        linewidth=1
    )

# Add reference line, title, and legend
plt.axhline(y=0, color="white", linestyle="-", linewidth=1, alpha=0.3)
plt.title("Annual % Growth Rate Comparison: US Indices vs. Recession Resistant Stock Basket", size=14, pad=20)
plt.xlabel("Year", size=12)
plt.ylabel("Annual Growth Rate (%)", size=12)
plt.grid(True, alpha=0.2)
plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
plt.xticks(ticks=range(start_date_obj.year, end_date_obj.year + 1, 2), rotation=45)
plt.tight_layout()
plt.show()

#-------------------------------------------------------------
# US Indices  Avg  vs. Global Indices Avg
#-------------------------------------------------------------

print("\n\n")

#######  Some Symbols   #######################################################

# 6 Custom GROUPS

# ('US_INDICES', U.S. Indices)
# ('GLOBAL_INDICES', Global Indices)
# ('ALL_STOCKS', All Stocks)
# ('REFERENCE_EQUITIES', Reference Equities)
# ('COMMODITIES', Commodities)
# ('REAL_ESTATE', Real Estate)

# 3 U.S Indices

# ('^GSPC', S&P 500)
# ('^IXIC', NASDAQ)
# ('^DJI', DJI)

# Single Stocks

# ('BRK-A', Berkshire - Class A)
# ('EPD', Enterprise Products)
# ('O', Realty Income)

# Commodities

# ('GC=F', Gold Price (USD))

# Real Estate

# ('VNQ', Vngrd REIT-Partial)

# 4 Global Indices

# ('000300.SS', CSI 300 (China))
# ('^N225', Nikkei 225 (Japan))
# ('EEM', MSCI (Emerging Markets))
# ('^STOXX', STOXX 600 (Europe))

#######  Some Symbols   #######################################################

# Function to calculate group growth for specified group
def calculate_group_growth(group_symbols):
    group_growth = pd.DataFrame()
    for symbol in group_symbols:
        growth = calculate_yearly_growth(symbol)  # Ensure calculate_yearly_growth is defined
        if not growth.empty:
            group_growth = pd.concat([group_growth, growth], axis=1)
    avg_growth = group_growth.mean(axis=1, skipna=True)
    return avg_growth.sort_index()

# Define toggleable datasets by symbol
dataset_inclusion = {
    '^GSPC': False,               					# S&P 500                                                1.  
    '^IXIC': False,               						# NASDAQ                                               2.  
    '^DJI': False,                						# DJI                                                         3. 
    'all_stocks_in_stock_group': False,  			# Group: All Stocks                                  4.
    'global_indices_group': True,       				# Group: Global Indices                           5.
    'us_indices_group': True,           				# Group: U.S. Indices                                6.
    'reference_equities_group': False,   			# Group: Reference Equities                     7.
    'commodities_group': False,          			# Group: Commodities                               8.
    'real_estate_group': False,          				# Group: Real Estate                                  9.
    'BRK-A': False,               						# Berkshire - Class A                               10.  
    'EPD': False,                 						# Enterprise Products                              11.  
    'O': False,                   						# Realty Income                                        12.  
    'GC=F': False,                						# Gold Price (USD)                                    13.  
    'VNQ': False,                 						# Vngrd REIT-Proxy                                 14.  
    '000300.SS': False,           					# CSI 300 (China)                                       15.  
    '^N225': False,               						# Nikkei 225 (Japan)                                   16.  
    'EEM': False,                 						# MSCI (Emerging Markets)                       17.  
    '^STOXX': False               					# STOXX 600 (Europe)                               18.  
}

# MUST USE DECIMAL FRACTION.
# CANNOT USE DATETIME.
# Recessions FOLLOW the market drop typically….

recession_periods = [
    (1990.5, 1991.25),  # Early 1990s Recession: July 1990 – March 1991
    (2001, 2001.75),    # Early 2000s Recession: March 2001 – November 2001
    (2007.92, 2009.5),  # Great Recession: December 2007 – June 2009
    (2020.1, 2020.33)   # COVID-19 Recession: February 2020 – April 2020
]

# Plotting Section
plt.figure(figsize=(15, 8))
plt.style.use('dark_background')

for symbol_or_group, include in dataset_inclusion.items():
    if not include:
        continue

# Setting Plot Line Widths and Solid/Dash

# Anything NOT referred to gets DASHED line.

    if symbol_or_group in data:  # Single Stock Symbols
        linestyle = "solid"
        linewidth = 1  # Single stocks: Solid, 1 pt   ( ABOVE )
    elif symbol_or_group == "all_stocks_in_stock_group":  
        linestyle = "solid"
        linewidth = 2  # ALL STOCKS Group: Solid, 2 pt  ( ABOVE )
    elif symbol_or_group in [
        "us_indices_group",
        "global_indices_group",
        "reference_equities_group",
        "commodities_group",
        "real_estate_group",
    ]:  # Custom Groups
        linestyle = "dashed"
        linewidth = 1  # Custom Groups: Dashed, 1 pt  ( ABOVE )

    # Handle individual stock data
    if symbol_or_group in data:
        growth = calculate_yearly_growth(symbol_or_group)
        plt.plot(
            growth.index,
            growth.values,
            label=symbol_info[symbol_or_group]["name"],
            color=symbol_info[symbol_or_group]["color"],
            linestyle=linestyle,
            linewidth=linewidth,
        )

# ADD GROUPS HERE TO BE HANDLED:  6 for Now

    elif symbol_or_group == "all_stocks_in_stock_group":
        growth = calculate_group_growth(all_stocks_in_stock_group)
        plt.plot(
            growth.index,
            growth.values,
            label="All Stocks",
            color=symbol_info["ALL_STOCKS"]["color"],
            linestyle=linestyle,
            linewidth=linewidth,
        )
    elif symbol_or_group == "global_indices_group":
        growth = calculate_group_growth(global_indices_group)
        plt.plot(
            growth.index,
            growth.values,
            label="Global Indices",
            color=symbol_info["GLOBAL_INDICES"]["color"],
            linestyle=linestyle,
            linewidth=linewidth,
        )
    elif symbol_or_group == "us_indices_group":
        growth = calculate_group_growth(us_indices_group)
        plt.plot(
            growth.index,
            growth.values,
            label="U.S. Indices",
            color=symbol_info["US_INDICES"]["color"],
            linestyle=linestyle,
            linewidth=linewidth,
        )
    elif symbol_or_group == "reference_equities_group":
        growth = calculate_group_growth(reference_equities_group)
        plt.plot(
            growth.index,
            growth.values,
            label="Reference Equities",
            color=symbol_info["REFERENCE_EQUITIES"]["color"],
            linestyle=linestyle,
            linewidth=linewidth,
        )
    elif symbol_or_group == "commodities_group":
        growth = calculate_group_growth(commodities_group)
        plt.plot(
            growth.index,
            growth.values,
            label="Commodities",
            color=symbol_info["COMMODITIES"]["color"],
            linestyle=linestyle,
            linewidth=linewidth,
        )
    elif symbol_or_group == "real_estate_group":
        growth = calculate_group_growth(real_estate_group)
        plt.plot(
            growth.index,
            growth.values,
            label="Real Estate",
            color=symbol_info["REAL_ESTATE"]["color"],
            linestyle=linestyle,
            linewidth=linewidth,
        )

# Right before recession shading section, add:
filtered_recession_periods = [
    (start, end) for start, end in recession_periods 
    if end >= start_date_obj.year and start <= end_date_obj.year
]

# Then modify the shading code:
for start, end in filtered_recession_periods:  # Changed from recession_periods
    plt.axvspan(
        start, end,
        color="red",
        alpha=0.2,
        edgecolor="red",
        linewidth=1
    )

# Add reference line, title, and legend
plt.axhline(y=0, color="white", linestyle="-", linewidth=1, alpha=0.3)
plt.title("US Indices  Avg  vs. Global Indices Avg", size=14, pad=20)
plt.xlabel("Year", size=12)
plt.ylabel("Annual Growth Rate (%)", size=12)
plt.grid(True, alpha=0.2)
plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
plt.xticks(ticks=range(start_date_obj.year, end_date_obj.year + 1, 2), rotation=45)
plt.tight_layout()
plt.show()

#-------------------------------------------------------------
# US Indices  vs. Global Indices
#-------------------------------------------------------------

print("\n\n")

#######  Some Symbols   #######################################################

# 6 Custom GROUPS

# ('US_INDICES', U.S. Indices)
# ('GLOBAL_INDICES', Global Indices)
# ('ALL_STOCKS', All Stocks)
# ('REFERENCE_EQUITIES', Reference Equities)
# ('COMMODITIES', Commodities)
# ('REAL_ESTATE', Real Estate)

# 3 U.S Indices

# ('^GSPC', S&P 500)
# ('^IXIC', NASDAQ)
# ('^DJI', DJI)

# Single Stocks

# ('BRK-A', Berkshire - Class A)
# ('EPD', Enterprise Products)
# ('O', Realty Income)

# Commodities

# ('GC=F', Gold Price (USD))

# Real Estate

# ('VNQ', Vngrd REIT-Partial)

# 4 Global Indices

# ('000300.SS', CSI 300 (China))
# ('^N225', Nikkei 225 (Japan))
# ('EEM', MSCI (Emerging Markets))
# ('^STOXX', STOXX 600 (Europe))

#######  Some Symbols   #######################################################

# Function to calculate group growth for specified group
def calculate_group_growth(group_symbols):
    group_growth = pd.DataFrame()
    for symbol in group_symbols:
        growth = calculate_yearly_growth(symbol)  # Ensure calculate_yearly_growth is defined
        if not growth.empty:
            group_growth = pd.concat([group_growth, growth], axis=1)
    avg_growth = group_growth.mean(axis=1, skipna=True)
    return avg_growth.sort_index()

# Define toggleable datasets by symbol
dataset_inclusion = {
    '^GSPC': True,               					  	# S&P 500                                                1.  
    '^IXIC': True,               						# NASDAQ                                               2.  
    '^DJI': True,                						# DJI                                                         3. 
    'all_stocks_in_stock_group': False,  			# Group: All Stocks                                  4.
    'global_indices_group': False,       			# Group: Global Indices                           5.
    'us_indices_group': False,           				# Group: U.S. Indices                                6.
    'reference_equities_group': False,   			# Group: Reference Equities                     7.
    'commodities_group': False,          			# Group: Commodities                               8.
    'real_estate_group': False,          				# Group: Real Estate                                  9.
    'BRK-A': False,               						# Berkshire - Class A                               10.  
    'EPD': False,                 						# Enterprise Products                              11.  
    'O': False,                   						# Realty Income                                        12.  
    'GC=F': False,                						# Gold Price (USD)                                    13.  
    'VNQ': False,                 						# Vngrd REIT-Proxy                                 14.  
    '000300.SS': True,           					# CSI 300 (China)                                       15.  
    '^N225': True,               						# Nikkei 225 (Japan)                                   16.  
    'EEM': True,                 						# MSCI (Emerging Markets)                       17.  
    '^STOXX': True               					# STOXX 600 (Europe)                               18.  
}

# MUST USE DECIMAL FRACTION.
# CANNOT USE DATETIME.
# Recessions FOLLOW the market drop typically….

recession_periods = [
    (1990.5, 1991.25),  # Early 1990s Recession: July 1990 – March 1991
    (2001, 2001.75),    # Early 2000s Recession: March 2001 – November 2001
    (2007.92, 2009.5),  # Great Recession: December 2007 – June 2009
    (2020.1, 2020.33)   # COVID-19 Recession: February 2020 – April 2020
]

# Plotting Section
plt.figure(figsize=(15, 8))
plt.style.use('dark_background')

for symbol_or_group, include in dataset_inclusion.items():
    if not include:
        continue

# Setting Plot Line Widths and Solid/Dash

# Anything NOT referred to gets DASHED line.

    if symbol_or_group in data:  # Single Stock Symbols
        linestyle = "solid"
        linewidth = 1  # Single stocks: Solid, 1 pt   ( ABOVE )
    elif symbol_or_group == "all_stocks_in_stock_group":  
        linestyle = "solid"
        linewidth = 2  # ALL STOCKS Group: Solid, 2 pt  ( ABOVE )
    elif symbol_or_group in [
        "us_indices_group",
        "global_indices_group",
        "reference_equities_group",
        "commodities_group",
        "real_estate_group",
    ]:  # Custom Groups
        linestyle = "dashed"
        linewidth = 1  # Custom Groups: Dashed, 1 pt  ( ABOVE )

    # Handle individual stock data
    if symbol_or_group in data:
        growth = calculate_yearly_growth(symbol_or_group)
        plt.plot(
            growth.index,
            growth.values,
            label=symbol_info[symbol_or_group]["name"],
            color=symbol_info[symbol_or_group]["color"],
            linestyle=linestyle,
            linewidth=linewidth,
        )

# ADD GROUPS HERE TO BE HANDLED:  6 for Now

    elif symbol_or_group == "all_stocks_in_stock_group":
        growth = calculate_group_growth(all_stocks_in_stock_group)
        plt.plot(
            growth.index,
            growth.values,
            label="All Stocks",
            color=symbol_info["ALL_STOCKS"]["color"],
            linestyle=linestyle,
            linewidth=linewidth,
        )
    elif symbol_or_group == "global_indices_group":
        growth = calculate_group_growth(global_indices_group)
        plt.plot(
            growth.index,
            growth.values,
            label="Global Indices",
            color=symbol_info["GLOBAL_INDICES"]["color"],
            linestyle=linestyle,
            linewidth=linewidth,
        )
    elif symbol_or_group == "us_indices_group":
        growth = calculate_group_growth(us_indices_group)
        plt.plot(
            growth.index,
            growth.values,
            label="U.S. Indices",
            color=symbol_info["US_INDICES"]["color"],
            linestyle=linestyle,
            linewidth=linewidth,
        )
    elif symbol_or_group == "reference_equities_group":
        growth = calculate_group_growth(reference_equities_group)
        plt.plot(
            growth.index,
            growth.values,
            label="Reference Equities",
            color=symbol_info["REFERENCE_EQUITIES"]["color"],
            linestyle=linestyle,
            linewidth=linewidth,
        )
    elif symbol_or_group == "commodities_group":
        growth = calculate_group_growth(commodities_group)
        plt.plot(
            growth.index,
            growth.values,
            label="Commodities",
            color=symbol_info["COMMODITIES"]["color"],
            linestyle=linestyle,
            linewidth=linewidth,
        )
    elif symbol_or_group == "real_estate_group":
        growth = calculate_group_growth(real_estate_group)
        plt.plot(
            growth.index,
            growth.values,
            label="Real Estate",
            color=symbol_info["REAL_ESTATE"]["color"],
            linestyle=linestyle,
            linewidth=linewidth,
        )

# Right before recession shading section, add:
filtered_recession_periods = [
    (start, end) for start, end in recession_periods 
    if end >= start_date_obj.year and start <= end_date_obj.year
]

# Then modify the shading code:
for start, end in filtered_recession_periods:  # Changed from recession_periods
    plt.axvspan(
        start, end,
        color="red",
        alpha=0.2,
        edgecolor="red",
        linewidth=1
    )

# Add reference line, title, and legend
plt.axhline(y=0, color="white", linestyle="-", linewidth=1, alpha=0.3)
plt.title("US Indices  vs. Global Indices", size=14, pad=20)
plt.xlabel("Year", size=12)
plt.ylabel("Annual Growth Rate (%)", size=12)
plt.grid(True, alpha=0.2)
plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
plt.xticks(ticks=range(start_date_obj.year, end_date_obj.year + 1, 2), rotation=45)
plt.tight_layout()
plt.show()

#-------------------------------------------------------------
# US Indices vs. Gold
#-------------------------------------------------------------

print("\n\n")

#######  Some Symbols   #######################################################

# 6 Custom GROUPS

# ('US_INDICES', U.S. Indices)
# ('GLOBAL_INDICES', Global Indices)
# ('ALL_STOCKS', All Stocks)
# ('REFERENCE_EQUITIES', Reference Equities)
# ('COMMODITIES', Commodities)
# ('REAL_ESTATE', Real Estate)

# 3 U.S Indices

# ('^GSPC', S&P 500)
# ('^IXIC', NASDAQ)
# ('^DJI', DJI)

# Single Stocks

# ('BRK-A', Berkshire - Class A)
# ('EPD', Enterprise Products)
# ('O', Realty Income)

# Commodities

# ('GC=F', Gold Price (USD))

# Real Estate

# ('VNQ', Vngrd REIT-Partial)

# 4 Global Indices

# ('000300.SS', CSI 300 (China))
# ('^N225', Nikkei 225 (Japan))
# ('EEM', MSCI (Emerging Markets))
# ('^STOXX', STOXX 600 (Europe))

#######  Some Symbols   #######################################################

# Function to calculate group growth for specified group
def calculate_group_growth(group_symbols):
    group_growth = pd.DataFrame()
    for symbol in group_symbols:
        growth = calculate_yearly_growth(symbol)  # Ensure calculate_yearly_growth is defined
        if not growth.empty:
            group_growth = pd.concat([group_growth, growth], axis=1)
    avg_growth = group_growth.mean(axis=1, skipna=True)
    return avg_growth.sort_index()

# Define toggleable datasets by symbol
dataset_inclusion = {
    '^GSPC': False,               					# S&P 500                                                1.  
    '^IXIC': False,               						# NASDAQ                                               2.  
    '^DJI': False,                						# DJI                                                         3. 
    'all_stocks_in_stock_group': False,  			# Group: All Stocks                                  4.
    'global_indices_group': False,       			# Group: Global Indices                           5.
    'us_indices_group': True,           				# Group: U.S. Indices                                6.
    'reference_equities_group': False,   			# Group: Reference Equities                     7.
    'commodities_group': False,          			# Group: Commodities                               8.
    'real_estate_group': False,          				# Group: Real Estate                                  9.
    'BRK-A': False,               						# Berkshire - Class A                               10.  
    'EPD': False,                 						# Enterprise Products                              11.  
    'O': False,                   						# Realty Income                                        12.  
    'GC=F': True,                						# Gold Price (USD)                                    13.  
    'VNQ': False,                 						# Vngrd REIT-Proxy                                 14.  
    '000300.SS': False,           					# CSI 300 (China)                                       15.  
    '^N225': False,               						# Nikkei 225 (Japan)                                   16.  
    'EEM': False,                 						# MSCI (Emerging Markets)                       17.  
    '^STOXX': False               					# STOXX 600 (Europe)                               18.  
}

# MUST USE DECIMAL FRACTION.
# CANNOT USE DATETIME.
# Recessions FOLLOW the market drop typically….

recession_periods = [
    (1990.5, 1991.25),  # Early 1990s Recession: July 1990 – March 1991
    (2001, 2001.75),    # Early 2000s Recession: March 2001 – November 2001
    (2007.92, 2009.5),  # Great Recession: December 2007 – June 2009
    (2020.1, 2020.33)   # COVID-19 Recession: February 2020 – April 2020
]

# Plotting Section
plt.figure(figsize=(15, 8))
plt.style.use('dark_background')

for symbol_or_group, include in dataset_inclusion.items():
    if not include:
        continue

# Setting Plot Line Widths and Solid/Dash

# Anything NOT referred to gets DASHED line.

    if symbol_or_group in data:  # Single Stock Symbols
        linestyle = "solid"
        linewidth = 1  # Single stocks: Solid, 1 pt   ( ABOVE )
    elif symbol_or_group == "all_stocks_in_stock_group":  
        linestyle = "solid"
        linewidth = 2  # ALL STOCKS Group: Solid, 2 pt  ( ABOVE )
    elif symbol_or_group in [
        "us_indices_group",
        "global_indices_group",
        "reference_equities_group",
        "commodities_group",
        "real_estate_group",
    ]:  # Custom Groups
        linestyle = "dashed"
        linewidth = 1  # Custom Groups: Dashed, 1 pt  ( ABOVE )

    # Handle individual stock data
    if symbol_or_group in data:
        growth = calculate_yearly_growth(symbol_or_group)
        plt.plot(
            growth.index,
            growth.values,
            label=symbol_info[symbol_or_group]["name"],
            color=symbol_info[symbol_or_group]["color"],
            linestyle=linestyle,
            linewidth=linewidth,
        )

# ADD GROUPS HERE TO BE HANDLED:  6 for Now

    elif symbol_or_group == "all_stocks_in_stock_group":
        growth = calculate_group_growth(all_stocks_in_stock_group)
        plt.plot(
            growth.index,
            growth.values,
            label="All Stocks",
            color=symbol_info["ALL_STOCKS"]["color"],
            linestyle=linestyle,
            linewidth=linewidth,
        )
    elif symbol_or_group == "global_indices_group":
        growth = calculate_group_growth(global_indices_group)
        plt.plot(
            growth.index,
            growth.values,
            label="Global Indices",
            color=symbol_info["GLOBAL_INDICES"]["color"],
            linestyle=linestyle,
            linewidth=linewidth,
        )
    elif symbol_or_group == "us_indices_group":
        growth = calculate_group_growth(us_indices_group)
        plt.plot(
            growth.index,
            growth.values,
            label="U.S. Indices",
            color=symbol_info["US_INDICES"]["color"],
            linestyle=linestyle,
            linewidth=linewidth,
        )
    elif symbol_or_group == "reference_equities_group":
        growth = calculate_group_growth(reference_equities_group)
        plt.plot(
            growth.index,
            growth.values,
            label="Reference Equities",
            color=symbol_info["REFERENCE_EQUITIES"]["color"],
            linestyle=linestyle,
            linewidth=linewidth,
        )
    elif symbol_or_group == "commodities_group":
        growth = calculate_group_growth(commodities_group)
        plt.plot(
            growth.index,
            growth.values,
            label="Commodities",
            color=symbol_info["COMMODITIES"]["color"],
            linestyle=linestyle,
            linewidth=linewidth,
        )
    elif symbol_or_group == "real_estate_group":
        growth = calculate_group_growth(real_estate_group)
        plt.plot(
            growth.index,
            growth.values,
            label="Real Estate",
            color=symbol_info["REAL_ESTATE"]["color"],
            linestyle=linestyle,
            linewidth=linewidth,
        )

# Right before recession shading section, add:
filtered_recession_periods = [
    (start, end) for start, end in recession_periods 
    if end >= start_date_obj.year and start <= end_date_obj.year
]

# Then modify the shading code:
for start, end in filtered_recession_periods:  # Changed from recession_periods
    plt.axvspan(
        start, end,
        color="red",
        alpha=0.2,
        edgecolor="red",
        linewidth=1
    )

# Add reference line, title, and legend
plt.axhline(y=0, color="white", linestyle="-", linewidth=1, alpha=0.3)
plt.title("US Indices vs. Gold  [ Gold Futures Contract ]", size=14, pad=20)
plt.xlabel("Year", size=12)
plt.ylabel("Annual Growth Rate (%)", size=12)
plt.grid(True, alpha=0.2)
plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
plt.xticks(ticks=range(start_date_obj.year, end_date_obj.year + 1, 2), rotation=45)
plt.tight_layout()
plt.show()

#-------------------------------------------------------------
# US Indices vs. Real Estate Proxy
#-------------------------------------------------------------

print("\n\n")

#######  Some Symbols   #######################################################

# 6 Custom GROUPS

# ('US_INDICES', U.S. Indices)
# ('GLOBAL_INDICES', Global Indices)
# ('ALL_STOCKS', All Stocks)
# ('REFERENCE_EQUITIES', Reference Equities)
# ('COMMODITIES', Commodities)
# ('REAL_ESTATE', Real Estate)

# 3 U.S Indices

# ('^GSPC', S&P 500)
# ('^IXIC', NASDAQ)
# ('^DJI', DJI)

# Single Stocks

# ('BRK-A', Berkshire - Class A)
# ('EPD', Enterprise Products)
# ('O', Realty Income)

# Commodities

# ('GC=F', Gold Price (USD))

# Real Estate

# ('VNQ', Vngrd REIT-Partial)

# 4 Global Indices

# ('000300.SS', CSI 300 (China))
# ('^N225', Nikkei 225 (Japan))
# ('EEM', MSCI (Emerging Markets))
# ('^STOXX', STOXX 600 (Europe))

#######  Some Symbols   #######################################################

# Function to calculate group growth for specified group
def calculate_group_growth(group_symbols):
    group_growth = pd.DataFrame()
    for symbol in group_symbols:
        growth = calculate_yearly_growth(symbol)  # Ensure calculate_yearly_growth is defined
        if not growth.empty:
            group_growth = pd.concat([group_growth, growth], axis=1)
    avg_growth = group_growth.mean(axis=1, skipna=True)
    return avg_growth.sort_index()

# Define toggleable datasets by symbol
dataset_inclusion = {
    '^GSPC': False,               					# S&P 500                                                1.  
    '^IXIC': False,               						# NASDAQ                                               2.  
    '^DJI': False,                						# DJI                                                         3.  
    'all_stocks_in_stock_group': False,  			# Group: All Stocks                                  4.
    'global_indices_group': False,       			# Group: Global Indices                           5.
    'us_indices_group': True,           				# Group: U.S. Indices                                6.
    'reference_equities_group': False,   			# Group: Reference Equities                     7.
    'commodities_group': False,          			# Group: Commodities                               8.
    'real_estate_group': True,          				# Group: Real Estate                                  9.
    'BRK-A': False,               						# Berkshire - Class A                               10.  
    'EPD': False,                 						# Enterprise Products                              11.  
    'O': False,                   						# Realty Income                                        12.  
    'GC=F': False,                						# Gold Price (USD)                                    13.  
    'VNQ': False,                 						# Vngrd REIT-Proxy                                 14.  
    '000300.SS': False,           					# CSI 300 (China)                                       15.  
    '^N225': False,               						# Nikkei 225 (Japan)                                   16.  
    'EEM': False,                 						# MSCI (Emerging Markets)                       17.  
    '^STOXX': False               					# STOXX 600 (Europe)                               18.  
}

# MUST USE DECIMAL FRACTION.
# CANNOT USE DATETIME.
# Recessions FOLLOW the market drop typically….

recession_periods = [
    (1990.5, 1991.25),  # Early 1990s Recession: July 1990 – March 1991
    (2001, 2001.75),    # Early 2000s Recession: March 2001 – November 2001
    (2007.92, 2009.5),  # Great Recession: December 2007 – June 2009
    (2020.1, 2020.33)   # COVID-19 Recession: February 2020 – April 2020
]

# Plotting Section
plt.figure(figsize=(15, 8))
plt.style.use('dark_background')

for symbol_or_group, include in dataset_inclusion.items():
    if not include:
        continue

# Setting Plot Line Widths and Solid/Dash

# Anything NOT referred to gets DASHED line.

    if symbol_or_group in data:  # Single Stock Symbols
        linestyle = "solid"
        linewidth = 1  # Single stocks: Solid, 1 pt   ( ABOVE )
    elif symbol_or_group == "all_stocks_in_stock_group":  
        linestyle = "solid"
        linewidth = 2  # ALL STOCKS Group: Solid, 2 pt  ( ABOVE )
    elif symbol_or_group in [
        "us_indices_group",
        "global_indices_group",
        "reference_equities_group",
        "commodities_group",
        "real_estate_group",
    ]:  # Custom Groups
        linestyle = "dashed"
        linewidth = 1  # Custom Groups: Dashed, 1 pt  ( ABOVE )

    # Handle individual stock data
    if symbol_or_group in data:
        growth = calculate_yearly_growth(symbol_or_group)
        plt.plot(
            growth.index,
            growth.values,
            label=symbol_info[symbol_or_group]["name"],
            color=symbol_info[symbol_or_group]["color"],
            linestyle=linestyle,
            linewidth=linewidth,
        )

# ADD GROUPS HERE TO BE HANDLED:  6 for Now

    elif symbol_or_group == "all_stocks_in_stock_group":
        growth = calculate_group_growth(all_stocks_in_stock_group)
        plt.plot(
            growth.index,
            growth.values,
            label="All Stocks",
            color=symbol_info["ALL_STOCKS"]["color"],
            linestyle=linestyle,
            linewidth=linewidth,
        )
    elif symbol_or_group == "global_indices_group":
        growth = calculate_group_growth(global_indices_group)
        plt.plot(
            growth.index,
            growth.values,
            label="Global Indices",
            color=symbol_info["GLOBAL_INDICES"]["color"],
            linestyle=linestyle,
            linewidth=linewidth,
        )
    elif symbol_or_group == "us_indices_group":
        growth = calculate_group_growth(us_indices_group)
        plt.plot(
            growth.index,
            growth.values,
            label="U.S. Indices",
            color=symbol_info["US_INDICES"]["color"],
            linestyle=linestyle,
            linewidth=linewidth,
        )
    elif symbol_or_group == "reference_equities_group":
        growth = calculate_group_growth(reference_equities_group)
        plt.plot(
            growth.index,
            growth.values,
            label="Reference Equities",
            color=symbol_info["REFERENCE_EQUITIES"]["color"],
            linestyle=linestyle,
            linewidth=linewidth,
        )
    elif symbol_or_group == "commodities_group":
        growth = calculate_group_growth(commodities_group)
        plt.plot(
            growth.index,
            growth.values,
            label="Commodities",
            color=symbol_info["COMMODITIES"]["color"],
            linestyle=linestyle,
            linewidth=linewidth,
        )
    elif symbol_or_group == "real_estate_group":
        growth = calculate_group_growth(real_estate_group)
        plt.plot(
            growth.index,
            growth.values,
            label="Real Estate",
            color=symbol_info["REAL_ESTATE"]["color"],
            linestyle=linestyle,
            linewidth=linewidth,
        )

# Right before recession shading section, add:
filtered_recession_periods = [
    (start, end) for start, end in recession_periods 
    if end >= start_date_obj.year and start <= end_date_obj.year
]

# Then modify the shading code:
for start, end in filtered_recession_periods:  # Changed from recession_periods
    plt.axvspan(
        start, end,
        color="red",
        alpha=0.2,
        edgecolor="red",
        linewidth=1
    )

# Add reference line, title, and legend
plt.axhline(y=0, color="white", linestyle="-", linewidth=1, alpha=0.3)
plt.title("US Indices vs. Real Estate PROXY [ Vngrd REIT ]", size=14, pad=20)
plt.xlabel("Year", size=12)
plt.ylabel("Annual Growth Rate (%)", size=12)
plt.grid(True, alpha=0.2)
plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
plt.xticks(ticks=range(start_date_obj.year, end_date_obj.year + 1, 2), rotation=45)
plt.tight_layout()
plt.show()


#==================================================================================================
#                                              SUMAMRY END
#==================================================================================================

# Analysis SUMMARY End.  (phew. all done!)

print('=' * 100)
print("\n\033[1mAnalysis Summary:\033[0m")  # Bold text for "Analysis Summary"

# Dynamically use the start and end dates
analysis_start_year = start_date_obj.year
analysis_end_year = end_date_obj.year
total_years_in_period = analysis_end_year - analysis_start_year + 1  # Inclusive count of years

print(f"Total symbols analyzed: {len(symbol_info) - 6}")  # Subtracting the 6 custom groups not directly analyzed
print(f"Analysis period: {analysis_start_year} to {analysis_end_year}")
print(f"# of Years in Period: {total_years_in_period}")
print('=' * 100)





