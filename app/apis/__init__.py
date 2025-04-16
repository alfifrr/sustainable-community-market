from .user import user
from .auth import auth
from .address import address
from .product import product

blueprints = [
    (user, '/api'),
    (auth, '/api'),
    (address, '/api'),
    (product, '/api')
]
