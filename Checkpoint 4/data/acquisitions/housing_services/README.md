# Housing services acquisition — provenance note

Housing/Chicago universality demos use the **`ntee_density` adapter only**
(IRS BMF NTEE prefixes L20/L21/L22/L25/L40/L41). There is no Feed America–
style open HTTP bulk API for housing shelters in this repo.

Therefore this folder may be empty of HTTP raw JSONL/CSV. That is
**expected**, not a failed acquisition. Density and frame artifacts live at:

- `Checkpoint 4/data/housing_services_density_by_zip.csv`
- `Checkpoint 4/data/cp4_chicago_housing_services_xsection.csv`
- `Checkpoint 4/phase3_results/housing_chicago/`

Food assistance is the HTTP-provenance exemplar
(`../food_assistance/` + Feed America CC BY 4.0 attribution).
