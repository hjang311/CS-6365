import pandas as pd, numpy as np
from scipy.stats import chi2_contingency

CSV = "/Users/carladuplessis/Documents/CS-6365/dataverse_files/YEAR-04-DATA-PUF.csv"
OUT = "/Users/carladuplessis/Documents/CS-6365/dataverse_files/cleaned_test_case_1_weighted.csv"

# ---------- 1. SENSE ----------
df = pd.read_csv(CSV, low_memory=False)
cols = ["Benefits_Health", "BenefitsImpact", "year4wt"]
for c in cols:
    assert c in df.columns, f"MISSING COLUMN: {c}"
print("=== SENSE ===")
for c in cols:
    print(f"\n[{c}] dtype={df[c].dtype}  missing%={df[c].isna().mean()*100:.2f}")
    print("unique:", sorted(df[c].dropna().unique().tolist())[:30])

# ---------- 2. CLEANING CONTRACT (exact order) ----------
# a. subset
d = df[cols].copy()
# b. coerce numeric
for c in cols:
    d[c] = pd.to_numeric(d[c], errors="coerce")
# c. Likert mapping on BenefitsImpact; 97/98 -> missing
def likert(v):
    if v in (1, 2): return "Negative"
    if v == 3:      return "No Impact"
    if v in (4, 5): return "Positive"
    return np.nan  # includes 97, 98, NaN
d["impact"] = d["BenefitsImpact"].map(likert)
# d. listwise deletion: Benefits_Health null OR impact null
d = d[d["Benefits_Health"].notna() & d["impact"].notna()]
# e. weight filter
d = d[np.isfinite(d["year4wt"]) & (d["year4wt"] > 0)]
# f. final n
n = len(d)
print(f"\n=== CLEANING ===\nWeight column used: year4wt\nFinal n after listwise+weight filter: {n}")

# ---------- 3. WEIGHTED COMPUTATION ----------
order = ["Negative", "No Impact", "Positive"]
print("\n=== WEIGHTED CROSS-TAB (sum of year4wt) Benefits_Health x impact ===")
wct = d.pivot_table(index="Benefits_Health", columns="impact",
                    values="year4wt", aggfunc="sum", fill_value=0.0).reindex(columns=order)
print(wct.round(2))

def wpct(cat):
    denom = d.loc[d["impact"] == cat, "year4wt"].sum()
    num = d.loc[(d["impact"] == cat) & (d["Benefits_Health"] == 1), "year4wt"].sum()
    return num / denom * 100 if denom else float("nan")

def rpct(cat):
    sub = d[d["impact"] == cat]
    return (sub["Benefits_Health"] == 1).mean() * 100 if len(sub) else float("nan")

print("\n=== FIGURE 17 HEADLINE: % Benefits_Health==1 within impact category ===")
print(f"{'category':<10} {'WEIGHTED %':>12} {'UNWEIGHTED %':>14}")
for cat in order:
    print(f"{cat:<10} {wpct(cat):>12.2f} {rpct(cat):>14.2f}")
print(f"\nOFFICIAL (weighted) Positive={wpct('Positive'):.1f}%  Negative={wpct('Negative'):.1f}%")

# ---------- 4. SIGNIFICANCE (unweighted counts) ----------
ct = pd.crosstab(d["Benefits_Health"], d["impact"]).reindex(columns=order, fill_value=0)
chi2, p, dof, _ = chi2_contingency(ct)
N = ct.values.sum()
cramers_v = np.sqrt(chi2 / (N * (min(ct.shape) - 1)))
print("\n=== CHI-SQUARE (unweighted counts) ===")
print("contingency:\n", ct)
print(f"chi2={chi2:.4f}  dof={dof}  p={p:.3e}  CramersV={cramers_v:.4f}")

# ---------- 5. OUTPUT ----------
out = d[["Benefits_Health", "impact", "year4wt"]].rename(columns={"impact": "BenefitsImpact_label"})
out.to_csv(OUT, index=False)
print(f"\nWrote {len(out)} rows -> {OUT}")
