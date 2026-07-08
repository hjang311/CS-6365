"""
07_deterministic_loop.py  —  Phase 7: Deterministic Agentic Loop

Runs hypothesis testing systematically across variable pairs in the CP3 modeling frame.
Features two execution modes:
  1. --interactive: Runs only H4 & H5 validation pairs with step-by-step agent prompts.
  2. --batch: Scans all combinatorial variable pairs, filtering and prompting the agent to 
              interpret only the statistically significant findings (p < 0.05).
"""
import os
import sys
import argparse
import json
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
OUTPUT_DIR = os.path.join(HERE, "loop_results")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "iteration_logs"), exist_ok=True)

CONTROLS = "log_total_revenue + C(ntee_major) + C(region) + poverty_rate + median_hh_income"

# Groups of related variables to skip redundant intra-group pairs
REDUNDANCY_GROUPS = {
    "total_revenue": ["total_revenue", "log_total_revenue"],
    "efficiency": ["fundraising_efficiency", "log_fundraising_efficiency", "fundraising_efficiency_w"],
    "density": ["nonprofit_branch_density", "log_nonprofit_branch_density"],
    "zhvi": ["zhvi_2022", "log_zhvi_2022"],
    "contributions": ["total_contributions"],
    "expenses": ["total_expenses"],
    "events": ["fundraising_events_direct_expenses"],
    "fees": ["professional_fundraising_fees"],
    "proxy": ["fundraising_expense_proxy"],
    "population": ["population"],
    "social_service_count": ["social_service_count"]
}

def get_redundancy_group(var):
    for group_name, vars_list in REDUNDANCY_GROUPS.items():
        if var in vars_list:
            return group_name
    return None

def run_ols(df, iv, dv):
    """Deterministic, robust Python OLS with controls."""
    cols = [iv, dv, "log_total_revenue", "poverty_rate", "median_hh_income", "ntee_major", "region"]
    
    # If IV is categorical (like size_segment), handle it
    is_categorical_iv = (iv == "size_segment" or df[iv].dtype == object)
    
    # Clean data
    df_clean = df[cols].replace([np.inf, -np.inf], np.nan).dropna().copy()
    if len(df_clean) < 100:
        return None
        
    formula_iv = f"C({iv})" if is_categorical_iv else iv
    formula = f"{dv} ~ {formula_iv} + {CONTROLS}"
    
    try:
        m = smf.ols(formula, data=df_clean).fit(cov_type="HC1")
        return m
    except Exception as e:
        print(f"  [OLS Error] failed to regress {dv} ~ {iv}: {e}")
        return None

def prompt_agent(prompt_text):
    """Prints prompt and waits for agent input ending with END_OF_RESPONSE."""
    print("\n" + "=" * 70)
    print(prompt_text)
    print("=" * 70)
    
    lines = []
    while True:
        try:
            line = input()
            if line.strip() == "END_OF_RESPONSE":
                break
            lines.append(line)
        except EOFError:
            break
            
    response = "\n".join(lines)
    try:
        return json.loads(response)
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON. Error: {e}")
        print("Raw response received:")
        print(response)
        # Return fallback mock JSON to allow execution to proceed if there's a JSON issue
        return {
            "error_fallback": True,
            "hypothesis_direction": "none",
            "hypothesis_rationale": "Fallback due to JSON parse error.",
            "prior_art_notes": "None",
            "extra_cleaning_rules": [],
            "hypothesis_confirmed": False,
            "strength": "weak",
            "interpretation": "Fallback due to JSON parse error."
        }

def run_interactive(df):
    """Interactive validation mode for H4 and H5 only."""
    print("\n=== Deterministic Agentic Loop: Interactive Validation Mode (H4 & H5) ===")
    
    validation_pairs = [
        ("log_zhvi_2022", "fundraising_efficiency_w", "H4"),
        ("log_nonprofit_branch_density", "fundraising_efficiency_w", "H5")
    ]
    
    results = []
    
    for iv, dv, label in validation_pairs:
        # Prompt 1: Phase 1 & 2 (Specialize & Hypothesize)
        p1 = f"""AGENT ACTION REQUIRED: Phase 1 & 2 (Specialize & Hypothesize)
Testing validation pair {label}: {dv} ~ {iv}

System Instruction: You are an expert sociological researcher. Suggest a hypothesis and specialization strategy for this pair.
Respond with a JSON object containing:
  "hypothesis_direction": "positive" | "negative" | "none",
  "hypothesis_rationale": "your detailed sociological rationale",
  "prior_art_notes": "citation of 1-2 papers or known literature from your training memory",
  "extra_cleaning_rules": [] (or array of conditions)

Type 'END_OF_RESPONSE' on a new line when finished."""
        
        agent_p1 = prompt_agent(p1)
        
        # Execute OLS
        m = run_ols(df, iv, dv)
        if m is None:
            print(f"Validation failed for {label}: OLS execution returned None.")
            continue
            
        beta = m.params.get(iv, m.params.get(f"C({iv})[T.large]", 0))
        pvalue = m.pvalues.get(iv, m.pvalues.get(f"C({iv})[T.large]", 1))
        
        # Prompt 2: Phase 3 (Interpret Results)
        p2 = f"""AGENT ACTION REQUIRED: Phase 3 (Interpret Results)
OLS Results for {label} ({dv} ~ {iv}):
  n = {int(m.nobs):,}
  beta = {beta:.5f}
  p-value = {pvalue:.4g}
  R-squared = {m.rsquared:.4f}
  95% CI = [{m.conf_int().loc[iv, 0]:.4f}, {m.conf_int().loc[iv, 1]:.4f}]

Your pre-analysis hypothesis direction was: "{agent_p1.get('hypothesis_direction', 'none')}"

TASK: Interpret these results.
Respond with a JSON object containing:
  "hypothesis_confirmed": true | false,
  "strength": "weak" | "moderate" | "strong",
  "interpretation": "what this means practically for the nonprofit sector"

Type 'END_OF_RESPONSE' on a new line when finished."""
        
        agent_p2 = prompt_agent(p2)
        
        # Save Iteration Log
        log_data = {
            "label": label,
            "iv": iv,
            "dv": dv,
            "hypothesis": agent_p1,
            "results": {
                "n": int(m.nobs),
                "beta": float(beta),
                "pvalue": float(pvalue),
                "rsquared": float(m.rsquared)
            },
            "interpretation": agent_p2
        }
        log_path = os.path.join(OUTPUT_DIR, "iteration_logs", f"{label}_interactive.json")
        with open(log_path, "w") as f:
            json.dump(log_data, f, indent=2)
            
        results.append(log_data)
        print(f"\n[{label}] Regression complete: beta={beta:.5f}, p={pvalue:.3g}")
        
    # Write validation report
    validation_check_path = os.path.join(OUTPUT_DIR, "validation_check.md")
    lines = [
        "# Interactive Loop Validation Report\n",
        "This report checks if the deterministic loop successfully reproduces the verified H4 & H5 results.\n",
        "## Validation Results\n",
        "| Metric | Expected H4 | Loop H4 | Status | Expected H5 | Loop H5 | Status |",
        "|---|---|---|---|---|---|---|",
    ]
    
    # Extract loop metrics
    h4_loop = next((r for r in results if r["label"] == "H4"), None)
    h5_loop = next((r for r in results if r["label"] == "H5"), None)
    
    h4_status = "PASS" if h4_loop and abs(h4_loop["results"]["beta"] - (-7.91647)) < 1e-4 else "FAIL"
    h5_status = "PASS" if h5_loop and abs(h5_loop["results"]["beta"] - 2.11963) < 1e-4 else "FAIL"
    
    h4_beta_loop = f"{h4_loop['results']['beta']:.5f}" if h4_loop else "N/A"
    h5_beta_loop = f"{h5_loop['results']['beta']:.5f}" if h5_loop else "N/A"
    
    lines.append(f"| IV | `log_zhvi_2022` | `log_zhvi_2022` | - | `log_nonprofit_branch_density` | `log_nonprofit_branch_density` | - |")
    lines.append(f"| beta | `-7.91647` | `{h4_beta_loop}` | **{h4_status}** | `2.11963` | `{h5_beta_loop}` | **{h5_status}** |")
    
    with open(validation_check_path, "w") as f:
        f.write("\n".join(lines) + "\n")
        
    print(f"\n[Validation] Validation report written to {validation_check_path}")
    print(f"  H4 Status: {h4_status}")
    print(f"  H5 Status: {h5_status}")

def run_batch(df):
    """Batch mode scanning all non-redundant pairs, prompting for significant findings."""
    print("\n=== Deterministic Agentic Loop: Batch Combinatorial Mode ===")
    
    exclude_cols = ["ein", "EIN", "ZIP5", "STATE", "NTEE_CD", "tax_year",
                    "log_total_revenue", "poverty_rate", "median_hh_income", "ntee_major", "region"]
    
    testables = [c for c in df.columns if c not in exclude_cols]
    
    # We want valid numeric DVs
    valid_dvs = [c for c in testables if c != "size_segment"]
    valid_ivs = testables
    
    pairs = []
    for iv in valid_ivs:
        for dv in valid_dvs:
            if iv == dv:
                continue
            # Redundancy group check
            iv_group = get_redundancy_group(iv)
            dv_group = get_redundancy_group(dv)
            if iv_group and dv_group and iv_group == dv_group:
                continue
            pairs.append((iv, dv))
            
    print(f"Total combinatorial pairs generated: {len(pairs)}")
    
    significant_findings = []
    all_results = []
    
    iter_count = 0
    for iv, dv in pairs:
        iter_count += 1
        m = run_ols(df, iv, dv)
        if m is None:
            continue
            
        beta = m.params.get(iv, m.params.get(f"C({iv})[T.large]", 0))
        pvalue = m.pvalues.get(iv, m.pvalues.get(f"C({iv})[T.large]", 1))
        
        res_row = {
            "id": iter_count,
            "iv": iv,
            "dv": dv,
            "n": int(m.nobs),
            "beta": float(beta),
            "pvalue": float(pvalue),
            "rsquared": float(m.rsquared),
            "significant": pvalue < 0.05
        }
        all_results.append(res_row)
        
        if pvalue < 0.05:
            # Stats are significant! Ask the agent for interpretation
            p_sig = f"""AGENT ACTION REQUIRED: Interpret Significant Finding
We found a statistically significant correlation ({iter_count}/{len(pairs)}):
  DV: {dv} ~ IV: {iv}
  n = {int(m.nobs):,}
  beta = {beta:.5f}
  p-value = {pvalue:.4g}
  R-squared = {m.rsquared:.4f}

System Instruction: You are an expert sociological researcher. Formulate a hypothesis rationale, cite prior art from memory, and interpret this finding.
Respond with a JSON object containing:
  "hypothesis_direction": "positive" | "negative" | "none",
  "hypothesis_rationale": "theoretical explanation of why these variables correlate",
  "prior_art_notes": "citation of 1-2 papers or known literature from your training memory",
  "strength": "weak" | "moderate" | "strong",
  "interpretation": "what this means practically for the nonprofit sector"

Type 'END_OF_RESPONSE' on a new line when finished."""
            
            agent_res = prompt_agent(p_sig)
            
            sig_finding = {
                "id": iter_count,
                "iv": iv,
                "dv": dv,
                "n": int(m.nobs),
                "beta": float(beta),
                "pvalue": float(pvalue),
                "rsquared": float(m.rsquared),
                "agent_analysis": agent_res
            }
            significant_findings.append(sig_finding)
            
            # Save individual iteration log
            log_path = os.path.join(OUTPUT_DIR, "iteration_logs", f"iter_{iter_count:03d}_{iv}_to_{dv}.json")
            with open(log_path, "w") as f:
                json.dump(sig_finding, f, indent=2)
                
            print(f"  [Significant] {dv} ~ {iv} (beta={beta:.5f}, p={pvalue:.3g}) interpreted by agent.")
        else:
            if iter_count % 20 == 0:
                print(f"Processed {iter_count}/{len(pairs)} pairs...")

    # Write loop_summary.md
    summary_path = os.path.join(OUTPUT_DIR, "loop_summary.md")
    summary_lines = [
        "# Deterministic Agentic Loop - Summary of Results\n",
        f"Tested a total of {len(pairs)} combinatorial variable pairs.\n",
        "| ID | IV | DV | beta | p-value | R² | n | Significant? |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for r in all_results:
        sig_str = "✅ Yes" if r["significant"] else "No"
        summary_lines.append(f"| {r['id']} | `{r['iv']}` | `{r['dv']}` | {r['beta']:.5f} | {r['pvalue']:.4g} | {r['rsquared']:.4f} | {r['n']:,} | {sig_str} |")
        
    with open(summary_path, "w") as f:
        f.write("\n".join(summary_lines) + "\n")
        
    # Write significant_findings.md
    sig_path = os.path.join(OUTPUT_DIR, "significant_findings.md")
    sig_lines = [
        "# Deterministic Agentic Loop - Significant Findings\n",
        f"Out of {len(pairs)} pairs tested, {len(significant_findings)} were statistically significant at p < 0.05.\n",
    ]
    
    for sf in significant_findings:
        aa = sf["agent_analysis"]
        sig_lines.extend([
            f"## Finding #{sf['id']}: `{sf['dv']} ~ {sf['iv']}`",
            "",
            f"- **IV Coefficient (beta):** `{sf['beta']:.5f}`",
            f"- **P-value:** `{sf['pvalue']:.4g}`",
            f"- **R-squared:** `{sf['rsquared']:.4f}`",
            f"- **Sample Size (n):** `{sf['n']:,}`",
            f"- **Hypothesized Direction:** `{aa.get('hypothesis_direction', 'none')}`",
            f"- **Relationship Strength:** `{aa.get('strength', 'weak')}`",
            "",
            "### Hypothesis Rationale",
            f"{aa.get('hypothesis_rationale', 'N/A')}",
            "",
            "### Prior Art & Citations (Agent Training Memory)",
            f"{aa.get('prior_art_notes', 'N/A')}",
            "",
            "### Practical Interpretation",
            f"{aa.get('interpretation', 'N/A')}",
            "\n---\n"
        ])
        
    with open(sig_path, "w") as f:
        f.write("\n".join(sig_lines) + "\n")
        
    print(f"\n[Batch Complete] Wrote summary to {summary_path}")
    print(f"[Batch Complete] Wrote significant findings to {sig_path}")

def main():
    parser = argparse.ArgumentParser(description="Deterministic Agentic Loop")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--interactive", action="store_true", help="Interactive validation mode (H4/H5)")
    group.add_argument("--batch", action="store_true", help="Batch mode scanning all pairs")
    args = parser.parse_args()
    
    frame_path = os.path.join(DATA, "cp3_modeling_frame.csv")
    if not os.path.exists(frame_path):
        print(f"Error: Modeling frame not found at {frame_path}. Run Phase 2 first.")
        sys.exit(1)
        
    df = pd.read_csv(frame_path)
    
    if args.interactive:
        run_interactive(df)
    elif args.batch:
        run_batch(df)

if __name__ == "__main__":
    main()
