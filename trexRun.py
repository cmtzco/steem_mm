from gekko import Trex
import config as c
import urllib2
import logging
import random
import time
import sys
#0.47405412 BTC
logging.basicConfig(filename='gekko.log',level=logging.INFO)
RUNNING = True
while RUNNING:
    try:
        c.lotSize = random.uniform(0.75, 1.25)
        b = Trex(c.TrexKey, c.TrexSecret)
        orders = b.getOpenOrders()

        while RUNNING:
            ticker = b.getCoinTicker()
            btc = b.getCoinBalance('BTC')
            steem = b.getCoinBalance('STEEM')
            steemRate = b.getBuyRate(ticker)
            try:
                orders = b.getOpenOrders()
                if b.checkMinBuyAmount(ticker):
                    bid = b.getBid(ticker)
                    buy = b.makeBuyOrder(ticker)
                    btc_balance = b.getCoinBalance('BTC')
                    steem_balance = b.getCoinBalance('STEEM')
                    orders = b.getOpenOrders()
                    print "[INFO][TREX][MM][BUY] ORDERNUM: {}, BALANCES: {} BTC, {} STEEM, TOTAL OPEN ORDERS: {}".format(buy['result']['uuid'],
                                                                                                                    btc_balance,
                                                                                                                    steem_balance,
                                                                                                                    b.getNumOpenOrders(orders))
                    logging.info("[INFO][TREX][MM][BUY] ORDERNUM: {}, BALANCES: {} BTC, {} STEEM, TOTAL OPEN ORDERS: {}".format(buy['result']['uuid'],
                                                                                                                            btc_balance,
                                                                                                                            steem_balance,
                                                                                                                            b.getNumOpenOrders(orders)))
                elif steem > c.trexLotSize:
                    ask = b.getAsk(ticker)
                    sell = b.makeSellOrder(ticker)
                    btc_balance = b.getCoinBalance('BTC')
                    steem_balance = b.getCoinBalance('STEEM')
                    orders = b.getOpenOrders()
                    print "[INFO][TREX][MM][SELL] ORDERNUM: {}, BALANCES: {} BTC, {} STEEM, TOTAL OPEN ORDERS: {}".format(sell['result']['uuid'],
                                                                                                                    btc_balance,
                                                                                                                    steem_balance,
                                                                                                                    b.getNumOpenOrders(orders))
                    logging.info(
                        "[INFO][TREX][MM][SELL] ORDERNUM: {}, BALANCES: {} BTC, {} STEEM, TOTAL OPEN ORDERS: {}".format(sell['result']['uuid'],
                                                                                                                        btc_balance,
                                                                                                                        steem_balance,
                                                                                                                        b.getNumOpenOrders(orders)))
                    # time.sleep(1)
                    # orders = b.getOpenOrders()
                    # for order in orders['result']:
                    #     print "[INFO][TREX][MM][CANCEL][ORDER] Cancelled Order: {}".format(b.makeCancelOrder(order['OrderUuid']))
                    #     logging.info("[INFO][TREX][MM][CANCEL][ORDER] Cancelled Order: {}".format(b.makeCancelOrder(order['OrderUuid'])))
                else:
                    highscore = 0
                    ids = list()
                    for order in orders['result']:
                        ticker = b.getCoinTicker()
                        last = b.getLast(ticker)
                        furthestOrder = b.getFurthestOrderPercentage(order['limit'], last)
                        if furthestOrder > highscore:
                            highscore = furthestOrder
                            ids.append(order['result']['Uuid'])
                    print "[INFO][TREX][MM][CANCEL] Cancelling the following order IDs: {}".format(ids)
                    logging.info("[INFO][TREX][MM][CANCEL] Cancelling the following order IDs: {}".format(ids))
                    for id in ids:
                        print "[INFO][TREX][MM][CANCEL][ORDER] Cancelled Order: {}".format(b.makeCancelOrder(id))
                        logging.info("[INFO][TREX][MM][CANCEL][ORDER] Cancelled Order: {}".format(b.makeCancelOrder(id)))
                    orders = b.getOpenOrders()
                    print "[INFO][TREX][MM][ORDERS] Total Orders Open After Cancel:{}".format(b.getNumOpenOrders(orders))
                    logging.info("[INFO][TREX][MM][ORDERS] Total Orders Open After Cancel:{}".format(b.getNumOpenOrders(orders)))
                    print "[INFO][TREX][MM][ORDERS] Waiting for opportunity to buy/sell"
            except urllib2.HTTPError as e:
                print "[ERROR][TREX][MM][WHILE][HTTP] {}".format(e)
                logging.error("[ERROR][TREX][MM][WHILE][HTTP] {}".format(e))
                time.sleep(20)
                continue
            except KeyError as e:
                print "[ERROR][TREX][MM][WHILE][KEY] {}".format(e)
                logging.error("[ERROR][TREX][MM][WHILE][KEY] {}".format(e))
                print "[ERROR][TREX][MM][WHILE][ORDERLIMIT]We've hit an order limit, waiting 20s to see if any orders fill{}".format(e)
                logging.error("[ERROR][TREX][MM][WHILE][ORDERLIMIT]We've hit an order limit, waiting 20s to see if any orders fill {}".format(e))
                time.sleep(20)
                pass
            except ValueError as e:
                print "[ERROR][TREX][MM][WHILE][VALUE] {}".format(e)
                logging.error("[ERROR][TREX][MM][WHILE][VALUE] {}".format(e))
                pass
            except TypeError as e:
                print "[ERROR][TREX][MM][WHILE][TYPE] {}".format(e)
                logging.error("[ERROR][TREX][MM][WHILE][TYPE] {}".format(e))
                pass
    except urllib2.HTTPError as e:
        print "[ERROR][TREX][MM][MAIN] {}".format(e)
        logging.error("[ERROR][TREX][MM][MAIN] {}".format(e))
        time.sleep(20)
        RUNNING = True
