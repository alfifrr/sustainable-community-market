# Sustainable Community Market API

A community-driven marketplace API focusing on reducing food waste by implementing dynamic pricing for perishable goods. This platform enables users to buy and sell food items with automatic price reductions as products approach their expiration dates.

## Table of Contents

- [Sustainable Community Market API](#sustainable-community-market-api)
  - [Table of Contents](#table-of-contents)
  - [Using UV Package Manager](#using-uv-package-manager)
  - [Swagger API Documentation](#swagger-api-documentation)
  - [Note](#note)
  - [Dynamic Pricing System](#dynamic-pricing-system)

## Using UV Package Manager

Copy and configure the environment file, then add the database provider and mailing service of your choice first:

```bash
cp .env.example .env
```

Create a virtual environment using UV and run Flask application:

```bash
uv venv
source .venv/bin/activate # Linux
uv pip install -r pyproject.toml
flask run
```

## Swagger API Documentation

For complete API documentation, visit [Swagger Documentation](https://sustainable-community-market.onrender.com/api/docs).

## Note

- Purchasing a product (`/api/buy`) costs additional fixed delivery and service fee of `Rp. 15,000`
- Delivery and service fee will be fully returned upon order cancellation (`/api/cancel`)

## Dynamic Pricing System

Products are automatically discounted based on their remaining days until expiration:

| Days Until Expiration | Discount | Final Price            |
| --------------------- | -------- | ---------------------- |
| > 4 days              | 0%       | 100% of original price |
| 4 days                | 20%      | 80% of original price  |
| 3 days                | 40%      | 60% of original price  |
| 2 days                | 60%      | 40% of original price  |
| 1 day                 | 80%      | 20% of original price  |
| 0 days (today)        | 90%      | 10% of original price  |
| Expired               | -        | Not available for sale |

Example:

- Original price: Rp 100,000
- 3 days until expiration: Rp 60,000 (40% discount)
- 1 day until expiration: Rp 20,000 (80% discount)
