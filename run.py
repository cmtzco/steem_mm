from gekko import Polo
import config as c


p = Polo(c.Key, c.Secret)
orders = p.getOpenOrders()
for order in orders:
    print order['orderNumber']