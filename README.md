# Superstore Regional Profitability Analysis

This analysis identifies which regions and product categories increase or decrease profit, and flags a data-quality issue that significantly influences the performance numbers. I merged three data sheets (Orders, Returns, Users), then grouped by Region and Product Category to calculate Total Sales, Profit, and Unique Orders.

Three regions showed similar profitability — East ($85,291.40), Central ($77,365.47), West ($75,844.79) — all profitable across every category. South's raw total profit was -$14,424.05, the only region at a loss. But $16,476.84 of that comes from a single transaction (Row 975, South Technology) whose Product Name field is corrupted (literal value "5165"). Excluding it brings South's total to +$2,052.78 — still far below the other regions, but no longer a loss.

The verified loss driver is three high-ticket SKUs, each appearing twice among the 10 worst-profit transactions: Polycom ViewStation ($6,783.02/unit, 2× West), Okidata Pacemark 4410N ($3,502.14/unit, 2× West), and Epson DFX-8500 ($2,550.14/unit, 1× West, 1× Central). These are West-concentrated and should not be read as the cause of South's number. Discount (1-10%) and Product Base Margin (0.39-0.57, not thin) on these SKUs don't explain the losses.

**Recommended:** correct or exclude Row 975 before any regional profit reporting, and flag the source system for the Product Name corruption; investigate actual per-unit cost on the three loss-driving SKUs before any pricing action; and treat South as a scoped underperformance review, not a crisis — it is profitable post-correction, just far behind its peers.

**Limitations:** no unit-cost field exists for profit calculations; Returns barely joins to Orders (11 of 1,634 matched); Row 975 suggests other data-quality issues may exist uncaught.

## What this demonstrates
- Cardinality-checked merges across 3 data sources before joining
- Multi-key groupby / named aggregation
- Spearman correlation + descriptive stats
- Isolating a data-quality artifact from a genuine business finding (not conflating the two)
- Client-facing written insight under a strict word cap

## Files
- `superstore_analysis.py` — full analysis script
- `Profit_Region&Category.png` — bar chart, total profit by region + category
- `Profit_UnitPrice.png` — scatter, unit price vs. profit (log-x, symlog-y)

**Tools:** Python, pandas, matplotlib
