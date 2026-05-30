#!/usr/bin/env python3
"""
Generate a small, realistic sales dataset for a Power BI demo dashboard.

Produces a simple star schema (one fact table + four dimension tables) as CSVs
in the same directory as this script:

    fact_sales.csv      grain = one order line
    dim_date.csv        calendar covering the fact date range
    dim_product.csv     product catalog
    dim_region.csv      sales territories
    dim_customer.csv    customers + segment

The data is deterministic (fixed random seed) so re-running reproduces the
same numbers. No third-party packages required.
"""

import csv
import os
import random
from datetime import date, timedelta

SEED = 625  # CS 625 :)
random.seed(SEED)

HERE = os.path.dirname(os.path.abspath(__file__))

START = date(2023, 1, 1)
END = date(2024, 12, 31)
N_ORDERS = 4000

# --- Dimension source data ---------------------------------------------------

# (Category, SubCategory, ProductName, UnitCost, UnitPrice)
PRODUCTS = [
    ("Electronics", "Phones",      "Aurora Smartphone X",   320.00, 699.00),
    ("Electronics", "Phones",      "Aurora Smartphone SE",  180.00, 399.00),
    ("Electronics", "Laptops",     "Nimbus Ultrabook 14",   640.00, 1199.00),
    ("Electronics", "Laptops",     "Nimbus Pro 16",         980.00, 1899.00),
    ("Electronics", "Audio",       "EchoBuds Wireless",      28.00, 89.00),
    ("Electronics", "Audio",       "EchoBuds Pro ANC",       55.00, 179.00),
    ("Electronics", "Wearables",   "PulseWatch Fit",         42.00, 129.00),
    ("Electronics", "Wearables",   "PulseWatch Series 5",    95.00, 299.00),
    ("Home",        "Kitchen",     "BrewMaster Coffee Maker",34.00, 99.00),
    ("Home",        "Kitchen",     "ChopPro Blender",        22.00, 69.00),
    ("Home",        "Lighting",    "LumenDesk Lamp",         12.00, 39.00),
    ("Home",        "Lighting",    "LumenSmart Bulb 4-pack", 14.00, 49.00),
    ("Home",        "Furniture",   "ErgoChair Mesh",        110.00, 329.00),
    ("Home",        "Furniture",   "StandUp Desk 48",       180.00, 499.00),
    ("Apparel",     "Footwear",    "TrailRunner Sneakers",   38.00, 119.00),
    ("Apparel",     "Footwear",    "Glide Court Shoes",      30.00, 95.00),
    ("Apparel",     "Outerwear",   "Summit Down Jacket",     65.00, 199.00),
    ("Apparel",     "Outerwear",   "RainShell Windbreaker",  28.00, 89.00),
    ("Apparel",     "Accessories", "Everyday Backpack",      24.00, 79.00),
    ("Apparel",     "Accessories", "Canvas Tote",             8.00, 29.00),
]

# (Region, Country, City, Manager)
REGIONS = [
    ("West",      "USA",    "San Francisco", "Dana Whitfield"),
    ("West",      "USA",    "Seattle",       "Dana Whitfield"),
    ("East",      "USA",    "New York",      "Marcus Lee"),
    ("East",      "USA",    "Boston",        "Marcus Lee"),
    ("Central",   "USA",    "Chicago",       "Priya Nair"),
    ("Central",   "USA",    "Dallas",        "Priya Nair"),
    ("Canada",    "Canada", "Toronto",       "Olivia Tremblay"),
    ("Canada",    "Canada", "Vancouver",     "Olivia Tremblay"),
]

SEGMENTS = ["Consumer", "Corporate", "Small Business"]

FIRST_NAMES = ["Avery", "Jordan", "Riley", "Casey", "Morgan", "Taylor", "Quinn",
               "Reese", "Hayden", "Rowan", "Skyler", "Emerson", "Finley", "Sage",
               "Devin", "Harper", "Logan", "Parker", "Drew", "Kai"]
LAST_NAMES = ["Nguyen", "Garcia", "Smith", "Patel", "Johnson", "Kim", "Brown",
              "Martinez", "Davis", "Lopez", "Wilson", "Anderson", "Chen",
              "Walker", "Hall", "Young", "Wright", "Khan", "Murphy", "Reed"]


def daterange(start, end):
    days = (end - start).days + 1
    for n in range(days):
        yield start + timedelta(days=n)


def build_customers(n=180):
    rows = []
    used = set()
    cid = 1
    while len(rows) < n:
        name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        if name in used:
            continue
        used.add(name)
        rows.append({
            "CustomerID": f"C{cid:04d}",
            "CustomerName": name,
            "Segment": random.choices(SEGMENTS, weights=[55, 30, 15])[0],
        })
        cid += 1
    return rows


def write_csv(filename, fieldnames, rows):
    path = os.path.join(HERE, filename)
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    print(f"  wrote {filename:22s} {len(rows):>6,} rows")


def main():
    print(f"Generating sales data ({START} .. {END}), seed={SEED}")

    # dim_date
    date_rows = []
    for d in daterange(START, END):
        date_rows.append({
            "Date": d.isoformat(),
            "Year": d.year,
            "Quarter": f"Q{(d.month - 1) // 3 + 1}",
            "MonthNumber": d.month,
            "MonthName": d.strftime("%b"),
            "Day": d.day,
            "DayOfWeek": d.strftime("%a"),
            "IsWeekend": "Yes" if d.weekday() >= 5 else "No",
        })

    # dim_product
    product_rows = []
    for i, (cat, sub, name, cost, price) in enumerate(PRODUCTS, start=1):
        product_rows.append({
            "ProductID": f"P{i:03d}",
            "ProductName": name,
            "Category": cat,
            "SubCategory": sub,
            "UnitCost": f"{cost:.2f}",
            "UnitPrice": f"{price:.2f}",
        })

    # dim_region
    region_rows = []
    for i, (region, country, city, mgr) in enumerate(REGIONS, start=1):
        region_rows.append({
            "RegionID": f"R{i:02d}",
            "Region": region,
            "Country": country,
            "City": city,
            "Manager": mgr,
        })

    # dim_customer
    customer_rows = build_customers()

    # fact_sales
    product_ids = [p["ProductID"] for p in product_rows]
    price_lookup = {p["ProductID"]: float(p["UnitPrice"]) for p in product_rows}
    cost_lookup = {p["ProductID"]: float(p["UnitCost"]) for p in product_rows}
    region_ids = [r["RegionID"] for r in region_rows]
    customer_ids = [c["CustomerID"] for c in customer_rows]
    all_dates = [d["Date"] for d in date_rows]

    # Seasonality weight per month (holiday bump in Nov/Dec, summer dip)
    month_weight = {1: 0.8, 2: 0.8, 3: 0.95, 4: 1.0, 5: 1.05, 6: 0.95,
                    7: 0.9, 8: 0.95, 9: 1.05, 10: 1.1, 11: 1.4, 12: 1.6}
    weighted_dates = []
    for d in date_rows:
        w = int(round(month_weight[d["MonthNumber"]] * 10))
        weighted_dates.extend([d["Date"]] * w)

    fact_rows = []
    for oid in range(1, N_ORDERS + 1):
        pid = random.choice(product_ids)
        order_date = random.choice(weighted_dates)
        qty = random.choices([1, 2, 3, 4, 5, 8, 12], weights=[40, 25, 15, 8, 6, 4, 2])[0]
        unit_price = price_lookup[pid]
        unit_cost = cost_lookup[pid]
        # discounts cluster at 0, with occasional promo discounts
        discount = random.choices([0.0, 0.05, 0.10, 0.15, 0.20],
                                  weights=[55, 18, 14, 8, 5])[0]
        gross = unit_price * qty
        sales = round(gross * (1 - discount), 2)
        cogs = round(unit_cost * qty, 2)
        profit = round(sales - cogs, 2)
        fact_rows.append({
            "OrderID": f"SO{oid:05d}",
            "OrderDate": order_date,
            "ProductID": pid,
            "RegionID": random.choice(region_ids),
            "CustomerID": random.choice(customer_ids),
            "Quantity": qty,
            "UnitPrice": f"{unit_price:.2f}",
            "Discount": f"{discount:.2f}",
            "SalesAmount": f"{sales:.2f}",
            "COGS": f"{cogs:.2f}",
            "Profit": f"{profit:.2f}",
        })

    fact_rows.sort(key=lambda r: r["OrderDate"])

    write_csv("dim_date.csv",
              ["Date", "Year", "Quarter", "MonthNumber", "MonthName", "Day",
               "DayOfWeek", "IsWeekend"], date_rows)
    write_csv("dim_product.csv",
              ["ProductID", "ProductName", "Category", "SubCategory",
               "UnitCost", "UnitPrice"], product_rows)
    write_csv("dim_region.csv",
              ["RegionID", "Region", "Country", "City", "Manager"], region_rows)
    write_csv("dim_customer.csv",
              ["CustomerID", "CustomerName", "Segment"], customer_rows)
    write_csv("fact_sales.csv",
              ["OrderID", "OrderDate", "ProductID", "RegionID", "CustomerID",
               "Quantity", "UnitPrice", "Discount", "SalesAmount", "COGS",
               "Profit"], fact_rows)

    total_sales = sum(float(r["SalesAmount"]) for r in fact_rows)
    total_profit = sum(float(r["Profit"]) for r in fact_rows)
    print(f"Done. Total sales ${total_sales:,.0f} | total profit ${total_profit:,.0f}")


if __name__ == "__main__":
    main()
