import yaml
from errors import *
from item import Item
from shopping_cart import ShoppingCart


def sort_by_tag(tag: list, tag_list: list) -> int:
    """tag is a list and tag_list is a list of lists so we check for evey str in tag and for evey list in tag_list
    the amount of times the str appears in the list and for evey str in tag we do so and return the sum of
    appearances """
    appearances = 0
    for tag1 in tag:
        for tag2 in tag_list:
            appearances += tag2.count(tag1)
    return appearances


class Store:
    def __init__(self, path):
        with open(path) as inventory:
            items_raw = yaml.load(inventory, Loader=yaml.FullLoader)['items']
        self._items = self._convert_to_item_objects(items_raw)
        self._shopping_cart = ShoppingCart()

    @staticmethod
    def _convert_to_item_objects(items_raw):
        return [Item(item['name'],
                     int(item['price']),
                     item['hashtags'],
                     item['description'])
                for item in items_raw]

    def get_items(self) -> list:
        return self._items

    def search_by_name(self, item_name: str) -> list:
        """first we biuld a list using list comprianson for every x we add we check if the given str is a substring
        of x.name and if x is already in the cart then we sort by name then we build a list of hashtag lists from the
        current cart and sort by the number of matches. we return a sorted list """
        ans = [x for x in self._items if
               (item_name in x.name) & (ShoppingCart.not_in_cart(self._shopping_cart, x.name))]
        ans.sort(key=lambda item: item.name)
        list_tag = [x.hashtags for x in self._shopping_cart.cart]
        ans.sort(key=lambda item: sort_by_tag(item.hashtags, list_tag), reverse=True)
        return ans

    def search_by_hashtag(self, hashtag: str) -> list:
        """first we biuld a list using list comprianson for every x we add we check if the given hashtag is in
        x.hashtags (in the list) and if x is already in the cart then we sort by name then we build a list of hashtag
        lists from the current cart and sort by the number of matches. we return a sorted list """
        ans = [x for x in self._items if
               (hashtag in x.hashtags) & (ShoppingCart.not_in_cart(self._shopping_cart, x.name))]
        ans.sort(key=lambda item: item.name)
        list_tag = [x.hashtags for x in self._shopping_cart.cart]
        ans.sort(key=lambda item: sort_by_tag(item.hashtags, list_tag), reverse=True)
        return ans

    def add_item(self, item_name: str):
        """first we build a list of all the items from the store that the given str is a substring of there name then we
        check if the size of the list is different then one if so we raise an error else we add the item from the list
        using add item from shopping cart class """
        temp_list = [x for x in self._items if (item_name in x.name)]
        if len(temp_list) == 0:
            raise ItemNotExistError
        elif len(temp_list) > 1:
            raise TooManyMatchesError
        else:
            ShoppingCart.add_item(self._shopping_cart, temp_list[0])

    def remove_item(self, item_name: str):
        """first we build a list of all the items from the store that the given str is a substring of there name then
        we check if the size of the list is different then one if so we raise an error else we remove the item from
        the list using remove item from shopping cart class """
        temp_list = [x for x in self._items if (item_name in x.name)]
        if len(temp_list) == 0:
            raise ItemNotExistError
        elif len(temp_list) > 1:
            raise TooManyMatchesError
        ShoppingCart.remove_item(self._shopping_cart, item_name)

    def checkout(self) -> int:
        """returns the sum of all item preses that are in the cart"""
        return ShoppingCart.get_subtotal(self._shopping_cart)
