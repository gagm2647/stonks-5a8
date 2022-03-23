class Item:
    def __init__(self, itemId, price):
        self.id = itemId
        self.price = price
        self.totalItemSold = 0

    def updateItemSold(self, itemSold):
        if itemSold > 0:
            self.totalItemSold += itemSold
