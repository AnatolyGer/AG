from binance.client import Client
from binance.enums import *
from binance_api import Binance     # bot
import source5 as src
# Работа со временем
import time
import datetime as dt
# Работа с вычислениями
import math
#######################################################

BINANCE_API = '9UD74nMGt7MK1Ar2awpNqeRh5R0fP2AeMfd9obImCoZwu6DPYGho30oPwSlqVlXt'
BINANCE_SECRET = 'nWQonlvsNw0hKGMuzTSRN0hLWt5S2nbIqw7QV6PA0ZRtpCu6ctjHTcFFCXIAJT7M'
botR = Binance( API_KEY=BINANCE_API, API_SECRET=BINANCE_SECRET)
# for real trading and prices
clientR = Client(BINANCE_API, BINANCE_SECRET)
SOCKET = "wss://stream.binance.com:9443/ws/busdusdt@kline_1m"  #  котировки с реального счета
#SOCKET = "wss://stream.binance.com:9443/ws/busdusdt@kline_1m"  #  котировки с реального счета
# for testnet trading -----------------------------------------------------------------------  менять  !!!!!!!!!
TEST_BINANCE_API = 'lueE5N8CXAfcCByFaYPebvqtaLYqQwmcS3MhLRKdtunOqBr2WkKgJb4Sxm32JWtr'
TEST_BINANCE_SECRET = 'pmjbtHJWW2HwzweQnNQ7Qos8ZIHQXPjTsUa21FcKobGDq6SGDNwhoKKFvVnl6GWx'
botT = Binance( API_KEY=TEST_BINANCE_API, API_SECRET=TEST_BINANCE_SECRET)
test_client = Client(TEST_BINANCE_API, TEST_BINANCE_SECRET)
test_client.API_URL = 'https://testnet.binance.vision/api'
test_socket = "wss://testnet.binance.vision/ws/busdusdt@kline_1m"

# global variables =========================================================================
BASE = 'BUSD'                           #def= "BNB" -БАЗОВАЯ КРИПТОВАЛЮТА
QUOTE = "USDT"                          #                      -КВОТИРУЕМАЯ
SYMBOL = BASE+QUOTE
ASSET = SYMBOL

MIN_LOT = 10.0    # 10.01
NstepSize = 1
                    #TickSize = 0.01             # stepSize
STRATEGY = 5         # def=пробой волатильности   1-ALEX1   2-ALEXbuy  3- ALEX(buy/sell) 4 - com4 5- com5
TEST = False         # False - РЕАЛЬНЫЙ ACCOUNT
R_T = 'REAL'         # TEST - order={}  'REAL' order={dict}
TORG = True          # разрешение ТОРГА

START_SIDE = 'sell'
START_bb = 0.0
START_bq = 0.0

BALANCE_T_BASE = 0.0           # кол-во монет базовой криптовалюты на  TECT счете
BALANCE_T_QUOTE = 0.0          # кол-во монет квотируемой валюты на  TECT счете
BALANCE_BASE = 0.0           # кол-во монет базовой криптовалюты на счете
PRE_BB = 2
BALANCE_QUOTE = 0.0          # кол-во монет квотируемой валюты
PRE_BQ = 2              # точность 2-знака после .

MY_SIDE = 'sell'
CUR_SIDE = 'none'
CUR_PRICE = 0.0              # текущая цена  открытия ордера LIMIT_MAKER
Dask = 0.0001         #  дельта анализа цены для выбора направления позиции
Dbid = 0.0001         #   AVG_PRICE - Dbid
AVG_PRICE = 1.0       # BUSDUSDT=1.0
DLIM_PRICE = 0.0000   # дельта отклонения LIM oт MARKET

INF = 'alert '               # уровень отображения информации
OLD_VALUE = ''
TIME = ' '
TIME_LIMIT = ' '
TIME_MARKET = ' '
LEVER = 2  # ????
LAST_ID = 0
N_TEST_ORDER = 0
LAST_PRICE = 0.0
LAST_QTY = 0.0
LAST_TYPE = 'LIMIT_TEST'
LAST_SIDE = 'none'

##########################################################
sTest = 'TEST'
if TEST and R_T == 'REAL':        # False - РЕАЛЬНЫЙ ACCOUT
    client = test_client
    bot = botT
elif TEST and R_T == 'TEST':
    client = test_client
    bot = botT
elif TEST == False and R_T == 'TEST':
    client = clientR
    bot = botR
    sTest = 'REAL'
elif TEST == False and R_T == 'REAL':
    client = clientR
    bot = botR
    sTest = 'REAL'
else:
    print('НЕДОПУСТИМО: TEST / R_T =' + str(TEST) + ' / ' + str(R_T))
#print('config5(): ====================================================== ACCOUNT=' + sTest + ' / ORDER=' + str(R_T))
dt1 = dt.datetime.now()
TIME = dt1
dts = str(dt1.strftime("%Y%m%d %H:%M:%S"))
#time = datetime.utcfromtimestamp(candle['t']/1000).strftime('%Y-%m-%d %H:%M:%S')
print(str(dts) + '] config5(): ACCOUNT TEST=' + str(TEST) + ' / ORDER=' + str(R_T) + '  PARA=' + ASSET + ' STRATEGY=' + str(STRATEGY))
#--------------------------------
info = client.get_symbol_info(ASSET)
    #print("info=" + str(info))
    #print("info['orderTypes'] = " + str(info['orderTypes']))
    #print("info['quoteAssetPrecision'] = " + str(info['quoteAssetPrecision']))
filters = info['filters']
    # print("info['filters']= " + str(filters))
f0 = filters[0]
minPrice = float(f0.get('minPrice'))
maxPrice = float(f0.get('maxPrice'))  #: '100000.00000000', '
tickSize = float(f0.get('tickSize'))  #: '0.01000000'
print('  minPrice=' + str(minPrice) + ' maxPrice=' + str(maxPrice) + ' tickSize=' + str(tickSize))
f2 = filters[2]
    #      {'filterType': 'LOT_SIZE', 'minQty': '0.00001000', 'maxQty': '9000.00000000', 'stepSize': '0.00001000'},
minQty = float(f2.get('minQty'))  # ': '0.00001000', '
maxQty = float(f2.get('maxQty'))  # ': '9000.00000000', '
stepSize = float(f2.get('stepSize'))  # ': '0.00001000'
f3 = filters[3]
    #      {'filterType': 'MIN_NOTIONAL', 'minNotional': '10.00000000', 'applyToMarket': True, 'avgPriceMins': 5},
MIN_LOT = float(f3.get('minNotional'))
print('  minQty=' + str(minQty) + ' maxQty=' + str(maxQty) + ' stepSize=' + str(stepSize) + ' minNotional=' + str(MIN_LOT))
'''
bot.ticker24hr=  {'symbol': 'BNBUSDT', 'priceChange': '-13.53000000', 'priceChangePercent': '-2.531', 'weightedAvgPrice': '518.91576478',
 'prevClosePrice': '534.67000000', 'lastPrice': '521.13000000', 'lastQty': '0.03800000', 'bidPrice': '521.15000000', 'bidQty': '2.83020000',
  'askPrice': '521.16000000', 'askQty': '7.25590000', 'openPrice': '534.66000000', 'highPrice': '542.50000000', 'lowPrice': '492.02000000',
print('bot.tickerPrice= ', bot.tickerPrice(symbol=ASSET))
'''
bot_ticker24hr = bot.ticker24hr(symbol=ASSET)
priceChange = float(bot_ticker24hr.get('priceChange'))                   # -13.53000000
priceChangePercent = float(bot_ticker24hr.get('priceChangePercent'))     # -2.531
WeightedAvgPrice = float(bot_ticker24hr.get('weightedAvgPrice'))       # 518.91576478'
print('ИЗМЕНЕНИЯ ЗА СУТКИ: priceChange= ' + str(priceChange) + ' %= ' + str(priceChangePercent) + ' AVR= ' + str(WeightedAvgPrice))

cur_askPrice = float(bot_ticker24hr.get('askPrice'))
cur_bidPrice = float(bot_ticker24hr.get('bidPrice'))
bot_tickerPrice = float(bot.tickerPrice(symbol=ASSET).get('price'))
CUR_PRICE = bot_tickerPrice
print('bot.tickerPrice= ' + str(bot_tickerPrice) + ' cur_askPrice=' + str(cur_askPrice) + ' cur_bidPrice=' + str(cur_bidPrice))
if R_T == 'TEST':
    START_bq = round(float(client.get_asset_balance(asset=QUOTE)['free']), 4)  # тек баланс квотируемой валюты
    START_bb = round(float(client.get_asset_balance(asset=BASE)['free']), 4)  # базовой
    BALANCE_T_QUOTE = START_bq
    BALANCE_T_BASE = START_bb
    MY_SIDE = 'none'
    zapis = 'config5()-model: MY_SIDE = START_SIDE = ' + MY_SIDE + ' START_bq/bb=' + str(START_bq) + '/' + str(START_bb)
else:
    START_bq = round(float(client.get_asset_balance(asset=QUOTE)['free']),4)  # тек баланс квотируемой валюты
    START_bb = round(float(client.get_asset_balance(asset=BASE)['free']),4)   # базовой
    BALANCE_QUOTE = START_bq
    BALANCE_BASE = START_bb
    MY_SIDE = START_SIDE
    zapis = 'config5(): MY_SIDE = START_SIDE = ' + MY_SIDE + ' START_bq/bb=' + str(START_bq) + '/' + str(START_bb)
print(zapis)
#src.f_write(zapis)
dt1 = dt.datetime.now()
TIME = dt1
dts = str(dt1.strftime("%Y.%m.%d %H:%M:%S"))
print('end ------------------------------------------- config5()  TIME=' + dts)
