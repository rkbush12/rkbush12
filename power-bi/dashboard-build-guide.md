# Building a Gorgeous Power BI Sales Dashboard

A step-by-step guide to turning the sample data in this folder into a polished,
executive-ready sales dashboard in **Power BI Desktop**. Every measure, layout
coordinate, and formatting tweak you need is spelled out below — follow it
top to bottom and you'll end up with something that looks like it came out of a
consulting deck.

> **Why there's no `.pbix` file here:** A `.pbix` is a binary file authored
> interactively inside Power BI Desktop (a Windows GUI app). It can't be
> hand-written or generated from a script. What this folder *does* give you is
> everything that goes *into* one: clean data, a custom theme, and this guide.

---

## Contents of this folder

```
power-bi/
├── theme.json                    # Custom "Aurora Sales" report theme
├── dashboard-build-guide.md      # This guide
└── data/
    ├── generate_sales_data.py    # Reproducible data generator (seed = 625)
    ├── fact_sales.csv            # 4,000 order lines (the fact table)
    ├── dim_date.csv              # Calendar 2023-01-01 .. 2024-12-31
    ├── dim_product.csv           # 20 products across 3 categories
    ├── dim_region.csv            # 8 territories / 4 regions
    └── dim_customer.csv          # 180 customers across 3 segments
```

The data is a classic **star schema**: one fact table (`fact_sales`) surrounded
by four dimension tables. Totals across the sample: **~$3.15M in sales** and
**~$1.69M in profit** over two years.

---

## Prerequisites

- **Power BI Desktop** (free) — Windows only. Download from
  <https://powerbi.microsoft.com/desktop/>. (On macOS/Linux, run it in a
  Windows VM or use Power BI Service in a browser, though the theme/format steps
  below assume Desktop.)
- The CSV files in `data/`.
- The `theme.json` file in this folder.

---

## Step 1 — Load the data

1. Open Power BI Desktop → **Home → Get data → Text/CSV**.
2. Import each of the five CSVs in `data/`. For each one, click
   **Transform Data** (not just *Load*) so you land in **Power Query**.
3. In Power Query, confirm the data types (Power BI usually auto-detects, but
   verify):
   - `fact_sales`: `OrderDate` = **Date**; `Quantity` = **Whole Number**;
     `UnitPrice`, `Discount`, `SalesAmount`, `COGS`, `Profit` = **Decimal Number**.
   - `dim_date`: `Date` = **Date**; `Year`, `MonthNumber`, `Day` = **Whole Number**.
   - `dim_product`: `UnitCost`, `UnitPrice` = **Decimal Number**.
4. **Close & Apply**.

---

## Step 2 — Build the model (relationships)

Go to **Model view** (the diagram icon on the left). Create these relationships
by dragging the key from the dimension onto the matching key in `fact_sales`.
All are **one-to-many**, single-direction (dimension → fact):

| From (one side)        | To (many side)          |
| ---------------------- | ----------------------- |
| `dim_date[Date]`       | `fact_sales[OrderDate]` |
| `dim_product[ProductID]`| `fact_sales[ProductID]`|
| `dim_region[RegionID]` | `fact_sales[RegionID]`  |
| `dim_customer[CustomerID]`| `fact_sales[CustomerID]`|

Then mark the calendar as a date table: select `dim_date` →
**Table tools → Mark as date table** → choose the `Date` column. This makes
time-intelligence measures (YTD, prior year) reliable.

---

## Step 3 — Apply the custom theme

This is what makes the report look designed instead of default.

1. **View → Themes → Browse for themes**.
2. Select `theme.json` from this folder.

You'll immediately get the *Aurora Sales* look: a soft blue-grey page
background (`#F4F7FB`), white cards with rounded 12px corners and a subtle drop
shadow, a blue→teal→amber categorical palette, and Segoe UI Semibold titles.
Conditional-formatting colors are pre-wired too (`good` = green, `bad` = red),
so KPI logic picks up sensible colors automatically.

---

## Step 4 — Create the core DAX measures

Right-click `fact_sales` → **New measure** for each. (Keeping all measures on
the fact table keeps the field list tidy.)

```dax
Total Sales = SUM ( fact_sales[SalesAmount] )

Total Profit = SUM ( fact_sales[Profit] )

Total Cost = SUM ( fact_sales[COGS] )

Order Count = DISTINCTCOUNT ( fact_sales[OrderID] )

Units Sold = SUM ( fact_sales[Quantity] )

Profit Margin % =
DIVIDE ( [Total Profit], [Total Sales] )

Avg Order Value =
DIVIDE ( [Total Sales], [Order Count] )
```

Time intelligence (these rely on Step 2's date table):

```dax
Sales PY =
CALCULATE ( [Total Sales], SAMEPERIODLASTYEAR ( dim_date[Date] ) )

Sales YoY % =
DIVIDE ( [Total Sales] - [Sales PY], [Sales PY] )

Sales YTD =
TOTALYTD ( [Total Sales], dim_date[Date] )
```

Format them: select each measure → **Measure tools → Format**.
- `Total Sales`, `Total Profit`, `Total Cost`, `Avg Order Value`, `Sales PY`,
  `Sales YTD` → **Currency**, 0 decimals.
- `Profit Margin %`, `Sales YoY %` → **Percentage**, 1 decimal.
- `Order Count`, `Units Sold` → **Whole Number**, comma separator.

---

## Step 5 — Lay out the canvas

Set the page size first: **Format → Canvas settings → Type = 16:9** (the
default 1280×720). Think of the page as a grid with generous margins.

Suggested layout (top to bottom):

```
┌──────────────────────────────────────────────────────────────┐
│  Sales Performance Overview            [Year ▾] [Region ▾]     │  ← title + slicers
├───────────┬───────────┬───────────┬───────────┬───────────────┤
│  Total    │  Total    │  Profit   │  Avg Order │   Sales YoY % │  ← 5 KPI cards
│  Sales    │  Profit   │  Margin   │  Value     │               │
├───────────────────────────────────┬────────────────────────────┤
│  Sales & Profit over time          │  Sales by Category         │  ← line + bar
│  (line/area chart)                 │  (bar chart)               │
├───────────────────────────────────┼────────────────────────────┤
│  Sales by Region (map or bar)      │  Top Products (table)      │  ← map + table
└───────────────────────────────────┴────────────────────────────┘
```

---

## Step 6 — Add the visuals

For each, drop the visual from the **Visualizations** pane, then drag fields in.

1. **KPI cards (×5)** — use the new **Card (new)** visual.
   - Card 1: `Total Sales` · Card 2: `Total Profit` · Card 3: `Profit Margin %`
     · Card 4: `Avg Order Value` · Card 5: `Sales YoY %`.
   - For *Sales YoY %*, add conditional formatting on the callout value:
     **Format → Callout value → fx** → Format by **Rules** → ≥ 0 → `good` green,
     < 0 → `bad` red.

2. **Sales & Profit over time** — **Line and stacked column** or **Area chart**.
   - X axis: `dim_date[MonthName]` (or build a `Year-Month` sort column).
   - Values: `Total Sales` and `Total Profit`.
   - Tip: sort the X axis by `MonthNumber` so months read Jan→Dec, not
     alphabetically.

3. **Sales by Category** — **Clustered bar chart**.
   - Y axis: `dim_product[Category]`. X axis: `Total Sales`.
   - Sort descending by `Total Sales`. Turn on **Data labels**.

4. **Sales by Region** — **Map** (bubble) *or* a clustered bar.
   - Map: Location = `dim_region[City]`, Bubble size = `Total Sales`,
     Legend = `dim_region[Region]`.
   - Simpler/cleaner: clustered bar with `Region` on the axis.

5. **Top Products** — **Table** visual.
   - Columns: `dim_product[ProductName]`, `Total Sales`, `Units Sold`,
     `Profit Margin %`.
   - Add a **Top N** filter on `ProductName` by `Total Sales`, Top 10.
   - Apply **data bars** conditional formatting to `Total Sales` for a mini
     in-cell chart.

6. **Slicers (×2)** — drop two **Slicer** visuals at the top right.
   - `dim_date[Year]` (set style to **Tile / horizontal**).
   - `dim_region[Region]` (dropdown).

---

## Step 7 — Polish (this is the "gorgeous" part)

The theme does the heavy lifting, but these finishing touches separate a good
dashboard from a great one:

- **Alignment.** Select multiple visuals → **Format → Align** to snap edges.
  Equal spacing between the five KPI cards matters more than anything else.
- **Consistent number formats.** Money with no decimals on cards; percentages
  to one decimal. Don't mix.
- **One accent color for "the answer."** The theme makes blue (`#2E5FE8`) the
  hero color. Use it sparingly so the eye knows where to land.
- **Title bar.** Add a **Text box** across the top: *"Sales Performance
  Overview"* in 20pt Segoe UI Semibold, plus a smaller subtitle with the date
  range. Or add a thin colored **Shape → Rectangle** banner behind it.
- **Whitespace.** Resist filling every pixel. The soft grey background +
  floating white cards needs breathing room to look premium.
- **Tooltips.** Turn on for charts; consider a **report-page tooltip** showing
  profit detail on hover.
- **Interactions.** Click a category bar and watch the other visuals
  cross-filter — verify this behaves (Format → **Edit interactions**).

---

## Step 8 — Save and (optionally) publish

1. **File → Save as** → `Sales-Dashboard.pbix` (keep it *out* of this content
   repo unless you specifically want the binary tracked — `.pbix` files are
   large and don't diff well in git).
2. To share: **Home → Publish** → sign in → pick a workspace. This pushes the
   report to the Power BI Service where you can pin visuals to a dashboard and
   share a link.

---

## Design principles (the CS 625 angle)

If you're using this for a data-visualization writeup, here's the *why* behind
the choices — tie these back to course concepts:

- **Visual hierarchy / preattentive attributes.** Size and a single saturated
  hue draw the eye to KPIs first, then to trends. Color is used to *encode*, not
  to decorate.
- **Expressiveness & effectiveness (Mackinlay).** Position and length (bars,
  lines) carry the quantitative comparisons; color is reserved for category and
  for good/bad status — never for quantity on its own.
- **Data-ink ratio (Tufte).** Gridlines are faint, borders are subtle, chart
  junk is removed. Every pixel of ink should carry information.
- **Small multiples & consistency.** Repeated card shapes and aligned axes let
  the viewer compare without re-learning the layout each time.
- **Sorting communicates.** Ranked bars (descending) and a chronologically
  sorted time axis make the takeaway readable in seconds.

---

## Regenerating the data

The dataset is deterministic. To rebuild it (or change the size/date range,
edit the constants at the top of the script):

```bash
python3 power-bi/data/generate_sales_data.py
```

No third-party packages are required — it uses only the Python standard library.
