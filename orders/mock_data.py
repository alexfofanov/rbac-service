from orders.models import Order

MOCK_ORDERS = [
    Order(obj_id=1, product_name='Ноутбук', quantity=2, owner_id=1),
    Order(obj_id=2, product_name='Монитор', quantity=1, owner_id=2),
    Order(obj_id=3, product_name='Клавиатура', quantity=5, owner_id=3),
    Order(obj_id=4, product_name='Мышь', quantity=10, owner_id=2),
    Order(obj_id=5, product_name='Монитор 4K', quantity=1, owner_id=1),
    Order(obj_id=6, product_name='Ноутбук игровой', quantity=3, owner_id=3),
]
