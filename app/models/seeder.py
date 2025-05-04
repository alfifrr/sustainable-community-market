from app.models import Category, Role, RoleType
from app import db


def seed_product_categories():
    default_categories = [
        {
            "name": "Meals and Snacks",
            "description": "Ready-to-eat foods, bread, packaged snacks, prepared meals, and food products",
        },
        {
            "name": "Drinks and Beverages",
            "description": "All types of drinks including water, juice, coffee, tea, and other beverages",
        },
        {
            "name": "Grains and Staples",
            "description": "Rice, flour, noodles, cereals, and other basic food ingredients",
        },
        {
            "name": "Protein and Dairy",
            "description": "Meats, eggs, cheese, milk, tofu, tempeh, and other protein products",
        },
        {
            "name": "Vegetables and Fruits",
            "description": "Fresh and frozen vegetables, fruits, and related agricultural products",
        },
        {
            "name": "Seasonings and Condiments",
            "description": "Spices, herbs, sauces, cooking oils, and flavor enhancers",
        },
        {
            "name": "Clothing and Gear",
            "description": "Apparel, accessories, bags, shoes, raincoat, and personal equipment",
        },
        {
            "name": "Tools",
            "description": "Household and kitchen tools, gardening equipment, and utility items",
        },
        {
            "name": "Hygiene and Cleaning",
            "description": "Personal care items, toiletries, cleaning supplies, and sanitation products",
        },
    ]

    for category in default_categories:
        exists = Category.query.filter_by(name=category["name"]).first()
        if not exists:
            new_category = Category(
                name=category["name"], description=category["description"]
            )
            db.session.add(new_category)

    try:
        db.session.commit()
        print("Categories seeded successfully")
    except Exception as e:
        db.session.rollback()
        print(f"Error seeding categories: {str(e)}")


def seed_roles():
    default_roles = [
        {
            "name": RoleType.ADMIN,
            "description": "System administrator with full access",
        },
        {"name": RoleType.SELLER, "description": "Verified seller account"},
        {"name": RoleType.BUYER, "description": "Regular user account"},
        {
            "name": RoleType.EXPEDITION,
            "description": "Delivery and logistics service provider account",
        },
    ]

    for role in default_roles:
        exists = Role.query.filter_by(name=role["name"]).first()
        if not exists:
            new_role = Role(name=role["name"], description=role["description"])
            db.session.add(new_role)

    try:
        db.session.commit()
        print("Roles seeded successfully")
    except Exception as e:
        db.session.rollback()
        print(f"Error seeding roles: {str(e)}")
