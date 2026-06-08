# Environment Setup Log — NORP_Spring26_G5 Reproduction

## Date: May 25, 2026

---

## 1. Prerequisites

### 1.1 System Information
- **OS:** macOS (Apple Silicon / ARM64)
- **Python Version:** 3.9.6 (system Python via `/Library/Developer/CommandLineTools`)
- **Virtual Environment:** Created at `NORP_Spring26_G5/venv/` using `python3 -m venv venv`

### 1.2 Required Accounts / API Keys
- [x] `SOCRATA_APP_TOKEN` — Chicago Data Portal app token
- [x] `OPENROUTER_API_KEY` — OpenRouter API key

---

## 2. Repository Clone

```bash
git clone https://github.gatech.edu/IEC-Summer-26/NORP_Spring26_G5.git
```

- **14:23 CDT** — Clone initiated. Required GT enterprise GitHub authentication (interactive username + password prompt).
- **14:27 CDT** — Clone completed successfully. 15 files, 1 commit, all Python.

> [!NOTE]
> GitHub Enterprise authentication required interactive terminal input (username + password). This cannot be done via automated CLI without a Personal Access Token (PAT).

---

## 3. Virtual Environment Setup

```bash
python3 -m venv venv
source venv/bin/activate
```

- **14:30 CDT** — Virtual environment created at `NORP_Spring26_G5/venv/` using system Python 3.9.6.

---

## 4. Dependencies Installation

```bash
pip install -r requirements.txt
```

- **14:30 CDT** — Installation started.
- **14:36 CDT** — Installation completed (~6 minutes).

### 4.1 Installation Details
- **Direct dependencies:** 18 packages listed in `requirements.txt`
- **Total installed packages:** 160+ (including transitive dependencies)
- **Notable large packages:** `torch`, `transformers`, `sentence-transformers`, `chromadb`
- **Version pinning:** None — `requirements.txt` has no version pins; all installed as latest

### 4.2 Warnings (Non-Critical)
- `pip` version 21.2.4 is outdated (upgrade available)
- `urllib3` `NotOpenSSLWarning`: system ships LibreSSL 2.8.3, but `urllib3` prefers OpenSSL 1.1.1+. Does not affect functionality.

---

## 5. Configuration

### 5.1 .env Setup

- **14:30 CDT** — Created `.env` file with the following variables:

| Variable | Purpose | Status |
|:---|:---|:---:|
| `SOCRATA_APP_TOKEN` | Chicago Data Portal app token | ✅ Configured |
| `OPENROUTER_API_KEY` | OpenRouter API key | ✅ Configured |

---

## 6. Issues Encountered

### 6.1 Python 3.10+ Syntax Incompatibility ⚠️

**File:** `cp2_extraction.py`, line 37
**Problem:** Uses `pd.DataFrame | None` union type hint syntax, which requires Python 3.10+. The system Python is 3.9.6.
**Fix:** Added `from __future__ import annotations` at the top of the file.

> [!IMPORTANT]
> This is a **new reproducibility finding** not documented in the original repository. The codebase implicitly requires Python 3.10+ due to PEP 604 union type syntax, but does not specify a minimum Python version anywhere.

### 6.2 urllib3 SSL Warning

**Severity:** Non-critical
**Details:** LibreSSL 2.8.3 (bundled with macOS) triggers a `NotOpenSSLWarning` from `urllib3`. No functional impact.

### 6.3 GitHub Enterprise Authentication

**Details:** Cloning from `github.gatech.edu` required interactive terminal authentication. Automated or scripted reproduction would require a pre-configured Personal Access Token.

---

## 7. Setup Summary

| Step | Status | Notes |
|:---|:---:|:---|
| Repository clone | ✅ | Required GT enterprise auth |
| Virtual environment | ✅ | Python 3.9.6 |
| Dependencies install | ✅ | 160+ packages, ~6 min |
| `.env` configuration | ✅ | Both API keys set |
| Python compatibility fix | ✅ | Added `from __future__ import annotations` to `cp2_extraction.py` |
| Ready for execution | ✅ | — |

---

## Timeline

| Time (CDT) | Event |
|:---|:---|
| 14:23 | Clone initiated |
| 14:27 | Clone completed |
| 14:30 | venv created, `.env` configured, `pip install` started |
| 14:36 | Dependencies installed — setup complete |
