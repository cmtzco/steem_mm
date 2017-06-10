import wrapper
import time
import random
import config as c

class Polo:
    def __init__(self, Key=c.Key, Secret=c.Secret):
        self.p = wrapper.poloniex(Key, Secret)
        self.lotSize = c.lotSize
        self.minSpread = c.downMinSpread
        self.maxSpread = c.downMaxSpread

    def getTicker(self):
        return self.p.returnTicker()

    def getBid(self, ticker, pair=c.pair):
        return float(ticker[pair]['highestBid'])

    def getAsk(self, ticker, pair=c.pair):
        return float(ticker[pair]['lowestAsk'])

    def getLast(self, ticker, pair=c.pair):
        return float(ticker[pair]['last'])

    def getOpenOrders(self, pair=c.pair):
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
        return float(rate/lastPrice)

    def makeBuyOrder(self, ticker, rate=0, amountToBuy=0, pair=c.pair):
        if ticker and rate==0:
            return self.p.buy(pair, self.getBuyRate(ticker), self.lotSize)
        else:
            return self.p.buy(pair, rate, amountToBuy)

    def makeSellOrder(self, ticker, rate=0, amountToBuy=0, pair=c.pair):
        if ticker and rate==0:
            return self.p.buy(pair, self.getBuyRate(ticker), self.lotSize)
        else:
            return self.p.buy(pair, rate, amountToBuy)

    def makeCancelOrder(self, id, pair=c.pair):
        return self.p.cancel(pair, id)










