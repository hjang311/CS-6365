"""
04_parse_efile_fees.py  —  FEASIBILITY PROBE for the direct fintech measure

Hypothesis (H3): Among nonprofits with revenue >= $500K, a higher share of expenses
on payment-processing fees (direct fintech measure) is associated with greater
fundraising efficiency, stronger among smaller ($500K-$1M) than larger (>=$1M) orgs.

Payment-processing fees are NOT in NCCS CORE — they appear only as free-text in IRS
990 e-file XML, Part IX Line 24 "Other Expenses" (<OtherExpensesGrp><Desc>+<TotalAmt>).
This probe streams a SAMPLE of returns from one IRS monthly ZIP via HTTP range requests
(remotezip — no full 2.6 GB download) and measures:
  - how many >=$500K full-990 filers report an identifiable payment-processing line
    (the COVERAGE that decides whether H3 is testable), and
  - the distribution of processing_fee_pct.

Usage:  python 04_parse_efile_fees.py --sample 600
"""
import argparse, random, re
import pandas as pd
from remotezip import RemoteZip

ZIP_URL = "https://apps.irs.gov/pub/epostcard/990/xml/2022/2022_TEOS_XML_01A.zip"

# free-text descriptions that denote payment / card / fintech transaction fees
FEE_RE = re.compile(
    r"(credit\s*card|merchant|payment\s*process|processing\s*fee|transaction\s*fee|"
    r"stripe|paypal|\bsquare\b|online\s*(giving|donation)|donation\s*process|"
    r"card\s*process|cc\s*fee|e-?commerce|ach\s*fee|bank\s*card)", re.I)

def first(pat, text, cast=float, default=None):
    m = re.search(pat, text)
    return cast(m.group(1)) if m else default

def parse_return(xml):
    """Return a dict of the fields we need, or None if not a usable full-990."""
    if "<ReturnTypeCd>990</ReturnTypeCd>" not in xml:
        return None
    ein   = first(r"<EIN>(\d+)</EIN>", xml, str)
    rev   = first(r"<CYTotalRevenueAmt>(-?\d+)</CYTotalRevenueAmt>", xml)
    exp   = first(r"<CYTotalExpensesAmt>(-?\d+)</CYTotalExpensesAmt>", xml)
    cont  = first(r"<CYContributionsGrantsAmt>(-?\d+)</CYContributionsGrantsAmt>", xml)
    fund  = first(r"<CYTotalFundraisingExpenseAmt>(-?\d+)</CYTotalFundraisingExpenseAmt>", xml)
    if not ein or not rev or not exp:
        return None
    # Part IX Line 24 other-expense groups: Desc + TotalAmt
    fee = 0.0
    for grp in re.findall(r"<OtherExpensesGrp>(.*?)</OtherExpensesGrp>", xml, re.S):
        desc = re.search(r"<Desc>([^<]*)</Desc>", grp)
        amt  = re.search(r"<TotalAmt>(-?\d+)</TotalAmt>", grp)
        if desc and amt and FEE_RE.search(desc.group(1)):
            fee += float(amt.group(1))
    return dict(ein=ein, total_revenue=rev, total_expenses=exp,
                total_contributions=cont, fundraising_expense_true=fund,
                payment_processing_fee=fee,
                processing_fee_pct=(fee / exp if exp else None))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", type=int, default=600)
    args = ap.parse_args()

    rows = []
    with RemoteZip(ZIP_URL) as z:
        names = z.namelist()
        random.seed(42)
        picks = random.sample(names, min(args.sample, len(names)))
        print(f"Sampling {len(picks):,} of {len(names):,} returns from 01A zip...")
        for i, n in enumerate(picks, 1):
            try:
                r = parse_return(z.read(n).decode("utf-8", "ignore"))
                if r:
                    rows.append(r)
            except Exception:
                pass
            if i % 100 == 0:
                print(f"  parsed {i:,} / {len(picks):,}  (usable full-990s: {len(rows):,})")

    df = pd.DataFrame(rows)
    df.to_csv("data/efile_fee_probe_2022.csv", index=False)

    big = df[df["total_revenue"] >= 500_000]
    with_fee = big[big["payment_processing_fee"] > 0]
    print("\n========== PROBE RESULTS ==========")
    print(f"Usable full-990 returns parsed:         {len(df):,}")
    print(f"  ... with revenue >= $500K:            {len(big):,}")
    print(f"  ... of those, with an identifiable")
    print(f"      payment-processing fee line:      {len(with_fee):,} "
          f"({(len(with_fee)/len(big)*100 if len(big) else 0):.1f}% COVERAGE)")
    if len(with_fee):
        s = with_fee["processing_fee_pct"]
        print(f"  processing_fee_pct among those: "
              f"median={s.median():.4f}  mean={s.mean():.4f}  max={s.max():.4f}")
    tf = big["fundraising_expense_true"].notna().mean() * 100
    print(f"True fundraising-expense field present:  {tf:.1f}% of >=$500K returns "
          f"(fixes the DV proxy)")
    print("Saved -> data/efile_fee_probe_2022.csv")

if __name__ == "__main__":
    main()
