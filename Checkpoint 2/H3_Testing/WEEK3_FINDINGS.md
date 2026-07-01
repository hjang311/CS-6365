# H3 Testing — Direct Fintech-Adoption Measure (Week 3 Findings)

## Objective
After establishing the bank-branch-density proxy for H2, we investigated whether a
**direct** measure of nonprofit fintech adoption could be obtained, in order to test a
stronger hypothesis: that among nonprofits with revenue ≥ $500,000, greater fintech
adoption is associated with higher fundraising efficiency, with a larger effect among
smaller organizations ($500K–$1M) than larger ones (≥$1M). We probed two candidate data
sources before committing engineering effort.

## Quantitative findings

**Option A — IRS 990 payment-processing fees (Part IX, Line 24).** Payment-processing
fees are absent from the structured NCCS CORE data and exist only as free-text line items
in the raw 990 e-file XML. Using a streaming parser (`remotezip`, which extracts
individual returns from the 2.6 GB IRS archive via HTTP range requests rather than
downloading it whole), we extracted a random sample of 600 individual returns. After
restricting to full Form 990 filers (270 returns) and then to our study population of
nonprofits with revenue ≥ $500,000 (145 returns), we found that only **8 organizations
(≈5.5%)** itemized an identifiable payment-processing fee (`processing_fee_pct`
median ≈ 1.6%, max ≈ 4.3%). This coverage is far too low for a primary analysis, and —
because all 990-derived databases (ProPublica, Candid, Cause IQ, NCCS) inherit the same
filings — no alternative database can exceed this ceiling.

**Option B — website technographics.** We tested detecting the donation/payment platform
a nonprofit uses on its website. The 990 e-file XML supplies each organization's website
for **~94%** of filers (free and EIN-linkable); on a 60-organization sample, **73% had a
usable website, 86% of those were reachable, and 37% of reachable sites exposed a
detectable platform.** This is roughly seven times the coverage of Option A and is a
floor, not a ceiling — the probe only scanned homepages with a fixed signature list.

**Incidental high-value finding.** The 990 e-file XML carries
`CYTotalFundraisingExpenseAmt` — the *true* Part IX total fundraising expense — at **100%
coverage**, which can replace the imperfect proxy denominator
(`professional fundraising fees + event expenses`) used in the branch-density model.

## Qualitative analysis
The platforms detected in the wild — **Stripe, PayPal, Blackbaud, Bloomerang, Classy,
and Qgiv** — are themselves informative. They fall into a meaningful spectrum: *modern,
self-serve fintech* (Stripe, and by extension Donorbox/Givebutter/FundraiseUp) versus
*legacy / enterprise donor-management systems* (Blackbaud, Bloomerang) versus *no
detectable digital giving infrastructure*. This suggests the most defensible
operationalization of "fintech adoption" is not a continuous fee-share but a
**categorical adoption tier** (modern fintech / legacy / none), which is truer to the
construct than a fee percentage. Organizations with no reachable website or no detected
platform skewed toward smaller, local, or volunteer-run entities (e.g., rural fire
departments, small co-ops) — consistent with the hypothesis that lower-infrastructure
nonprofits are exactly where fintech adoption should matter most, though it also signals a
selection effect to control for. Notably, Option A suffers a more severe bias:
organizations that explicitly itemize "credit card fees" are disproportionately
sophisticated electronic fundraisers, so a fee-based test would tend to *manufacture*
support for the hypothesis.

## Planned next steps
1. **Strengthen H2 immediately (low effort, high value):** swap the proxy denominator for
   the true `CYTotalFundraisingExpenseAmt` from the e-file XML and re-run the
   branch-density models.
2. **If pursuing the direct measure, build the technographics route, not the fee route:**
   develop a production crawler that follows each site's "Donate" link and expands the
   platform-signature set (targeting 50–70% detection), producing an
   `EIN → platform → adoption_tier` table to merge into the modeling frame.
3. **Re-test the reframed hypothesis** with the categorical fintech-adoption IV and the
   $500K–$1M vs ≥$1M size split, controlling for region, NTEE category, poverty rate, and
   median income.
4. **Address the temporal caveat explicitly:** website technology reflects 2026 while
   financials are 2018–2022, so frame any result as a cross-sectional association, not a
   causal effect, and note the website/reachability selection bias.
5. **Retain Option A only as a small, clearly caveated exploratory check**, never as
   primary evidence.

## Artifacts
- `04_parse_efile_fees.py` — Option A probe (990 e-file payment-fee parser)
- `05_probe_technographics.py` — Option B probe (website platform detector)
- `FINTECH_MEASURE_FEASIBILITY.md` — full feasibility memo
- `data/efile_fee_probe_2022.csv`, `data/technographics_probe_2022.csv` — probe outputs
  (git-ignored; re-run the scripts to regenerate)
