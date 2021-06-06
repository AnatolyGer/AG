# ----- ALEXbot7.py from ALEXbot4_210530_1 and barakbot_210508_1.py !!! mod GAN&Co - 210509
import websocket, json
import source5 as src
import config5 as co
import time as ti
import datetime as dt
# global variables =========================================================================
BASE = co.BASE    #'BUSD'
QUOTE = co.QUOTE  #"USDT"                          #                      -КВОТИРУЕМАЯ
SYMBOL = BASE+QUOTE
ASSET = SYMBOL
STRATEGY = 7            # 5 -COMMENT5
TEST = co.TEST          # False - РЕАЛЬНЫЙ
TORG = co.TORG
R_T  = co.R_T
MY_SIDE = co.MY_SIDE

BALANCE_BASE = 0.0           # кол-во монет базовой криптовалюты на счете
BALANCE_QUOTE = 0.0          # кол-во монет квотируемой валюты

LAST_ID = 1
LAST_PRICE = 0.0
LAST_QTY = 10.0
LAST_TYPE = ''
LAST_SIDE = ''
is_candle_opened = True
is_candle_closed = True
in_position = False
entry_price = 0.0
quantity = 0.0
free_usdt =0.0 
#--------------------------------- идентификация программы
prog0 = 'ALEXbot7'      # new STRATEGY=6 предложение САШИ - не учитывать положение цены относмтельно 1.0
ver = '_210605_1'       # balance +/- from start
prog = prog0 + ver
###############################################################################

# --------------------------
def main7(ws, msg):
    """Main algo function
    Args:
        ws: websocket
        msg: websocket message
    """
    global is_candle_opened, in_position, entry_price, quantity, free_usdt, TEST, TORG, STRATEGY, MY_SIDE
    global LAST_ID,LAST_PRICE,LAST_QTY,LAST_TYPE,LAST_SIDE
    try:
        json_message = json.loads(msg)
        candle = json_message['k']
        is_candle_closed = candle['x']

        dt1 = dt.datetime.now()
        co.TIME = dt1
        dts = str(dt1.strftime("%Y.%m.%d %H:%M:%S"))
        print('TIME=' + dts + ']===========================START_main7(): ASSET=' + ASSET + ' is_candle_open=' +str(is_candle_opened) +\
              ' is_candle_closed=' + str(is_candle_closed) + ' in_position=' + str(in_position) + ' R_T=' + co.R_T +\
              ' ACCOUNT TEST=' + str(TEST))
        if is_candle_opened:
            if in_position and R_T == 'REAL':    #==========================================================
                candle_c = float(candle['c'])
                #print('main7():  --------------------- анализ позы -- close=' + str(candle_c) + ' LAST_ID=' + str(co.LAST_ID))
                print('main7(): in_position = АНАЛИЗ позы R_T =' + co.R_T + ' ACOUNT=' + str(co.TEST))
                try:
                    status_order = co.client.get_order(symbol=ASSET,
                                                   orderId=co.LAST_ID,
                                                   recvWindow=10000)

                    LAST_ID = status_order.get('orderId')
                    LAST_PRICE = status_order.get('price')
                    LAST_QTY = status_order.get('origQty')
                    LAST_TYPE = status_order.get('type')
                    LAST_SIDE = status_order.get('side')
                    zapis = 'in_position-STATUS: ОТКРЫТ ОРДЕР id=' + str(LAST_ID) + ' ' + LAST_TYPE + ' ' + LAST_SIDE +\
                            ' ' + str(LAST_QTY) + ' ' + str(LAST_PRICE) + ' close_price=' + str(candle_c)
                    print(zapis)
                    src.f_write(zapis)
                    if LAST_TYPE == 'limit':
                        return
                    else:
                        print('main7(): lim -> market LAST_ID=' + str(LAST_ID))
                        in_position = False

                    if co.TEST== True: #
                        new_free_usdT = co.BALANCE_T_QUOTE
                        free_bnb = co.BALANCE_T_BASE
                    else: # real--------------------------------------------------------------------------
                        new_free_usdt = float(
                         co.client.get_asset_balance(asset=co.QUOTE)['free'])  # тек баланс квотируемой валюты
                        free_busd = float(co.client.get_asset_balance(asset=co.BASE)['free'])  # базовой
                    print('^^^^^^^^^^^^^^^^^^^^^^^^^ main7(): BASE_busd=' + str(free_busd) + ' QUOTE_usdt=' +\
                          str(new_free_usdt))
                    co.BALANCE_BASE = free_busd
                    co.BALANCE_QUOTE = new_free_usdt
                    if in_position == False:
                        r_bb = round((co.BALANCE_BASE - co.START_bb),4)
                        r_bq = round((co.BALANCE_QUOTE - co.START_bq),4)

                        print('main7():  BALANCE_BASE=' + str(co.BALANCE_BASE) + ' - ' + \
                              ' START_bb = ' + str(co.START_bb))
                        print('main7():  BALANCE_QUOTE=' + str(co.BALANCE_QUOTE) + ' - ' + \
                              ' START_bq = ' + str(co.START_bq))
                        dt1 = dt.datetime.now()
                        co.TIME_MARKET = dt1
                        stime = str(dt1.strftime("%Y.%m.%d %H:%M:%S"))
                        c = co.TIME_MARKET - co.TIME_OPEN
                        print('Разница во времени между событиями:', c)  # 0:05:17.099915'
                        sss = 'main7(): >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ИЗМЕНЕНИЯ БАЛАНСОВ от СТАРТА: bb= ' +\
                              str(r_bb) + ' / bq= ' + str(r_bq) + '<<<<<<<<<<<<< TIME=' + stime + '/ ' + str(c)
                        print(sss)
                        src.f_write(sss)
                        if co.MY_SIDE == 'sell':
                            co. MY_SIDE = 'buy'
                        else:
                            co.MY_SIDE = 'sell'
                    free_usdt = new_free_usdt
                    co.BALANCE_QUOTE = round(new_free_usdt,4)
                    co.BALANCE_BASE = round(free_bnb,4)
                    zapis = "main7(): balance_QUOTE= " + co.QUOTE + ' is ' + str(new_free_usdt) + ' balance_BASE=' +\
                            co.BASE + ' is ' + str(free_bnb)
                    print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ ' + zapis)
                    src.f_write(zapis)
                    return True
                except Exception as e:
                    print("main7(): status_order:  order error=   {}".format(e))
                    #raises: BinanceRequestException, BinanceAPIException
                    return False
            elif in_position and R_T == 'TEST': # МОДЕЛИРОВАНИЕ СДЕЛКИ ACCOUNT=REAL ============================
                #print('main7(): МОДЕЛИРОВАНИЕ СДЕЛКИ ACCOUNT=REAL =====================================================')
                in_position = src.analiz_lim_order(co.client,co.LAST_SIDE,co.LAST_QTY,co.LAST_PRICE)

                zapis = 'model-in_position-STATUS: ОТКРЫТ ОРДЕР id=' + str(co.LAST_ID) + ' ' + co.LAST_TYPE + \
                        ' ' + co.LAST_SIDE + ' ' + str(co.LAST_QTY) + ' ' + str(co.LAST_PRICE + ' in_position=' + \
                        str(in_position))
                print(zapis)
                src.f_write(zapis)

                #print('main5(): model-in_position = АНАЛИЗ позы STRATEGY =' + str(STRATEGY) + '```````````````````````')
                free_usdt = co.BALANCE_T_QUOTE
                change_free_usdt = round(float(co.LAST_QTY) * float(co.LAST_PRICE), 4)
                print('main7():                    Б А Л А Н С Ы ' + '\n' +\
                      '        КВОТИРУЕМАЯ(' + co.QUOTE + ')=' + str(co.BALANCE_T_QUOTE) + ' БАЗОВАЯ(' + \
                    co.BASE + ')=' + str(co.BALANCE_T_BASE) + ' +/- ' + str(change_free_usdt) + '=' +\
                      str(co.LAST_QTY) + '*' + str(co.LAST_PRICE))

                if in_position == False:
                    r_bb = round((co.BALANCE_T_BASE - co.START_bb), 4)
                    r_bq = round((co.BALANCE_T_QUOTE - co.START_bq), 4)

                    print('main7():  BALANCE_T_BASE=' + str(co.BALANCE_T_BASE) + ' - ' + \
                          ' START_bb = ' + str(co.START_bb))
                    print('main7():  BALANCE_T_QUOTE=' + str(co.BALANCE_T_QUOTE) + ' - ' + \
                          ' START_bq = ' + str(co.START_bq))
                    sss = 'main7(): >>>>>>>>>>>>>>>>>>>>>>>>>>моделирование ИЗМЕНЕНИЯ БАЛАНСОВ от СТАРТА: bb= ' + \
                          str(r_bb) + ' / bq= ' + str(r_bq) + '<<<<<<<<<<<<<<<<<<<<<<'
                    print(sss)
                    src.f_write(sss)

                    #a = dt.datetime.now()
                    #b = dt.datetime.now() + dt.timedelta(minutes=5)

                else:
                    print('main7(): NOT MARKET ORDER')
                    print('###########################################################################################')
                    ti.sleep(5) # 3 seconds
            else: #
                print('main7(): not in_position = not Limit -->  открытие позы STRATEGY =' + str(STRATEGY))
                if TEST: # анализ TEST
                    new_free_usdt = co.BALANCE_T_QUOTE
                    free_busd = co.BALANCE_T_BASE
                else: # REAL
                    new_free_usdt = float(
                     co.client.get_asset_balance(asset=co.QUOTE)['free'])  # тек баланс квотируемой валюты
                    free_busd = float(co.client.get_asset_balance(asset=co.BASE)['free'])  # базовой
                    co.BALANCE_QUOTE = free_usdt
                    co.BALANCE_BASE = free_busd
                    free_usdt = new_free_usdt

                print('main7(): =========================== not in_position ===  ' +
                      " balance_QUOTE= {} is {}, balance_BASE= {} is {}".format(co.QUOTE, new_free_usdt,
                                                                                        co.BASE, free_busd))
                print('     3/ ФОРМИРУЕМ ПАРАМЕТРЫ ОРДЕРА: ---------------------------------')
                cur_side, cur_lot, open_price = src.on_the_open7(co.client)
                
                #return cur_side, cur_lot, open_price
                print('     4 /  # Выставляем заявку: BUSDUSDT   LIM_MAKER  ===== TEST ACCOUNT=FALSE R_T= real')
                open_ord = src.limit(co.client,open_price,cur_lot,cur_side)
                print('     main7(): open_ord=' + str(open_ord))    # True /False

                if open_ord:
                    in_position = True
                return

        else: #  is_candle_opened=False #########################################################################3
            print('main(): is_candle_opened=False')
        if TORG:
            #print('#0/main(): current_candle=')
            src.print_current_candle(candle)
    except Exception as e:
        print("Websocket stream error: {}".format(e))
##################################################################################################### START main
ws = websocket.WebSocketApp(co.SOCKET, on_open=src.on_the_open7, on_close=src.on_close, on_message=main7)
ws.run_forever()
#  ----© 2021 GitHub, Inc.  SmartLab made

print('end===============================')