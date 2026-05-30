# Power BI — Sales Dashboard Kit

Everything you need to build a polished sales dashboard in **Power BI Desktop**,
minus the binary `.pbix` file (which can only be authored inside the Power BI
GUI — see the note in the build guide).

## What's here

| File | What it is |
| ---- | ---------- |
| [`dashboard-build-guide.md`](dashboard-build-guide.md) | **Start here.** Step-by-step build: load → model → theme → DAX → layout → polish → publish. |
| [`theme.json`](theme.json) | The *Aurora Sales* custom report theme. Import via **View → Themes → Browse**. |
| [`data/`](data/) | A star-schema sample sales dataset (5 CSVs) + the script that generates it. |

## Quick start

1. Open **Power BI Desktop**.
2. **Get data → Text/CSV** → import the five files in `data/`.
3. **View → Themes → Browse for themes** → pick `theme.json`.
4. Follow [`dashboard-build-guide.md`](dashboard-build-guide.md) from Step 2.

## The dataset at a glance

- **Grain:** one row per order line in `fact_sales` (4,000 rows).
- **Dimensions:** date (2 yrs), product (20 SKUs), region (8 cities), customer (180).
- **Totals:** ~$3.15M sales, ~$1.69M profit, with built-in seasonality (holiday bump).
- **Reproducible:** `python3 data/generate_sales_data.py` (standard library only, seed = 625).
