import random
import config as c
from lib import poloniex, bittrex


class Polo:
    def __init__(self, Key=c.PoloKey, Secret=c.PoloSecret):
        self.p = poloniex.poloniex(Key, Secret)
        self.lotSize = c.lotSize
        self.minSpread = c.downMinSpread
        self.maxSpread = c.downMaxSpread

    def getTicker(self):
        return self.p.returnTicker()

    def getBid(self, ticker, pair=c.poloPair):
        return float(ticker[pair]['highestBid'])

    def getAsk(self, ticker, pair=c.poloPair):
        return float(ticker[pair]['lowestAsk'])

    def getLast(self, ticker, pair=c.poloPair):
        return float(ticker[pair]['last'])

    def getOpenOrders(self, pair=c.poloPair):
        return self.p.returnOpenOrders(pair)

    def getNumOpenOrders(self, orders):
        return len(orders)

    def getCoinBalance(self, coin):
        return float(self.p.returnBalances()[coin])

    def getUpspread(self, min, max):
        return random.uniform(min, max)

    def getDownspread(self, min=c.downMinSpread, max=c.downMaxSpread):
        return random.uniform(min, max)

    def getMinBTCNeeded(self, ticker):
        return float(self.getAsk(ticker)*self.lotSize)

    def getBuyRate(self, ticker):
        return float(self.getBid(ticker)-self.getDownspread())

    def getSellRate(self, ticker):
        return float(self.getAsk(ticker)+self.getDownspread())

    def getFurthestOrderPercentage(self, rate, lastPrice):
        return abs(float(rate)/lastPrice)

    def checkMinBuyAmount(self, ticker, pair=c.poloPair, coin='BTC'):
        if float(self.getCoinBalance(coin)/self.getLast(ticker, pair)) > c.lotSize:
            return True
        else:
            return False

    def makeBuyOrder(self, ticker, rate=0, amountToBuy=0, pair=c.poloPair):
        if ticker and rate==0:
            return self.p.buy(pair, self.getBuyRate(ticker), self.lotSize)
        else:
            return self.p.buy(pair, rate, amountToBuy)

    def makeSellOrder(self, ticker, rate=0, amountToSell=0, pair=c.poloPair):
        if ticker and rate==0:
            return self.p.sell(pair, self.getSellRate(ticker), self.lotSize)
        else:
            return self.p.sell(pair, rate, amountToSell)

    def makeCancelOrder(self, id, pair=c.poloPair):
        return self.p.cancel(pair, id)

class Trex:
    def __init__(self, Key=c.TrexKey, Secret=c.TrexSecret):
        self.b = bittrex.bittrex(Key, Secret)
        self.lotSize = c.trexLotSize
        self.minSpread = c.downMinSpread
        self.maxSpread = c.downMaxSpread

    def getCoinTicker(self):
        return self.b.get_ticker(c.trexPair)

    def getBid(self, ticker):
        return float(ticker['result']['Ask'])

    def getAsk(self, ticker):
        return float(ticker['result']['Bid'])

    def getLast(self, ticker):
        return float(ticker['result']['Last'])

    def getOpenOrders(self):
        return self.b.get_open_orders(c.trexPair)

    def getNumOpenOrders(self, orders):
        return len(orders['result'])

    def getCoinBalance(self, coin):
        return float(self.b.get_balance(coin)['result']['Available'])

    def getUpspread(self, min, max):
        return random.uniform(min, max)

    def getDownspread(self, min=c.downMinSpread, max=c.downMaxSpread):
        return random.uniform(min, max)

    def getMinBTCNeeded(self, ticker):
        return float(self.getAsk(ticker)*self.trexLotSize)

    def getBuyRate(self, ticker):
        return float(self.getBid(ticker)-self.getDownspread())

    def getSellRate(self, ticker):
        return float(self.getAsk(ticker)+self.getDownspread())

    def getFurthestOrderPercentage(self, rate, lastPrice):
        return abs(float(rate) / lastPrice)

    def checkMinBuyAmount(self, ticker, pair=c.trexPair, coin='BTC'):
        if float(self.getCoinBalance(coin) / self.getLast(ticker)) > c.trexLotSize:
            return True
        else:
            return False

    def makeBuyOrder(self, ticker, rate=0, amountToBuy=0, pair=c.trexPair):
        if ticker and rate == 0:
            return self.b.buy_limit(pair, self.lotSize, self.getBuyRate(ticker))
        else:
            return self.b.buy_limit(pair, amountToBuy, rate)

    def makeSellOrder(self, ticker, rate=0, amountToSell=0, pair=c.trexPair):
        if ticker and rate == 0:
            return self.b.sell_limit(pair, self.lotSize, self.getSellRate(ticker))
        else:
            return self.b.sell_limit(pair, amountToSell, rate)

    def makeCancelOrder(self, id):
        return self.b.cancel(id)
#
# t = Trex()
# orders = t.getOpenOrders()
# for order in orders['result']:
#      t.makeCancelOrder(order['OrderUuid'])