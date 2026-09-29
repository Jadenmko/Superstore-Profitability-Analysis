
# Superstore Regional Profitability Analysis

**Research question:** which regions and product categories are driving or dragging profit, and is the sub-$0 region a real underperformer or a data artifact?

**Dataset:** `SuperStoreUS-2015.xlsx` — 3 sheets (Orders: 1,952 order-line rows, Returns: 1,634 rows, Users: 4 rows). Merged Orders → Returns → Users, then grouped by Region and Product Category.

## Findings

Three regions land in a similar band — East ($85,291.40), Central ($77,365.47), West ($75,844.79) — all profitable across every category. South's raw total was **-$14,424.05**, the only region at a loss.

$16,476.84 of that comes from one transaction (positional index 975 in the analysis output; Row ID 18306 in the source file), South/Technology, whose Product Name field is corrupted to the literal value `"5165"`. Excluding just that transaction brings South to **+$2,052.78** — still last place, but not a loss.

**The corruption is systemic, not isolated.** The same `"5165"` value appears in 4 rows total, not just the one flagged above: South +$101.49, West +$2,169.75, Central +$1,656.66, and the South -$16,476.84 row. All four should be corrected or excluded before this dataset is used for reporting — the source system, not just this one row, needs to be flagged.

Separately, three high-ticket SKUs each appear twice among the 10 worst-profit transactions: Polycom ViewStation ($6,783.02/unit, both West, -$14,140.70 / -$13,562.64), Okidata Pacemark 4410N ($3,502.14/unit, both West, -$6,923.60 / -$4,075.93), and Epson DFX-8500 ($2,550.14/unit, one West -$5,390.74, one Central -$3,971.06). These are West-concentrated and are a separate pattern from South's number, not its cause. Discount (1-9%) and Product Base Margin (0.39-0.57, not thin) don't explain them — Spearman confirms Discount has essentially no relationship with Profit (ρ = -0.05), so the losses aren't a discounting problem.

**Two more large losses in that same top-10 list don't fit either pattern above** and are flagged, not explained: a Central/Furniture bookcase at -$13,706.46 (a bigger single loss than any Okidata or Epson transaction) and a Central/Furniture table at -$3,465.07. Worth a follow-up pass before this dataset drives any pricing decision.

Unit Price correlates strongly with Sales (ρ = 0.85) and only weakly with Profit (ρ = 0.18) — high-priced items sell for more but aren't reliably more profitable, which is consistent with the high-ticket losses above.

**Recommended:** correct or exclude all 4 corrupted-Product-Name rows before any regional profit reporting, and flag the source system; investigate actual per-unit cost on the loss-driving SKUs before any pricing action; treat the two unexplained Furniture losses as an open follow-up; treat South as a scoped underperformance review, not a crisis — profitable post-correction, just far behind its peers.

**Limitations:** no unit-cost field exists for profit calculations; Returns barely joins to Orders (11 of 1,634 matched); the two unexplained Furniture losses above are not yet investigated.

## How to Run
```
pip install pandas numpy matplotlib openpyxl
python Superstore_analysis.py
```
Requires `SuperStoreUS-2015.xlsx` in the same directory.

## What this demonstrates
- Manual cardinality checks (`.duplicated()`, `.nunique()`) on merge keys before joining 3 sources
- Multi-key groupby / named aggregation
- Spearman correlation + descriptive stats, cited with actual values above
- Isolating a systemic data-quality defect from a genuine business finding — and following the defect until it's fully accounted for, not just the first instance found
- Client-facing written insight under a strict word cap

## Files
- `Superstore_analysis.py` — full analysis script
- `Profit_Region&Category.png` — bar chart, total profit by region + category
- `Profit_UnitPrice.png` — scatter, unit price vs. profit (log-x, symlog-y)

**Tools:** Python, pandas, matplotlib
