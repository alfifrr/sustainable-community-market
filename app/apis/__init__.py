from .user import user
from .auth import auth
from .address import address
from .product import product
from .balance import balance
from .buy import buy
from .manage_status import manage_status
from .confirm_delivery import confirm_delivery
from .history import history
from .category import category
from .manage_address import manage_address
from .cancel import cancel
from .manage_product import manage_product
from .user_profile import profile
from .processed_products import processed_products
from .product_review import product_review

blueprints = [
    (user, "/api"),
    (auth, "/api"),
    (address, "/api"),
    (product, "/api"),
    (balance, "/api"),
    (buy, "/api"),
    (manage_status, "/api"),
    (confirm_delivery, "/api"),
    (history, "/api"),
    (category, "/api"),
    (manage_address, "/api"),
    (cancel, "/api"),
    (manage_product, "/api"),
    (profile, "/api"),
    (processed_products, "/api"),
    (product_review, "/api"),
]
