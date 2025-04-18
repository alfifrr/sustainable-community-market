from .user import user
from .auth import auth
from .address import address
from .product import product
from .balance import balance
from .buy import buy
from .manage_status import manage_status
from .confirm_delivery import confirm_delivery

blueprints = [
    (user, '/api'),
    (auth, '/api'),
    (address, '/api'),
    (product, '/api'),
    (balance, '/api'),
    (buy, '/api'),
    (manage_status, '/api'),
    (confirm_delivery, '/api')
]
