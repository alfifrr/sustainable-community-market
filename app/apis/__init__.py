from .user import user
from .auth import auth
from .address import address
from .product import product
from .balance import balance
from .buy import buy

blueprints = [
    (user, '/api'),
    (auth, '/api'),
    (address, '/api'),
    (product, '/api'),
    (balance, '/api'),
    (buy, '/api')
]
