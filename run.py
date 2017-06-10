from gekko import Polo
import config as c
import urllib2
import logging
import time
#0.04985619 BTC


logging.basicConfig(filename='gekko.log',level=logging.INFO)
RUNNING = True
while RUNNING:
    try:
        p = Polo(c.PoloKey, c.PoloSecret)
        orders = p.getOpenOrders()
        # for order in orders:
        #     print order['orderNumber']

        while RUNNING:
            ticker = p.getTicker()
            btc = p.getCoinBalance('BTC')
            steem = p.getCoinBalance('STEEM')
            steemRate = p.getBuyRate(ticker)
            # print btc, steemRate
            try:
                orders = p.getOpenOrders()
                # print "[INFO][POLO][MM][ORDERS] Total Orders Open:{}".format(p.getNumOpenOrders(orders))
                if p.checkMinBuyAmount(ticker):
                    bid = p.getBid(ticker)
                    buy = p.makeBuyOrder(ticker)
                    btc_balance = p.getCoinBalance('BTC')
                    steem_balance = p.getCoinBalance('STEEM')
                    orders = p.getOpenOrders()
                    print "[INFO][POLO][MM][BUY] ORDERNUM: {}, BALANCES: {} BTC, {} STEEM, TOTAL OPEN ORDERS: {}".format(buy['orderNumber'],
                                                                                                                   btc_balance,
                                                                                                                   steem_balance,
                                                                                                                   p.getNumOpenOrders(orders))
                    logging.info("[INFO][POLO][MM][BUY] ORDERNUM: {}, BALANCES: {} BTC, {} STEEM, TOTAL OPEN ORDERS: {}".format(buy['orderNumber'],
                                                                                                                   btc_balance,
                                                                                                                   steem_balance,
                                                                                                                   p.getNumOpenOrders(orders)))

                    if steem > c.lotSize:
                        ask = p.getAsk(ticker)
                        sell = p.makeSellOrder(ticker)
                        btc_balance = p.getCoinBalance('BTC')
                        steem_balance = p.getCoinBalance('STEEM')
                        orders = p.getOpenOrders()
                        print "[INFO][POLO][MM][SELL] ORDERNUM: {}, BALANCES: {} BTC, {} STEEM, TOTAL OPEN ORDERS: {}".format(sell['orderNumber'],
                                                                                                                        btc_balance,
                                                                                                                        steem_balance,
                                                                                                                        p.getNumOpenOrders(orders))
                        logging.info("[INFO][POLO][MM][SELL] ORDERNUM: {}, BALANCES: {} BTC, {} STEEM, TOTAL OPEN ORDERS: {}".format(sell['orderNumber'],
                                                                                                                        btc_balance,
                                                                                                                        steem_balance,
                                                                                                                        p.getNumOpenOrders(orders)))
                else:
                    highscore = 0
                    ids = list()
                    for order in orders:
                        ticker = p.getTicker()
                        last = p.getLast(ticker)
                        furthestOrder = p.getFurthestOrderPercentage(order['rate'], last)
                        if furthestOrder > highscore:
                            highscore = furthestOrder
                            ids.append(order['orderNumber'])

                    print "[INFO][POLO][MM][CANCEL] Cancelling the following order IDs: {}".format(ids)
                    logging.info("[INFO][POLO][MM][CANCEL] Cancelling the following order IDs: {}".format(ids))
                    for id in ids:
                        print "[INFO][POLO][MM][CANCEL][ORDER] Cancelled Order: {}".format(p.makeCancelOrder(id))
                        logging.info("[INFO][POLO][MM][CANCEL][ORDER] Cancelled Order: {}".format(p.makeCancelOrder(id)))
                    orders = p.getOpenOrders()
                    print "[INFO][POLO][MM][ORDERS] Total Orders Open After Cancel:{}".format(p.getNumOpenOrders(orders))
                    logging.info("[INFO][POLO][MM][ORDERS] Total Orders Open After Cancel:{}".format(p.getNumOpenOrders(orders)))
            except urllib2.HTTPError as e:
                print "[ERROR][POLO][MM][WHILE] {}".format(e)
                logging.error("[ERROR][POLO][MM][WHILE] {}".format(e))
                time.sleep(20)
                continue
            except KeyError:
                pass
    except urllib2.HTTPError as e:
        print "[ERROR][POLO][MM][MAIN] {}".format(e)
        logging.error("[ERROR][POLO][MM][MAIN] {}".format(e))
        time.sleep(20)
        RUNNING = True
