"""
03_hitl_hypothesis_engine.py  —  Phase 3: HITL Hypothesis Engine

Reads CP3 modeling frame, uses the Antigravity Agent interactive prompt to brainstorm hypotheses,
pauses for human-in-the-loop (HITL) approval, and runs a deterministic log-log OLS regression.
No external API calls or API keys required.
"""
import json
import os
import sys
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
HERE = os.path.dirname(os.path.abspath(__file__))

# --- Helper function for robust OLS regression ---
def run_ols(df, iv, dv, label):
    """Deterministic, robust Python OLS with CP2 control covariates."""
    print(f"\n[OLS Execution] Running regression model: {dv} ~ {iv}")
    
    # Ensure variables exist in dataframe
    for var in [iv, dv, "log_total_revenue", "poverty_rate", "median_hh_income"]:
        if var not in df.columns:
            print(f"Error: Required column '{var}' is missing from the modeling frame.")
            return None
            
    # Subsetting and listwise dropping of NaNs
    analysis_cols = [iv, dv, "log_total_revenue", "poverty_rate", "median_hh_income", "ntee_major", "region"]
    df_clean = df[analysis_cols].replace([np.inf, -np.inf], np.nan).dropna().copy()
    
    if len(df_clean) < 100:
        print(f"Error: Too few data points ({len(df_clean):,}) after listwise deletion of NaNs.")
        return None
        
    formula = f"{dv} ~ {iv} + log_total_revenue + C(ntee_major) + C(region) + poverty_rate + median_hh_income"
    try:
        m = smf.ols(formula, data=df_clean).fit(cov_type="HC1")
        print(f"=== Regression Results: {label} (n={int(m.nobs):,}) ===")
        print(f"  IV coefficient ({iv}): beta={m.params.get(iv, 0):.5f}, "
              f"p={m.pvalues.get(iv, 1):.4g}, R2={m.rsquared:.4f}")
        return m
    except Exception as e:
        print(f"Regression OLS run failed: {e}")
        return None

def run_engine():
    frame_path = os.path.join(DATA, "cp3_modeling_frame.csv")
    
    if not os.path.exists(frame_path):
        print(f"Error: Modeling frame not found at {frame_path}. Run Phase 1 & 2 first.")
        return
        
    df = pd.read_csv(frame_path)
    
    print("\n=== [Engine] Step 1 & 2: Brainstorming Hypotheses & Prior Art Check ===")
    print("====================================================================")
    print("AGENT ACTION REQUIRED: Please act as the Sociological Hypothesis LLM.")
    print("System Instruction: You are an expert sociological researcher. Given a dataset's columns, generate 5 strong hypotheses that test relationships between these variables.")
    print("Your output MUST be a valid JSON array of objects, with each object having the following keys: 'id' (int 1-5), 'iv' (string), 'dv' (string), 'rationale' (string), 'novelty_score' (int 1-5), 'prior_art_summary' (string), 'key_citations' (list of strings).")
    print(f"Available Columns: {list(df.columns)}")
    print("---")
    print("Please paste the generated JSON below. Type 'END_OF_RESPONSE' on a new line when finished.")
    print("====================================================================")
    
    response_lines = []
    while True:
        try:
            line = input()
            if line.strip() == "END_OF_RESPONSE":
                break
            response_lines.append(line)
        except EOFError:
            break
            
    response_text = "\n".join(response_lines)
    
    try:
        hypotheses = json.loads(response_text)
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON. Error: {e}")
        print("Raw response:")
        print(response_text)
        return
        
    print("\n=== [Engine] Step 3: Human-In-The-Loop Interactive Loop ===")
    print("Here are the sociologically grounded hypotheses and their novelty scores:")
    for h in hypotheses:
        print(f"\n[{h['id']}] Hypothesis: {h['dv']} ~ {h['iv']}")
        print(f"    Rationale: {h['rationale']}")
        print(f"    Novelty Score: {h['novelty_score']}/5")
        print(f"    Prior Art: {h['prior_art_summary']}")
        print(f"    Citations: {', '.join(h['key_citations'])}")
            
    print("\n[0] Enter a custom manual hypothesis")
    
    choice = input("\nEnter the hypothesis ID you want to test (or 0 for custom): ")
    
    iv, dv = None, None
    if choice == "0":
        iv = input("Enter Independent Variable (IV) column name: ")
        dv = input("Enter Dependent Variable (DV) column name: ")
    else:
        try:
            selected = next(h for h in hypotheses if str(h["id"]) == choice.strip())
            iv, dv = selected["iv"], selected["dv"]
        except StopIteration:
            print("Invalid choice. Exiting.")
            return
        except ValueError:
            print("Invalid choice format. Exiting.")
            return

    # Deterministic OLS Run
    model = run_ols(df, iv, dv, f"CP3 Model: {dv} ~ {iv}")
    
    # Save output to Markdown Results
    if model:
        res_path = os.path.join(HERE, "H4", "H4_results.md")
        lines = [
            f"# Checkpoint 3 Hypothesis Testing Results\n",
            f"**Hypothesis Tested:** `{dv} ~ {iv}`\n",
            f"### Statistical Metrics",
            f"| Metric | Value |",
            f"|---|---|",
            f"| Independent Variable (IV) | `{iv}` |",
            f"| Dependent Variable (DV) | `{dv}` |",
            f"| Number of Observations (n) | {int(model.nobs):,} |",
            f"| R-squared ($R^2$) | {model.rsquared:.4f} |",
            f"| F-statistic | {model.fvalue:.4f} |",
            f"| IV coefficient (beta) | {model.params.get(iv, 0):.5f} |",
            f"| IV P-value | {model.pvalues.get(iv, 1):.4g} |",
            f"| 95% Confidence Interval | [{model.conf_int().loc[iv, 0]:.5f}, {model.conf_int().loc[iv, 1]:.5f}] |\n"
        ]
        
        # Add prior art summary if available
        if choice != "0":
            selected = next(h for h in hypotheses if str(h["id"]) == choice)
            lines += [
                "### Prior Art & Novelty Assessment",
                f"- **Novelty Score:** {selected['novelty_score']}/5",
                f"- **Prior Art Summary:** {selected['prior_art_summary']}",
                f"- **Key Citations:** {', '.join(selected['key_citations'])}"
            ]
            
        with open(res_path, "w") as f:
            f.write("\n".join(lines) + "\n")
            
        print(f"\n[Engine] Successfully saved results to: {res_path}")

def main():
    run_engine()

if __name__ == "__main__":
    main()
