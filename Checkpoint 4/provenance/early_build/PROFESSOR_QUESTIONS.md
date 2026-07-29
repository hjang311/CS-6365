# Professor Unblock Questions (Checkpoint 4 / Phase 3)

Pre-drafted for office hours. Answers here are our **working defaults** until confirmed.

---

### (a) Is propose → pre-register → deterministic-execute “rolled enough”?

**Question:** Does Phase 3 require the agent to control execution (spawn OLS itself), or is it enough that the agent rewrites the agenda after seeing results while Python remains the sole statistics engine?

**Our default:** Rolled enough. The agent proposes indicators/hypotheses; every round is written to JSON before OLS; `09 --run` executes deterministically. The agent never computes coefficients. This matches “agent proposes, system verifies.”

---

### (b) Is interaction-term OLS what is meant by higher-order correlation?

**Question:** For “3+ variable / higher-order,” is `DV ~ IV1 + IV2 + IV1:IV2 + controls` the intended specification, or do you want something else (mediation, multilevel, etc.)?

**Our default:** Interaction-term OLS with the shared Phase 2 control set and HC1 errors. Documented in the proposals schema as `spec_type: "interaction"`.

---

### (c) ACFB ToS / contact guidance if the locator is restrictive

**Question:** If [acfb.org/get-help/food-map](https://www.acfb.org/get-help/food-map/) has no public JSON API or blocks bulk collection, should we (1) contact ACFB for a partner list, (2) stay with agent-driven manual ZIP lookups for a pilot, or (3) stop at workflow documentation?

**Our default:** Feasibility spike first; if restricted, agent-driven/manual pilot for Fulton/DeKalb ZIPs + document ToS posture. Full 29-county / 700+ partner build is best-effort. Workflow documentation is itself a deliverable.

---

### (d) Definition of done for the final report

**Question:** Is “workflow documentation + pilot ZIP density + one loop demo” sufficient if the full ACFB build does not finish, or must we complete all ~700 partners?

**Our default:** Pilot + documented coverage achieved is done. Full build is stretch; report states exact ZIP/agency counts.

---

### (e) Validation bar for agent-proposed indicators

**Question:** How do we score a proposal “success”? Exact β match (like H4/H5 calibration), or sign + significance vs a pre-stated expected direction?

**Our default:** For new proposals: **sign + significance vs expected_direction** (confirmed / rejected / not significant). Exact β calibration remains reserved for H4/H5 regression tests of the shared OLS recipe.

---

### (f) How much “Beyond Phase 3” belongs in the final report?

**Question:** Should the Checkpoint 4 report include a substantial next-generation roadmap, or a short forward-looking paragraph?

**Our default:** A short “Beyond Phase 3” section (see `PROJECT_PROGRESSION.md`)—enough for continuity, not a second project plan.
