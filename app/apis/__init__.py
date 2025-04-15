from .user import user
from .auth import auth
from .address import address

blueprints = [
    (user, '/api'),
    (auth, '/api'),
    (address, '/api')
]
