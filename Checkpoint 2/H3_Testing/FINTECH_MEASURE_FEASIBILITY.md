# Feasibility Memo — A Direct Measure of Fintech Adoption

**Question:** Can we test the hypothesis that *direct* fintech adoption (not the
bank-branch-density proxy) is associated with nonprofit fundraising efficiency, among
nonprofits with revenue ≥ $500K — and is the effect stronger for smaller orgs
($500K–$1M) than larger (≥$1M)?

**Status: PAUSED after feasibility probing.** Two candidate data sources were probed;
findings and a recommended path are below. No production build was undertaken.

---

## Option A — IRS 990 payment-processing fees (Part IX, Line 24)

Payment-processing fees are **not** in NCCS CORE (CORE has the Line 24 *amounts*
`other_expenses_24a–f` but no description labels). They appear only as free-text in the
990 **e-file XML** (`<OtherExpensesGrp><Desc>+<TotalAmt>`). We probed this directly.

- **Probe:** `04_parse_efile_fees.py` — streamed a 600-return sample from the 2022 IRS
  e-file ZIP via HTTP range requests (`remotezip`; no 2.6 GB download) and regex-matched
  payment-processing descriptions.
- **Result:** of 145 sampled full-990 filers with revenue ≥ $500K, only **8 (≈5.5%)**
  reported an identifiable payment-processing fee line. Among those, `processing_fee_pct`
  median ≈ 1.6%, max ≈ 4.3%.
- **Verdict:** ❌ **Not viable as a primary measure.** Coverage is ~5.5% and the subset
  is **selection-biased** — orgs that itemize "credit card / Stripe fees" are
  disproportionately heavy electronic fundraisers, which would mechanically bias the
  result toward confirming the hypothesis.

**Other 990-derived databases (ProPublica, Candid/GuideStar, Cause IQ, ERI, NCCS) share
this ceiling** — they all derive from the same filings and cannot contain a figure the
filer never broke out.

### Silver lining
The same e-file XML carries `CYTotalFundraisingExpenseAmt` — the **true** Part IX total
fundraising expense — at **100% coverage**. This can replace the
`professional_fundraising_fees + events` **proxy** currently used as the DV denominator
in the branch-density H2, fixing that known limitation across the whole project.

---

## Option B — Website technographics (donation/payment platform detection)

Detect the actual donation/payment platform a nonprofit uses on its website (Stripe,
PayPal, Donorbox, Classy, Givebutter, Blackbaud, Bloomerang, Qgiv…). This is a *direct,
org-level* fintech-adoption signal and is **not** gated by whether the org itemized a fee.

- **Gate 1 — domains:** ~**94%** of full-990 returns carry `<WebsiteAddressTxt>` in the
  e-file XML → website is free and EIN-linkable (no fuzzy name matching).
- **Probe:** `05_probe_technographics.py` — for 60 ≥$500K filers, fetched the homepage
  (+ guessed `/donate`) and matched platform signatures / outbound links.
- **Result:**
  - **73%** have a usable website
  - **86%** of those reachable
  - **37% of reachable sites** had a detectable platform (Stripe, PayPal, Blackbaud,
    Bloomerang, Classy, Qgiv observed)
- **Verdict:** ✅ **Viable — ~7× the coverage of Option A** and a truer fintech measure.
  The 37% is a **floor**: the probe only scanned the homepage with a fixed signature
  list. A crawler that follows the actual "Donate" button and expands signatures would
  realistically reach 50–70%.

### Caveats to design around
1. **Temporal mismatch.** The website reflects *2026* tech; the 990 financials are
   *2018–2022*. Defensible as a cross-sectional adoption proxy, but **cannot** support a
   causal claim that 2022 efficiency was driven by tech observed in 2026.
2. **The IV changes shape** — from a continuous fee-share to **categorical adoption**
   (e.g. *modern fintech* [Stripe/Donorbox/Givebutter/FundraiseUp] vs *legacy*
   [Blackbaud/PayPal] vs *none*). Arguably a better operationalization of "fintech
   adoption" than fee %.
3. **Selection** — orgs with no website (~27%) or unreachable site (~14%) drop out
   (skews smaller/older), but far milder than Option A's itemization bias.

### Reframed hypothesis this would enable
> Among nonprofits with revenue ≥ $500K, those using a **modern fintech donation
> platform** have higher fundraising efficiency than those using legacy processors or
> none — with a stronger effect among smaller ($500K–$1M) organizations.

---

## Recommendation (for when we resume)

1. **Adopt the e-file `CYTotalFundraisingExpenseAmt`** to replace the DV proxy in the
   existing branch-density H2 — low effort, high payoff, full coverage.
2. **If pursuing the direct measure, use Option B (technographics), not Option A.** Build
   a production crawler (follow Donate links, expand signatures) writing
   `ein → platform → adoption_tier`, then merge into the modeling frame and re-run the
   models with the categorical fintech-adoption IV and the $500K–$1M vs ≥$1M split.
3. **Treat Option A (990 fees) only as a small, explicitly caveated exploratory check**,
   never as primary evidence.

## Artifacts
- `04_parse_efile_fees.py` + `data/efile_fee_probe_2022.csv` — Option A probe
- `05_probe_technographics.py` + `data/technographics_probe_2022.csv` — Option B probe
- (data files are git-ignored; re-run the scripts to regenerate)
