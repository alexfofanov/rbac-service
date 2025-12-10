class Order:
    element_name = 'order'

    def __init__(
        self, obj_id: int, product_name: str, quantity: int, owner_id: int
    ) -> None:
        self.id = obj_id
        self.product_name = product_name
        self.quantity = quantity
        self.owner_id = owner_id
