from item import Item
from errors import *


class ShoppingCart:
    def __init__(self):
        """initials object list as shopping cart """
        self.cart = []

    def add_item(self, item: Item):
        """if the item is aalrady in the cart raises an error else adds the item"""
        if item in self.cart:
            raise ItemAlreadyExistsError
        self.cart.append(item)

    def remove_item(self, item_name: str):
        """we try to remove the item if its in the list and then we check if the item was removed if not we raise an
        error"""
        size_check = len(self.cart)
        for Item in self.cart:
            if Item.name == item_name:
                self.cart.remove(Item)
        if size_check == len(self.cart):
            raise ItemNotExistError

    def get_subtotal(self) -> int:
        """adds the price fild of every item in the cart and returns the sum"""
        bil = 0
        for item in self.cart:
            bil += item.price
        return bil

    def not_in_cart(self, item_name: str) -> bool:
        """returns true if the item is not in the cart
        we check for every item in the list if the item name is equal to the given str if so we return false"""
        for Item in self.cart:
            if Item.name == item_name:
                return False
        return True
