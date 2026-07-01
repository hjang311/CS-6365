"""
05_probe_technographics.py  —  FEASIBILITY PROBE for a website-based fintech measure

Tests whether we can build a DIRECT, org-level fintech-adoption IV by detecting the
donation/payment platform a nonprofit uses on its website.

Gate 1 (already confirmed): ~94% of full-990 returns carry <WebsiteAddressTxt> in the
e-file XML, linkable by EIN for free.
Gate 2 (this probe): given those domains, can we DETECT a payment/donation platform by
fetching the homepage (and a /donate guess) and matching known platform signatures /
outbound links — without any paid technographics API?

Reports: website coverage, reachable %, and platform-detection % among reachable sites.

Usage:  python 05_probe_technographics.py --sample 80
"""
import argparse, random, re
import requests
import pandas as pd
from remotezip import RemoteZip

ZIP_URL = "https://apps.irs.gov/pub/epostcard/990/xml/2022/2022_TEOS_XML_01A.zip"
UA = {"User-Agent": "Mozilla/5.0 (research; nonprofit-fintech-study)"}

# platform signatures: embedded scripts OR outbound links to platform domains
PLATFORMS = {
    "Stripe": r"js\.stripe\.com|stripe\.com/v\d",
    "PayPal": r"paypal\.com/donate|paypalobjects\.com|paypal\.com/sdk",
    "Donorbox": r"donorbox\.org",
    "Classy": r"classy\.org",
    "Givebutter": r"givebutter\.com",
    "Qgiv": r"qgiv\.com",
    "FundraiseUp": r"fundraiseup\.com",
    "NetworkForGood": r"networkforgood\.com",
    "Bloomerang": r"bloomerang\.co",
    "Blackbaud": r"blackbaud|bbox|donordrive|app\.etapestry",
    "GiveLively": r"givelively\.org",
    "Anedot": r"anedot\.com",
    "DoubleTheDonation": r"doublethedonation\.com",
    "Kindful": r"kindful\.com",
}
ANY_RE = {k: re.compile(v, re.I) for k, v in PLATFORMS.items()}


def clean_url(w):
    if not w or w.strip().upper() in ("N/A", "NA", "NONE", ""):
        return None
    w = w.strip().lower()
    w = re.sub(r"^https?://", "", w)
    return "https://" + w.split("/")[0]


def detect(url):
    """Fetch homepage (+ /donate) and return list of detected platforms."""
    found = set()
    for suffix in ("", "/donate", "/donate/", "/give"):
        try:
            r = requests.get(url + suffix, headers=UA, timeout=8, allow_redirects=True)
            html = r.text
        except Exception:
            continue
        for name, rx in ANY_RE.items():
            if rx.search(html):
                found.add(name)
        if found and suffix == "":
            break  # homepage already showed something; don't hammer donate pages
    return sorted(found)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", type=int, default=80)
    args = ap.parse_args()

    rows = []
    random.seed(7)
    with RemoteZip(ZIP_URL) as z:
        names = z.namelist()
        picks = random.sample(names, min(args.sample * 5, len(names)))
        for n in picks:
            if len(rows) >= args.sample:
                break
            x = z.read(n).decode("utf-8", "ignore")
            if "<ReturnTypeCd>990</ReturnTypeCd>" not in x:
                continue
            rev = re.search(r"<CYTotalRevenueAmt>(-?\d+)</CYTotalRevenueAmt>", x)
            if not rev or float(rev.group(1)) < 500_000:
                continue
            ein = re.search(r"<EIN>(\d+)</EIN>", x)
            web = re.search(r"<WebsiteAddressTxt>([^<]*)</WebsiteAddressTxt>", x)
            url = clean_url(web.group(1)) if web else None
            rows.append(dict(ein=ein.group(1) if ein else None,
                             revenue=float(rev.group(1)),
                             website_raw=web.group(1) if web else None,
                             url=url))

    df = pd.DataFrame(rows)
    have_url = df[df["url"].notna()].copy()
    print(f"Sampled {len(df)} full-990 >=$500K returns; "
          f"{len(have_url)} have a usable website "
          f"({len(have_url)/len(df)*100:.0f}%)")

    reachable = detected = 0
    results = []
    for _, r in have_url.iterrows():
        plats = detect(r["url"])
        ok = plats is not None
        # distinguish unreachable (exception on all) from reachable-but-none:
        try:
            requests.get(r["url"], headers=UA, timeout=8)
            reach = True
        except Exception:
            reach = False
        reachable += reach
        if plats:
            detected += 1
        results.append({**r, "platforms": ",".join(plats), "reachable": reach})
        print(f"  {r['url'][:45]:45s} reach={reach}  -> {plats}")

    pd.DataFrame(results).to_csv("data/technographics_probe_2022.csv", index=False)
    print("\n========== TECHNOGRAPHICS PROBE RESULTS ==========")
    print(f"Usable websites:                 {len(have_url)}")
    print(f"Reachable sites:                 {reachable} "
          f"({reachable/len(have_url)*100:.0f}% of websites)")
    print(f"Platform detected on site:       {detected} "
          f"({detected/max(reachable,1)*100:.0f}% of reachable)")
    print("Saved -> data/technographics_probe_2022.csv")


if __name__ == "__main__":
    main()
