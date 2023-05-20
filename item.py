class Item:
    def __init__(self, item_name: str, item_price: int, item_hashtags: list, item_description: str):
        self.name = item_name
        self.price = item_price
        self.hashtags = item_hashtags
        self.description = item_description

    def __str__(self) -> str:
        return f'Name:\t\t\t{self.name}\n' \
               f'Price:\t\t\t{self.price}\n' \
               f'Description:\t{self.description}'

