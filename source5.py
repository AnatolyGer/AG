from binance.client import Client
from binance.enums import *
from datetime import datetime
import config5 as co
########################################################################################## def's
# функции программы СТРАТЕГИИ_5  см. COMMENT_ALEXbot5
###############################################################################################
def AL(name):     # Alert my
    global INF, prog   #
    #  dt1 = dt.datetime.now()
    # s = str(dt1.strftime("%Y%m%d %H:%M:%S")) + '=' + prog0 + ']', f'{name}'
    s = 'AL(): ' + prog + ']', f'{name}'
    print(s)
    '''
    if INF == 'alert':
        print(s)
    elif INF == 'log':
        #log.debug(s)
    else:
        print(s)
        #log.debug(s)
    '''
#-------------------------------------------------------- readFile()
def readFile(name):
    f = open(name)
    ints = []
    i=0
    try:
        for line in f:
         ints.append(line)
         i=i+1
        print(line)
    except ValueError:
        print('Это не число. Выходим.')
    except Exception:
        print('Это что ещё такое?')
    else:
        print('Всё хорошо.')
    finally:
        f.close()
        print('========  закрыл файл.Введено ',i,' строк.')
# ------------------------------------------------------- ''' Б а л а н с '''
def balance(symbol):
    balance = client.get_asset_balance(asset=symbol)
    balance = {'free': balance['free'], 'locked': balance['locked']}
    #s="БАЛАНС="+balance
    #AL(s)
    return balance
# --------------------------
def f_write(zapis):
    f = open("TORGI.txt", "a") # открыть на добавление записей
    z = zapis + '\n'
    f.write(z)
    #print("f_write():  file.closed: " + str(f.closed) + " / file.mode: " + f.mode + " / file.name: " + f.name)
    # file.closed: False  / file.mode: a  /  file.name: TORGI.txt
    f.close()

def f_read():
    f = open("TORGI.txt", "r")
    k_line = 0
    for line in f:
        #print(line)
        k_line += 1
    f.close()
    print('f_read():    В файле TORGI.txt записей = ' + str(k_line))

def on_open(ws):
    """Do something when websocket opening.
    Args:
        ws: current websocket
    """
    print("Opened connection=================== START_ proga = ALEXbot5.py________________________")

def on_close(ws):
    """Do something when websocket closing.
    Args:
        ws: current websocket
    """

    print("Closed connection")

def print_current_candle(candle):
    global TIME
    """Printing current candle. Read more https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md#klinecandlestick-streams
    Args:
        candle (list): candle info
    """
    time = datetime.utcfromtimestamp(candle['t']/1000).strftime('%Y-%m-%d %H:%M:%S')
    TIME = time
    #print("Time: {} Open: {} High: {} Low: {} Close: {} Volume: {}".format(time,candle['o'],candle['h'],candle['l'],candle['c'],candle['v']))

def profit_loss(entry_price):
    global CUR_PRICE, BALANCE_QUOTE, BALANCE_BASE, CLIENT, QUANTITY
    print('profit_loss(): entry_price=' + str(entry_price))
    # balances
    BALANCE_QUOTE = float(CLIENT.get_asset_balance(asset=settings.QUOTE)['free'])  # тек баланс квотируемой валюты
    BALANCE_BASE = float(CLIENT.get_asset_balance(asset=settings.BASE)['free'])  # базовой
    # free_usdt = new_free_usdt
    print("on_open...2()BUY:   balance_QUOTE= {} is {}, balance_BASE= {} is {}".format(settings.QUOTE, BALANCE_QUOTE, settings.BASE, BALANCE_BASE))
    if entry_price > 0.0:
        rBB = round((BALANCE_QUOTE - 1000.0), 4)  # прирост BNB
        rBB1 = round((rBB * entry_price * (1 / QUANTITY)), 4)  # прирост USDT по текущей цене BNBUSDT за лот
        rBB2 = round((BALANCE_QUOTE + rBB1), 4)  # сколько бы было USDT при продаже BNB прироста по тек.цене
        rBB3 = round((rBB2 - 10000.0), 4)  # оценка изменения USDT c начального баланса
        zapis = 'profit_loss(): прирост BNB=' + str(rBB) + ' прирост USDT=' + str(
            rBB1) + ' USDT при продаже BNB=' + str(rBB2) + ' PROFIT/LOSS=' + str(rBB3)
        print(zapis)
        f_write(zapis)
        #    f_read()
        ''' считаем прибыль-убыток с начала запуска бота:
        if BALANCE_BASE == 0.0:
            BALANCE_BASE = free_bnb
            BALANCE_QUOTE = new_free_usdt
        bb = BALANCE_BASE - free_bnb
        bq = BALANCE_QUOTE - new_free_usdt
        print('       РЕЗУЛЬТАТ ТОРГА balance_base=' + str(bb) + 'balance_quote=' + str(bq))
        '''

def on_the_open5(client):          # for ALEXbot5

    # global BASE, QUOTE, SYMBOL, BALANCE_BASE, BALANCE_QUOTE, TP, dTP, MY_SIDE, MIN_LOT
    print('on_the_open5():=============================================ACCOUNT TEST=' + str(co.TEST) + ' ORDER=' + co.R_T)
    info = client.get_symbol_info(co.ASSET)
    #print("info=" + str(info))
    #print("info['orderTypes'] = " + str(info['orderTypes']))
    #print("info['quoteAssetPrecision'] = " + str(info['quoteAssetPrecision']))
    filters = info['filters']
    f0 = filters[0]
    minPrice = float(f0.get('minPrice'))
    maxPrice = float(f0.get('maxPrice'))  #: '100000.00000000', '
    tickSize = float(f0.get('tickSize'))  #: '0.01000000'
    print('on...5(): minPrice=' + str(minPrice) + ' maxPrice=' + str(maxPrice) + ' tickSize=' + str(tickSize))
    f2 = filters[2]
    #      {'filterType': 'LOT_SIZE', 'minQty': '0.00001000', 'maxQty': '9000.00000000', 'stepSize': '0.00001000'},
    minQty = float(f2.get('minQty'))  # ': '0.00001000', '
    maxQty = float(f2.get('maxQty'))  # ': '9000.00000000', '
    stepSize = float(f2.get('stepSize'))  # ': '0.00001000'

    f3 = filters[3]
    #      {'filterType': 'MIN_NOTIONAL', 'minNotional': '10.00000000', 'applyToMarket': True, 'avgPriceMins': 5},
    MIN_LOT = float(f3.get('minNotional'))
    print('minQty=' + str(minQty) + ' maxQty=' + str(maxQty) + ' stepSize=' + str(stepSize) + ' minNotional=' + str(MIN_LOT))
    '''
    if co.TEST: # TEST account
        bb = co.BALANCE_T_BASE
        bq = co.BALANCE_T_QUOTE
    else: # real ACCOUNT
        bb = float(client.get_asset_balance(asset='BUSD')['free'])
        bq = float(client.get_asset_balance(asset='USDT')['free'])
        bbt = float(co.test_client.get_asset_balance(asset='BUSD')['free'])
        bqt = float(co.test_client.get_asset_balance(asset='USDT')['free'])
        co.BALANCE_BASE = bb
        co.BALANCE_QUOTE = bq
    '''
    if co.R_T == 'TEST' and co.TEST == False: #real ACCOUNT
        bb = co.BALANCE_T_BASE
        bq = co.BALANCE_T_QUOTE
        bbt = float(co.test_client.get_asset_balance(asset='BUSD')['free'])
        bqt = float(co.test_client.get_asset_balance(asset='USDT')['free'])
    elif co.R_T == 'TEST' and co.TEST == True:  #test ACCOUNT
        bb = co.BALANCE_T_BASE
        bq = co.BALANCE_T_QUOTE
        bbt = float(co.test_client.get_asset_balance(asset='BUSD')['free'])
        bqt = float(co.test_client.get_asset_balance(asset='USDT')['free'])
    else: # real account  R_T = 'REAL'
        bb = float(client.get_asset_balance(asset='BUSD')['free'])
        bq = float(client.get_asset_balance(asset='USDT')['free'])
        bbt = float(co.test_client.get_asset_balance(asset='BUSD')['free'])
        bqt = float(co.test_client.get_asset_balance(asset='USDT')['free'])
    print('on_the_open5(): bb,bq,bbt,bqt=' + str(bb) + ' / ' + str(bq) + ' / ' + str(bbt) + ' / ' + str(bqt))

    print('on_the_open5(): МОДИФИКАЦИЯ СТРАТЕГИИ ПОД пару BUSD_USDT')
#1. Выбор стартового направления -------------------------
    cur_ask = float(client.get_ticker(symbol=co.ASSET).get('askPrice'))
    cur_bid = float(client.get_ticker(symbol=co.ASSET).get('bidPrice'))
    avg_price = co.AVG_PRICE  # BUSDUSDT=1.0
    if cur_bid + co.Dbid < avg_price:
        cur_side = 'buy'
    elif cur_ask - co.Dask> avg_price:
        cur_side = 'sell'
    else:
        cur_side = 'none'
    co.MY_SIDE = cur_side
    sss = '#3.1/ ВЫБОР НАПРАВЛЕНИЯ ТОРГА: avg_price<(cur_ask-Dask) >(cur_bid+Dbid) => MY_SIDE= ' + str(avg_price) +\
          ' / ' + str(cur_ask) + ' / ' + str(co.Dask) + ' / ' + str(cur_bid) + ' / ' + str(co.Dbid) + ' / ' + cur_side
    print(sss)
    f_write(sss)
#2. Расчет размера позиции -------------------------------- ???
    Ntick =2
    cur_lot0 = co.MIN_LOT + co.Ntick * co.stepSize
    print('on_the_open5(): cur_lot=' + str(cur_lot0) + ' MIN_LOT=' + str(co.MIN_LOT) + ' stepSize=' + str(co.stepSize)\
          + ' Ntick=' + str(co.Ntick))
    if cur_side == 'sell' and bb > cur_lot0:
        cur_lot = cur_lot0      #round(bb, PRE_BB)-0.01
    elif cur_side == 'buy' and bq > cur_lot0:
        cur_lot = cur_lot0      #round(BALANCE_QUOTE, PRE_BQ)-0.01
    else:
        cur_lot = 0.0
    sss = '#3.2/ ВЫБОР ОБЬЕМА ТОРГА: BALANCE_BASE/PRE_BB/BALANCE_QUOTE/PRE_BQ/MIN_LOT/cur_lot= ' + str(bb) +\
    '/' + str(co.PRE_BB) + '/' + str(bq) + '/' + str(co.PRE_BQ) + '/' + str(co.MIN_LOT) + '/' + str(cur_lot)
    print(sss)
    f_write(sss)
#3.Определение цены отложенного ордера ----------------------------------
    dLIM_PRICE = co.DLIM_PRICE
    if cur_lot > 0.0:
        if cur_side == 'buy':
            open_price = cur_bid - dLIM_PRICE
        elif cur_side == 'sell':
            open_price = cur_ask + dLIM_PRICE
        else:
            open_price = 0.0
        sss = '#3.3/ ВЫБОР ЦЕНЫ LIMIT ORDER: DLIM_PRICE/open_price= ' + str(dLIM_PRICE) + ' / ' + str(open_price)
    else:
        open_price = 0.0
        sss='#3/ NOT LIMIT ORDER'
    co.CUR_PRICE = open_price
    print(sss)
    f_write(sss)
    print('on_the_open5(): return= LIMIT ORDER ' + cur_side + ' cur_lot=' + str(cur_lot) + ' open_price=' + str(open_price))
    return cur_side, cur_lot, open_price

def on_the_open6(client):          # for ALEXbot5

    # global BASE, QUOTE, SYMBOL, BALANCE_BASE, BALANCE_QUOTE, TP, dTP, MY_SIDE, MIN_LOT
    print('on_the_open5():=============================================ACCOUNT TEST=' + str(co.TEST) + ' ORDER=' + co.R_T)
    info = client.get_symbol_info(co.ASSET)
    filters = info['filters']
    f0 = filters[0]
    minPrice = float(f0.get('minPrice'))
    maxPrice = float(f0.get('maxPrice'))  #: '100000.00000000', '
    tickSize = float(f0.get('tickSize'))  #: '0.01000000'
    #print('on...5(): minPrice=' + str(minPrice) + ' maxPrice=' + str(maxPrice) + ' tickSize=' + str(tickSize))
    f2 = filters[2]
    #      {'filterType': 'LOT_SIZE', 'minQty': '0.00001000', 'maxQty': '9000.00000000', 'stepSize': '0.00001000'},
    minQty = float(f2.get('minQty'))  # ': '0.00001000', '
    maxQty = float(f2.get('maxQty'))  # ': '9000.00000000', '
    stepSize = float(f2.get('stepSize'))  # ': '0.00001000'

    f3 = filters[3]
    #      {'filterType': 'MIN_NOTIONAL', 'minNotional': '10.00000000', 'applyToMarket': True, 'avgPriceMins': 5},
    MIN_LOT = float(f3.get('minNotional'))
    print('minQty=' + str(minQty) + ' maxQty=' + str(maxQty) + ' stepSize=' + str(stepSize) + ' minNotional=' + str(MIN_LOT))
    '''
    if co.TEST: # TEST account
        bb = co.BALANCE_T_BASE
        bq = co.BALANCE_T_QUOTE
    else: # real ACCOUNT
        bb = float(client.get_asset_balance(asset='BUSD')['free'])
        bq = float(client.get_asset_balance(asset='USDT')['free'])
        bbt = float(co.test_client.get_asset_balance(asset='BUSD')['free'])
        bqt = float(co.test_client.get_asset_balance(asset='USDT')['free'])
        co.BALANCE_BASE = bb
        co.BALANCE_QUOTE = bq
    '''
    if co.R_T == 'TEST' and co.TEST == False: #real ACCOUNT
        bb = co.BALANCE_T_BASE
        bq = co.BALANCE_T_QUOTE
        bbt = float(co.test_client.get_asset_balance(asset='BUSD')['free'])
        bqt = float(co.test_client.get_asset_balance(asset='USDT')['free'])
    elif co.R_T == 'TEST' and co.TEST == True:  #test ACCOUNT
        bb = co.BALANCE_T_BASE
        bq = co.BALANCE_T_QUOTE
        bbt = float(co.test_client.get_asset_balance(asset='BUSD')['free'])
        bqt = float(co.test_client.get_asset_balance(asset='USDT')['free'])
    else: # real account  R_T = 'REAL'
        bb = float(client.get_asset_balance(asset='BUSD')['free'])
        bq = float(client.get_asset_balance(asset='USDT')['free'])
        bbt = float(co.test_client.get_asset_balance(asset='BUSD')['free'])
        bqt = float(co.test_client.get_asset_balance(asset='USDT')['free'])
    print('on_the_open5(): bb,bq,bbt,bqt=' + str(bb) + ' / ' + str(bq) + ' / ' + str(bbt) + ' / ' + str(bqt))
    cur_side = co.CUR_SIDE
    print('on_the_open5(): МОДИФИКАЦИЯ СТРАТЕГИИ ПОД пару BUSD_USDT')
    if cur_side == 'buy' or co.CUR_SIDE == 'none':
        cur_side = 'sell'
    elif cur_side == 'sell':
        cur_side = 'buy'
    else:
        cur_side = 'none'
    co.CUR_SIDE = cur_side

    #print('#1. Расчет размера позиции --------------------------------')
    # открытие: если есть депозит
    cur_lot0 = round((2*co.MIN_LOT + co.NstepSize * co.stepSize), 2)
    if bq >= cur_lot0 and cur_side == 'buy':
        cur_lot = cur_lot0
    elif bb >= cur_lot0 and cur_side == 'sell':
        cur_lot = cur_lot0
    else:
        cur_lot = 0.0
        print('NOT money on BALANCE  QUOTE=' + str(co.BASE_T_QUOTE) + '/ BASE=' + str(co.BALANCE_BASE))
        cur_side = 'none'
    print('cur_lot =', cur_lot)
    sss = '#3.1/ ВЫБОР ОБЬЕМА ТОРГА: MIN_LOT/NstepSize/stepSize/BALANCE_BASE/BALANCE_QUOTE/cur_lot= ' + str(co.MIN_LOT)\
          + '/' + str(co.NstepSize) + '/' + str(co.stepSize) + '/' + str(bb) + '/' + str(bq) + '/' + str(cur_lot)
    print(sss)
    f_write(sss)
    #3.Определение цены отложенного ордера ----------------------------------
    dLIM_PRICE = co.DLIM_PRICE
    cur_ask = float(client.get_ticker(symbol=co.ASSET).get('askPrice'))
    cur_bid = float(client.get_ticker(symbol=co.ASSET).get('bidPrice'))
    if cur_lot > 0.0:
        if cur_side == 'buy':
            open_price = cur_bid - dLIM_PRICE
        elif cur_side == 'sell':
            open_price = cur_ask + dLIM_PRICE
        else:
            open_price = 0.0
        sss = '#3.2/ ВЫБОР ЦЕНЫ LIMIT ORDER: DLIM_PRICE/open_price= ' + str(dLIM_PRICE) + ' / ' + str(open_price)
    else:
        open_price = 0.0
        sss='#3/ NOT LIMIT ORDER'
    co.CUR_PRICE = open_price
    print(sss)
    f_write(sss)
    print('on_the_open6(): return= LIMIT ORDER ' + cur_side + ' cur_lot=' + str(cur_lot) + ' open_price=' + str(open_price))
    return cur_side, cur_lot, open_price

def on_the_open7(client):          # for ALEXbot5

    # global BASE, QUOTE, SYMBOL, BALANCE_BASE, BALANCE_QUOTE, TP, dTP, MY_SIDE, MIN_LOT
    print('on_the_open7():=============================================ACCOUNT TEST=' + str(co.TEST) + ' ORDER=' + co.R_T)
    info = client.get_symbol_info(co.ASSET)
    filters = info['filters']
    f0 = filters[0]
    minPrice = float(f0.get('minPrice'))
    maxPrice = float(f0.get('maxPrice'))  #: '100000.00000000', '
    tickSize = float(f0.get('tickSize'))  #: '0.01000000'
    #print('on...5(): minPrice=' + str(minPrice) + ' maxPrice=' + str(maxPrice) + ' tickSize=' + str(tickSize))
    f2 = filters[2]
    #      {'filterType': 'LOT_SIZE', 'minQty': '0.00001000', 'maxQty': '9000.00000000', 'stepSize': '0.00001000'},
    minQty = float(f2.get('minQty'))  # ': '0.00001000', '
    maxQty = float(f2.get('maxQty'))  # ': '9000.00000000', '
    stepSize = float(f2.get('stepSize'))  # ': '0.00001000'

    f3 = filters[3]
    #      {'filterType': 'MIN_NOTIONAL', 'minNotional': '10.00000000', 'applyToMarket': True, 'avgPriceMins': 5},
    MIN_LOT = float(f3.get('minNotional'))
    #print('minQty=' + str(minQty) + ' maxQty=' + str(maxQty) + ' stepSize=' + str(stepSize) + ' minNotional=' + str(MIN_LOT))

    if co.R_T == 'TEST' and co.TEST == False: #real ACCOUNT
        bb = co.BALANCE_T_BASE
        bq = co.BALANCE_T_QUOTE
        bbt = float(co.test_client.get_asset_balance(asset='BUSD')['free'])
        bqt = float(co.test_client.get_asset_balance(asset='USDT')['free'])
    elif co.R_T == 'TEST' and co.TEST == True:  #test ACCOUNT
        bb = co.BALANCE_T_BASE
        bq = co.BALANCE_T_QUOTE
        bbt = float(co.test_client.get_asset_balance(asset='BUSD')['free'])
        bqt = float(co.test_client.get_asset_balance(asset='USDT')['free'])
    else: # real account  R_T = 'REAL'
        bb = float(client.get_asset_balance(asset='BUSD')['free'])
        bq = float(client.get_asset_balance(asset='USDT')['free'])
        bbt = float(co.test_client.get_asset_balance(asset='BUSD')['free'])
        bqt = float(co.test_client.get_asset_balance(asset='USDT')['free'])
    #print('on_the_open7(): МОДИФИКАЦИЯ СТРАТЕГИИ ПОД пару BUSD_USDT =================================================')
    print('on_the_open7(): bb,bq,bbt,bqt=' + str(bb) + ' / ' + str(bq) + ' / ' + str(bbt) + ' / ' + str(bqt))
    co.BALANCE_BASE = bb
    co.BALANCE_QUOTE = bq
    if bb > bq and bb > (co.MIN_LOT + stepSize):
        cur_side = 'sell'
        cur_lot = round((bb - stepSize), 2)
    elif bb < bq and bq > (co.MIN_LOT + stepSize):
        cur_side = 'buy'
        cur_lot = round((bq - stepSize), 2)
    else:
        print('NOT money on BALANCE  QUOTE=' + str(co.BALANCE_QUOTE) + '/ BASE=' + str(co.BALANCE_BASE))
        cur_side = 'none'
        cur_lot = 0.0
    print('on_the_open7(): cur_side =' + cur_side + ' cur_lot =' + str(cur_lot))

    #3.Определение цены отложенного ордера ----------------------------------
    dLIM_PRICE = co.DLIM_PRICE
    cur_ask = float(client.get_ticker(symbol=co.ASSET).get('askPrice'))
    cur_bid = float(client.get_ticker(symbol=co.ASSET).get('bidPrice'))
    if cur_lot > 0.0:
        if cur_side == 'buy':
            open_price = cur_bid - dLIM_PRICE
        elif cur_side == 'sell':
            open_price = cur_ask + dLIM_PRICE
        else:
            open_price = 0.0
        sss = '#3/  LIMIT ORDER: DLIM_PRICE/cur_lot/open_price= ' + str(dLIM_PRICE) + '/' + cur_side   +\
              ' / ' + str(cur_lot) + ' / ' + str(open_price)
    else:
        open_price = 0.0
        sss='#3/ NOT LIMIT ORDER'
    co.CUR_PRICE = open_price
    co.CUR_LOT = cur_lot
    co.CUR_SIDE = cur_side
    print(sss)
    f_write(sss)
    print('on_the_open7(): return= LIMIT ORDER ' + cur_side + ' cur_lot=' + str(cur_lot) + ' open_price=' + str(open_price))
    return cur_side, cur_lot, open_price

def precision_price(price):
    """Format price to SYMBOL precision. Use the get_symbol_info function to get info about a particular symbol.
    Args:
        price (float): current price
    Returns:
        float: formatted price
    """
    precision = 4
    precision_price = "{:0.0{}f}".format(price, precision)

    return precision_price

def limit(client,entry_price,quantity,side):
    """Sending  limit order.
    Args:
        client: TEST ACCOUNT / REAL
        entry_price (float):  price
        quantity (float):  quantity
        side: buy /sell
    Returns:
        boolean: True if buying order is finished and False if error
    """
    global LAST_ID, LAST_PRICE, LAST_QTY, LAST_TYPE, LAST_SIDE, TIME

    try:
        if entry_price == 0.0:
            return False
        precision_entry_price = precision_price(entry_price)
        time = co.TIME
        if side == 'buy':
            print("limit(): Time {} ПОКУПКА {} {} ЗА {} {}".format(time, quantity, co.BASE, precision_entry_price, co.QUOTE))
            order = client.order_limit_buy(
                symbol=co.SYMBOL,
                quantity=quantity,
                price=precision_entry_price
            )
        else:
            print("limit(): Time {} ПРОДАЖА {} {} ЗА {} {}".format(time, quantity, co.BASE, precision_entry_price,
                                                          co.QUOTE))
            order = client.order_limit_sell(
                symbol=co.SYMBOL,
                quantity=quantity,
                price=precision_entry_price
            )
        zapis = str(order)
        f_write(zapis)
        co.LAST_ID = order.get('orderId')
        co.LAST_PRICE = order.get('price')
        co.LAST_QTY = order.get('origQty')
        co.LAST_TYPE = order.get('type')
        co.LAST_SIDE = order.get('side')
        dt1 = dt.datetime.now()
        TIME = dt1
        co.TIME_LIMIT = dt1
        dts = str(dt1.strftime("%Y%m%d %H:%M:%S"))
        zapis = 'TIME=' + dts + ' limit(): ОТКРЫТ ОРДЕР id=' + str(co.LAST_ID) + ' ' + co.LAST_TYPE + ' ' +\
                co.LAST_SIDE + ' ' + str(co.LAST_QTY) + ' ' + str(co.LAST_PRICE)
        print(zapis)
        f_write(zapis)
        return True
    except Exception as e:
        print("limit():  order error:   {}".format(e))
        return False

def limitT(client,entry_price,quantity,side):
    """Sending  limit order.
    Args: LIM_MAKER  ===== TEST ACCOUNT=FALSE R_T= TEST
        client: TEST ACCOUNT / REAL
        entry_price (float):  price
        quantity (float):  quantity
        side: buy /sell
    Returns:
        boolean: True if buying order is finished and False if error
    """
    #global LAST_ID, LAST_PRICE, LAST_QTY, LAST_TYPE, LAST_SIDE, TIME

    try:
        if entry_price == 0.0:
            return False
        precision_entry_price = precision_price(entry_price)
        time = co.TIME
        if side == 'buy':
            print("limitT(): Time {} ПОКУПКА {} {} ЗА {} {}".format(time, quantity, co.BASE, precision_entry_price, co.QUOTE))
            order = client.create_test_order(
                symbol=co.SYMBOL,
                side='BUY',
                type='LIMIT',
                recvWindow=10000,
                timeInForce='GTC',
                quantity=quantity,
                price=precision_entry_price
            )
            if str(order) != '{}':
                print('Order Real Account Test - not BUY =' + str(order))
                return False
        else:
            print("limitT(): Time {} ПРОДАЖА {} {} ЗА {} {}".format(time, quantity, co.BASE, precision_entry_price,
                                                          co.QUOTE))
            order = client.create_test_order(
                symbol=co.SYMBOL,
                side='SELL',
                type='LIMIT',
                recvWindow=10000,
                timeInForce='GTC',
                quantity=quantity,
                price=precision_entry_price
            )
            if str(order) != '{}':
                print('Order Real Account Test - not SELL =' + str(order))
                return False
        print('limitT(): МОДЕЛИРОВАНИЕ  ОТКРЫТИЯ ОРДЕРА -------------------------------------------------------------')
        co.LAST_ID = co.N_TEST_ORDER + 1
        co.LAST_PRICE = precision_entry_price
        co.LAST_QTY = quantity
        co.LAST_TYPE = 'LIMIT_TEST'
        co.LAST_SIDE = side
        zapis = 'limitT(): ОТКРЫТ ОРДЕР id=' + str(co.LAST_ID) + ' ' + co.LAST_TYPE + ' ' + co.LAST_SIDE + ' ' + str(co.LAST_QTY) + ' ' + str(co.LAST_PRICE)
        print(zapis)
        f_write(zapis)
        return True
    except Exception as e:
        print("limitT():  order error:   {}".format(e))
        return False

def buy(client,entry_price,quantity):
    """Sending buy limit order.
    Args:
        entry_price (float): buying price
        quantity (float): buying quantity
    Returns:
        boolean: True if buying order is finished and False if error
    """
    global LAST_ID, LAST_PRICE, LAST_QTY, LAST_TYPE, LAST_SIDE, TIME
    # global test_client, BASE, QUOTE, SYMBOL
    try:
        if entry_price == 0.0:
            return False
        precision_entry_price = precision_price(entry_price)
        #time = datetime.utcfromtimestamp(candle['t'] / 1000).strftime('%Y-%m-%d %H:%M:%S')
        time = TIME
        #print("Buying {} {} at {} {}".format(quantity,settings.BASE,precision_entry_price,settings.QUOTE))
        print("Time {} ПОКУПКА {} {} ЗА {} {}".format(time, quantity, settings.BASE, precision_entry_price, settings.QUOTE))
        order = client.order_limit_buy(
            symbol=settings.SYMBOL,
            quantity=quantity,
            price=precision_entry_price
        )
        zapis = str(order)
        f_write(zapis)
        LAST_ID = order.get('orderId')
        LAST_PRICE = order.get('price')
        LAST_QTY = order.get('origQty')
        LAST_TYPE = order.get('type')
        LAST_SIDE = order.get('side')
        zapis = 'buy(): ОТКРЫТ ОРДЕР id=' + str(LAST_ID) + ' ' + LAST_TYPE + ' ' + LAST_SIDE + ' ' + str(LAST_QTY) + ' ' + str(LAST_PRICE)
        print(zapis)
        f_write(zapis)
        print("============================Buy order info: {}".format(order))
        return True
    except Exception as e:
        print("Buy order error:   {}".format(e))
        return False

def buyT(client,entry_price,quantity):
    """Sending buy limit order.
    Args:
        entry_price (float): buying price
        quantity (float): buying quantity
    Returns:
        boolean: True if buying order is finished and False if error
    """
    global LAST_ID, LAST_PRICE, LAST_QTY, LAST_TYPE, LAST_SIDE, TIME
    # global test_client, BASE, QUOTE, SYMBOL
    try:
        if entry_price == 0.0:
            return False
        precision_entry_price = precision_price(entry_price)
        #time = datetime.utcfromtimestamp(candle['t'] / 1000).strftime('%Y-%m-%d %H:%M:%S')
        time = TIME
        #print("Buying {} {} at {} {}".format(quantity,settings.BASE,precision_entry_price,settings.QUOTE))
        print("Time {} ПОКУПКА {} {} ЗА {} {}".format(time, quantity, settings.BASE, precision_entry_price, settings.QUOTE))
        '''
        order = client.order_limit_buyT(
            symbol=settings.SYMBOL,
            quantity=quantity,
            price=precision_entry_price
        )
        '''
        order = client.create_test_order(
            symbol=settings.SYMBOL,
            side='BUY',
            type='LIMIT',
            recvWindow=10000,
            timeInForce='GTC',
            quantity=quantity,
            price=precision_entry_price
        )
        if str(order) != '{}':
            print('Order Real Account Test - not BUY =' + str(order))
            return False
        else:
            zapis = str(order)
            f_write(zapis)
            LAST_ID = time
            LAST_PRICE = str(precision_entry_price)
            LAST_QTY = str(quantity)
            LAST_TYPE = 'limit'
            LAST_SIDE = 'buy'
        zapis = 'buyT(): ОТКРЫТ ОРДЕР id=' + str(LAST_ID) + ' ' + LAST_TYPE + ' ' + LAST_SIDE + ' ' + str(LAST_QTY) + ' ' + str(LAST_PRICE)
        print(zapis)
        f_write(zapis)
        print("============================Buy Test order info: {}".format(order))
        return True
    except Exception as e:
        print("Buy order error:   {}".format(e))
        return False

def sell(client,entry_price,quantity):
    """Sending buy limit order.
    Args:
        entry_price (float): buying price
        quantity (float): buying quantity
    Returns:
        boolean: True if buying order is finished and False if error
    """
    global LAST_ID, LAST_PRICE, LAST_QTY, LAST_TYPE, LAST_SIDE, TIME
    # global test_client, BASE, QUOTE, SYMBOL
    try:
        if entry_price == 0.0:
            return False
        precision_entry_price = precision_price(entry_price)
        #time = datetime.utcfromtimestamp(candle['t'] / 1000).strftime('%Y-%m-%d %H:%M:%S')
        time = TIME
        #print("ПРОДАЖА {} {} at {} {}".format(quantity,settings.BASE,precision_entry_price,settings.QUOTE))
        print("Time {} продажа {} {} ЗА {} {}".format(time, quantity, settings.BASE, precision_entry_price, settings.QUOTE))
        order = client.order_limit_sell(
            symbol=settings.SYMBOL,
            quantity=quantity,
            price=precision_entry_price
        )
        zapis = str(order)
        f_write(zapis)
        LAST_ID = order.get('orderId')
        LAST_PRICE = order.get('price')
        LAST_QTY = order.get('origQty')
        LAST_TYPE = order.get('type')
        LAST_SIDE = order.get('side')
        zapis = 'sell(): ОТКРЫТ ОРДЕР id=' + str(LAST_ID) + ' ' + LAST_TYPE + ' ' + LAST_SIDE + ' ' + str(LAST_QTY) + ' ' + str(LAST_PRICE)
        print(zapis)
        f_write(zapis)
        #print("============================Buy order info: {}".format(order))
        return True
    except Exception as e:
        print("Buy order error: {}".format(e))
        return False

def sellT(client,entry_price,quantity):
    """Sending buy limit order.
    Args:
        entry_price (float): buying price
        quantity (float): buying quantity
    Returns:
        boolean: True if buying order is finished and False if error
    """
    global LAST_ID, LAST_PRICE, LAST_QTY, LAST_TYPE, LAST_SIDE, TIME
    # global test_client, BASE, QUOTE, SYMBOL
    try:
        if entry_price == 0.0:
            return False
        precision_entry_price = precision_price(entry_price)
        #time = datetime.utcfromtimestamp(candle['t'] / 1000).strftime('%Y-%m-%d %H:%M:%S')
        time = TIME
        #print("ПРОДАЖА {} {} at {} {}".format(quantity,settings.BASE,precision_entry_price,settings.QUOTE))
        print("Time {} продажа {} {} ЗА {} {}".format(time, quantity, settings.BASE, precision_entry_price, settings.QUOTE))
        order = client.create_test_order(
            symbol=settings.SYMBOL,
            side='SELL',
            type='LIMIT',
            recvWindow=10000,
            timeInForce='GTC',
            quantity=quantity,
            price=precision_entry_price
        )
        if str(order) != '{}':
            print('Order Real Account Test - not SELL =' + str(order))
            return False
        else:
            zapis = str(order)
            f_write(zapis)
            LAST_ID = time
            LAST_PRICE = str(precision_entry_price)
            LAST_QTY = str(quantity)
            LAST_TYPE = 'limit'
            LAST_SIDE = 'sell'
            zapis = 'sellT(): ОТКРЫТ ОРДЕР id=' + str(LAST_ID) + ' ' + LAST_TYPE + ' ' + LAST_SIDE + ' ' + str(
            LAST_QTY) + ' ' + str(LAST_PRICE)
        print(zapis)
        f_write(zapis)
        print("============================SELL Test order info: {}".format(order))
        return True
    except Exception as e:
        print("Buy order error: {}".format(e))
        return False

def take_profit(client, quantity, tp, MY_SIDE):
        """Sending selling market order
        Args:
            tp (float): close price
            quantity (float): selling quantity
            MY_SIDE - buy /sell
        Returns:
            boolean: True if take order is finished and False if error
        """
        free_usdt = float(client.get_asset_balance(asset=settings.QUOTE)['free'])
        if tp == 0.0:
            print('TP-error=' + str(tp))
            return free_usdt
        try:
            print("Take profit: Close price is {} {}".format(tp, MY_SIDE))
            precision_entry_price = precision_price(tp)
            time = TIME

            if MY_SIDE == 'buy':
                # print("ПРОДАЖА {} {} at {} {}".format(quantity,settings.BASE,precision_entry_price,settings.QUOTE))
                print("Time {} TP=продажа {} {} ЗА {} {}".format(time, quantity, settings.BASE, precision_entry_price,
                                                              settings.QUOTE))
                order = client.order_limit_sell(
                    symbol=settings.SYMBOL,
                    quantity=quantity,
                    price=precision_entry_price
                )
            else:
                order = client.order_limit_buy(
                    symbol=settings.SYMBOL,
                    quantity=quantity,
                    price=precision_entry_price
                )
            new_free_usdt = float(client.get_asset_balance(asset=settings.QUOTE)['free'])
            print("Profit is {} {}".format(free_usdt - new_free_usdt, settings.QUOTE))
            free_usdt = new_free_usdt

            print("Take order info: {}".format(order))
            close_price = order.get('fills')[0].get('price')
            print('order.close_price=' + str(close_price))
            zapis = str(order)
            f_write(zapis)
            return free_usdt
        except Exception as e:
            print("Take order error: {}".format(e))
            return False

def take(client,quantity,open_price,free_usdt):
    """Sending selling market order
    Args:
        open_price (float): open candle price
        quantity (float): selling quantity
    Returns:
        boolean: True if take order is finished and False if error
    """
    # global free_usdt, test_client, BASE, QUOTE, SYMBOL
    try:
        print("Take order. Open price is {} {}".format(open_price,settings.QUOTE))
        order = client.order_market_sell(
            symbol=settings.SYMBOL,
            quantity=quantity
        )
        new_free_usdt = float(client.get_asset_balance(asset=settings.QUOTE)['free'])
        print("Profit is {} {}".format(free_usdt-new_free_usdt,settings.QUOTE))
        free_usdt = new_free_usdt
        print("Take order info: {}".format(order))
        close_price = order.get('fills')[0].get('price')
        print('close_price=' + str(close_price))
        zapis = str(order)
        f_write(zapis)
        return free_usdt
    except Exception as e:
        print("Take order error: {}".format(e))
        return False

def stop(client,quantity,open_price,free_usdt):
    """Sending selling market order
    Args:
        open_price (float): open candle price
        quantity (float): selling quantity
    Returns:
        boolean: True if stop order is finished and False if error
    """
    # global free_usdt, test_client, BASE, QUOTE, SYMBOL
    try:
        print("Stop order. Open price is {} {}".format(open_price,settings.QUOTE))
        order = client.order_market_sell(
            symbol=settings.SYMBOL,
            quantity=quantity
        )
        zapis = "Stop order =" + str(order)
        price(zapis)
        f_write(zapis)
        new_free_usdt = float(client.get_asset_balance(asset=settings.QUOTE)['free'])
        print("Loss is {} {}".format(new_free_usdt-free_usdt,settings.QUOTE))
        free_usdt = new_free_usdt
        print("Stop order info: {}".format(order))
        return free_usdt
    except Exception as e:
        print("Stop order error: {}".format(e))
        return False

def my_orders():
    orders = client.get_all_orders()
    print('my_orders(): ' + str(orders))
    return orders

def get_order_trades(order_id, pair, bot):
    trades = bot.myTrades(symbol=pair)
    trades.reverse()

    ret_trades = []
    for trade in trades:
        if str(trade['orderId']) == str(order_id):
            ret_trades.append(
                BaseTrade(
                    trade_id=trade['id'],
                    trade_rate=float(trade['price']),
                    trade_amount=float(trade['qty']),
                    trade_type='buy' if trade['isBuyer'] else 'sell',
                    trade_fee=float(trade['commission']),
                    fee_type=trade['commissionAsset']
                )
            )
    return ret_trades

def analiz_lim_order(client, my_side, quantity, open_price):
    cur_ask = float(client.get_ticker(symbol=co.ASSET).get('askPrice'))
    cur_bid = float(client.get_ticker(symbol=co.ASSET).get('bidPrice'))
    print('analiz_lim_order(): my_side, quantity, open_price, cur_ask, cur_bid=' + my_side + '/' +\
          str(quantity) + '/' + str(open_price) + '/' + str(cur_ask) + '/' + str(cur_bid))
    if my_side == 'buy' and cur_bid <= float(open_price):
        in_position = False
        co.BALANCE_T_QUOTE = co.BALANCE_T_QUOTE + round((quantity) * float(open_price),2)
        co.BALANCE_T_BASE = co.BALANCE_T_BASE - quantity
    elif my_side == 'sell' and cur_ask >= float(open_price):
        in_position = False
        co.BALANCE_T_QUOTE = co.BALANCE_T_QUOTE - round((quantity) * float(open_price),2)
        co.BALANCE_T_BASE = co.BALANCE_T_BASE + quantity
    else:
        print('analiz_lim_order(): <>  NOT MARKET_ORDER')
        in_position = True
    print('analiz_lim_order():                                '  + ' ЦЕНА ОТКРЫТИЯ LIMIT ORDER=' + str(open_price) +\
          '  <>     текущий ask=' + str(cur_ask) + ' текущий bid=' + str(cur_bid))
    return in_position

