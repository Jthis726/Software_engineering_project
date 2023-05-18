class Product:
    id_generator = 0;
    product_list = []
    coin_list={}
    def __init__(self, id, coin, price, user_id):
        self.id = id
        self.coin = coin
        self.price = price
        self.user_id = user_id
    
    @classmethod
    def add_product(cls, coin, price, user_id):
        id = cls.id_generator
        cls.id_generator += 1
        if(coin in cls.coin_list.keys()):
            cls.coin_list[coin].append(id)
            cls.product_list.append(Product(id, coin, price, user_id))
        else:
            cls.coin_list[coin]=[]
            cls.coin_list[coin].append(id)
            cls.product_list.append(Product(id, coin, price, user_id))
        return id
    
    @classmethod
    def search(cls, id):
        for product in cls.product_list:
            if id == product.id:
                return product
        return None

    @classmethod
    def buy(cls, id):
        for idx, product in enumerate(cls.product_list):
            if id == product.id:
                cls.product_list.pop(idx)

    @classmethod
    def delete(cls, id):
        for idx, product in enumerate(cls.product_list):
            if id == product.id:
                cls.product_list.pop(idx)

    # def __repr__(self):
    #     return self.id

