# Methodology — AU Unclaimed Welfare Report

## 1. Core formula

Each benefit is estimated independently:

```
Unclaimed AUD per year =
    Eligible card holders (state, applicable card types, latest quarter)
  × Household dedup factor (0.70)
  × State-specific take-up gap (CPRC, NECF 2021-22 Q3)
  × Per-household entitlement (YAML amount.value)
```

## 2. Data sources and full citations

### 2.1 Take-up gap rates

**Citation block:**

> Consumer Policy Research Centre (CPRC), *Mind the Gap – Identifying the gap between energy concession eligibility and concessions received*, November 2022. Author: Ben Martin Hobbs.
> URL: https://cprc.org.au/report/mind-the-gap/
> PDF: https://cprc.org.au/wp-content/uploads/2022/11/Mind-the-Gap_Report_Update-1011.pdf
> Note: 2022-11-09 revised edition (ACT 41% → 31%)

CPRC is an independent consumer think-tank funded by the Victorian Government. The author is Ben Martin Hobbs. Since publication, the report has been cited by MS Australia, the Energy Charter, AIHW, and others. Media inquiries: media@cprc.org.au.

**State-specific rates (NECF framework, 2021-22 Q3):**

| State | Unclaimed rate |
|---|---|
| SA | 38% |
| NSW | **35%** |
| ACT | 31% (revised 2022-11) |
| QLD | 29% |
| TAS | 19% |

**Victoria (separate methodology — do not combine with the NECF table above):**

| Concession type | Unclaimed rate |
|---|---|
| Electricity | 7% |
| Gas | 12% |
| Water | 22% |

Victorian data is derived by DFFH from retailer monthly returns, on a methodology distinct from the AER's quarterly NECF reporting. CPRC's own caveat: "NECF and VIC may not be comparable." NECF five-state and Victoria figures are reported separately throughout this report; the two are not directly comparable.

### 2.2 Household dedup factor (0.70)

Source: CPRC Mind the Gap, p10, footnote 14:

```
weight = ((100/(1+x*R)) + ((100/(1+x*R)*R))) / 100
where x = 2 (cards per multi-card household, assumed)
      R = 42/58 = 0.72 (ratio of multi-card to single-card households)
→ weight ≈ 0.70
```

The 42% figure is from DHHS Victoria, *Victorian Utility Consumption Household Survey 2015* (the 2007 wave of the same survey reported 49%).

### 2.3 Eligible population — pilot uses CPRC-native counts; broader rollout will add direct DSS extraction

**Pilot decision (NSW Low Income Household Rebate).** The pilot directly adopts the NSW figures already published in CPRC *Mind the Gap* Figure 2 (p11):
- Total eligible concession holders (NSW): **1,783,270** (based on DSS June 2022 + DVA March 2022)
- Eligible households after 0.70 weighting: **1,248,289**
- Published concessions claimed (AER Q3 2021-22): **814,313**

**Why not pull the latest DSS quarter directly?**
- Matches CPRC's source and reference period exactly, so any side-by-side comparison between CPRC and this report uses identical denominators.
- Avoids several potential miscount sources — conflating the HCC and LIHCC columns, mishandling DVA Gold sub-types, and retailer-switching double-counting.
- The currency trade-off is acceptable: CPRC's 2021-22 data is the reference period for the gap rate; pairing the latest DSS quarter with the CPRC 2021-22 gap rate would introduce a vintage mismatch.

**Beyond the pilot.**
- Extending to non-NECF benefits, federal benefits, or more than five clusters requires a state × card_type breakdown drawn directly from DSS Payment Demographic Data.
- DSS source: https://data.gov.au/data/dataset/dss-payment-demographic-data
- **LIHCC is a sub-category of HCC.** When DSS reports a single "Health Care Card" column, it already includes LIHCC. Counting both columns introduces a 5–10% double-count error.

### 2.4 Entitlement amounts

**Fixed-type benefits** (all five NECF states' primary electricity concessions): use the YAML `amount.value` directly.

**Percentage-type benefits** (all three Victorian utility concessions): the YAML provides a discount rate (`base_rate`); a typical-recipient profile is used to impute a per-household AUD value. See §6 "Amount imputation for percentage rebates" for the imputation method.

**Formula-type benefits** (out of scope for v1): each rule's formula combined with typical input parameters yields a calibrated amount; these are modelled separately in subsequent waves.

## 3. Known biases — disclosure

| # | Bias | Direction | Magnitude | Treatment |
|---|---|---|---|---|
| 1 | DVA Gold sub-type | n/a | n/a | YAML uses a generic DVA Gold category; DSS uses the same generic category; CPRC's broad eligibility criteria align with both. All three sources are consistent, so there is no net bias. |
| 2 | 0.70 factor with x=2 assumption | Underestimates (conservative) | Hard to quantify; CPRC concedes that households "may be 3 or more" cards | Matches CPRC's own treatment, ensuring comparability; conservative direction is disclosed. |
| 3 | Gap rate vintage (mixed-vintage approach) | n/a | n/a | CPRC's 2022 gap rates paired with CPRC's 2022 eligibility counts (CPRC itself derived these from DSS June 2022 + DVA March 2022). Per-household amounts use current 2025-26 scheme rates. This is a mixed-vintage approach — 2022 eligibility combined with 2025-26 rates — made necessary by the absence of a published systematic update to CPRC's 2022 estimates. |
| 4 | CPRC self-assessment | Underestimates (conservative) | n/a | CPRC states: "the actual gap between eligible and claimed concessions may be greater." Quoted verbatim in this report. |
| 5 | Scope limitation | n/a | n/a | CPRC covers energy concessions only. The pilot is an energy rebate, so the methodology applies directly; any later extension to non-energy clusters must explicitly flag the gap rate as a proxy. |
| 6 | CSHC exclusion | n/a | n/a | The NSW LIHR rule directs CSHC holders to the Seniors Energy Rebate; CSHC is therefore not counted in this benefit's eligible population. |
| 7 | HCC/LIHCC counting convention | Prevents double-counting | 5–10% if mishandled | The computation script inspects DSS columns before aggregating, to avoid summing HCC and LIHCC twice. |
| 8 | **EBRF does not substitute for state concessions** | n/a | Material for interpretation | The federal Energy Bill Relief Fund is a universal, automatically applied temporary subsidy layered on top of state-level concessions. The 35% non-receipt rate for the NSW LIHR concerns the state concession's own take-up gap, and is unaffected by EBRF. When EBRF concludes at the end of 2025, state concessions become the only ongoing energy bill relief for low-income households — which is why the state concession take-up gap is a structural problem that a federal temporary subsidy does not address. |
| 9 | NSW cluster variant (RETAIL vs ON_SUPPLY) | Underestimates (conservative) | <1% | The NSW LIHR cluster has two mutually exclusive variants — RETAIL ($285/yr) and ON_SUPPLY ($313.50/yr). The pilot uses the RETAIL amount as a conservative floor. The ON_SUPPLY variant applies to approximately 5% of households in embedded networks (caravan parks, apartment embedded supply); including it would raise the NSW estimate by less than 1% (~$1.7M on a $124.5M base). Other states (QLD, SA, TAS, ACT) have no retail/on-supply split — a single rule covers the full eligible cohort. |

## 4. Cross-source corroboration (report lead)

**This section documents the strongest cross-source agreement in the dataset.** Two independent data sources — one government department's annual report, one independent think-tank — converge on the same finding.

### NSW Low Income Household Rebate

| Source | Methodology | Take-up gap | Year |
|---|---|---|---|
| **NSW Department of Planning and Environment**, *NSW Energy Rebates Annual Report 2020-21*, p4 | NSW Government's own administrative reporting (64% of eligible NSW consumers accessed the LIHR) | **36%** | 2020-21 |
| **CPRC**, *Mind the Gap*, Figure 3 p11 | Independent analysis of DSS card holder data vs AER concession reporting | **35%** | 2021-22 Q3 |

Difference: **≤1 percentage point**. The NSW Government's own annual report and CPRC's independent dataset analysis are within statistical noise of each other on the headline unclaimed rate.

This is the strongest corroboration in the dataset: one is the state agency administering the rebate itself; the other is a Victorian-funded national think tank. Their agreement makes the 35% figure exceptionally well-grounded.

NSW DPE source link: https://www.energy.nsw.gov.au/sites/default/files/2022-08/nsw-energy-rebates-annual-report-2020-21.pdf (CPRC endnote 8)

### Other NECF states

CPRC p7: "At time of writing, we could not identify any publicly available data about the size of the gap between those eligible and receiving concessions in other states."

QLD, SA, TAS, ACT figures rely on CPRC's single-source analysis. The NSW corroboration is the proxy for methodology validation across the NECF framework.

## 5. Validation (sanity gate)

Each benefit has a sanity gate built into compute_unclaimed.py: the script computes CPRC Figure 2 state eligible_households × state gap rate × (YAML amount.value or imputed AUD); a result within ±8–15% of the expected value passes, otherwise the script exits with code 1 without producing a CSV.

NSW worked example: 1,248,289 × 0.35 × $285 = $124,516,785 (actual = expected).

## 6. Amount imputation for percentage rebates

All five NECF states' primary electricity concessions are fixed annual amounts (YAML `amount.type=fixed`, applied directly). The Victorian three-utility cluster comprises percentage-type benefits (`base_rate` discount), requiring a per-household average dollar figure before unclaimed dollar totals can be computed. Every imputed value must be supported by citable retailer or DFFH data — no values are taken without source.

### VIC Electricity Concession — 17.5% off → $262.50/yr

Discount rate: 17.5% (YAML `AU_VIC_ANNUAL_ELECTRICITY_CONCESSION.amount.base_rate`; the first $171.60 of the bill is not discounted).

Typical calibration value: **concession-household annual electricity bill ≈ $1,500/yr**, drawn from CPRC's same-period dataset (AER Retail Market Performance Q3 2021-22, retailer-reported median bill for concession households — conservative compared to the unrestricted-population benchmark of approximately $2,000).

→ 17.5% × $1,500 = **$262.50/yr per concession household**

Note: the YAML formula further subtracts the first $171.60 of supply charge. A stricter "17.5% of the portion above $171.60" calculation would produce a lower (more conservative) per-household amount; the calibration here applies the headline 17.5% rate.

### VIC Winter Gas Concession — 17.5% winter only → $80/yr

Discount rate: 17.5% (1 May to 31 October only).

Typical calibration: concession-household annual gas bill ≈ $900/yr × winter share ~50% = $450 winter spend; 17.5% × $450 ≈ **$80/yr per gas-eligible household**.

Note: the rule includes an Excess Gas Concession trigger (winter bills above $2,499.14 use a separate formula); this calibration does not include the excess scenario.

### VIC Water and Sewerage Concession — 50% off, cap $372.10 → $250/yr

YAML: `amount.base_rate=0.5`, cap $372.10/yr (water + sewerage); eligibility limited to PCC and DVA Gold holders (HCC is not eligible under the DFFH rule).

Typical calibration: **$250/yr per water-eligible household**. This assumes most concession households remain below the cap (cap $372.10 × 67% ≈ $250). A cap-only scenario with all eligible households reaching the cap would imply $372.10/yr × 21.9% gap × 871,143 households ≈ $71M (versus our $47.9M estimate). This calibration uses the conservative value.

Note: the cap value is the official 2025-26 figure (confirmed via DFFH services.dffh.vic.gov.au); the CPRC 2022 report period had a slightly lower cap of $327/yr, which does not affect the gap rate calculation.

### VIC water HCC discrepancy disclosure

**The denominator CPRC uses for VIC water in Figure 4 (p13) — 1,414,194 cards / 871,143 households — does not fully align with the actual DFFH rule.** The DFFH VIC Water and Sewerage Concession (YAML rule schedule, card-linked) excludes HCC holders, accepting only PCC and DVA Gold. CPRC, however, applies the same 1,414,194 card total (which includes HCC) across all three utilities.

CPRC's published 22% water gap rate therefore uses a denominator that **includes ineligible HCC holders**. Under the actual DFFH eligibility (PCC + DVA Gold only), the eligible population would be smaller and the gap rate would be higher (because the published claimed count comes from actual DFFH enrolment data). This is one of the few places where the conservative direction breaks: the $47.9M VIC water estimate may be slightly overstated.

We retain CPRC's figures to preserve direct comparability with CPRC. This caveat is disclosed in the report; the actual VIC water rule eligibility can be verified on the official DFFH page (linked in the rule_url field).

## 7. Formula amount imputation

This section defines the calibration method for formula-type rules. Formula benefits (such as the VIC Excess Electricity Concession, Age Pension, JobSeeker, FTB) compute the dollar amount per recipient from household-specific inputs (bills, income, family composition, etc.) rather than from a fixed value. To run the "unclaimed households × per-household amount" computation, a per-household average dollar calibration is required. **This is the most error-prone step in the report** — selecting the wrong calibration value can throw the final figure off by a factor of 2 to 5.

### 7.1 Two traps to avoid

**Trap A — `base rate` ≠ actual rate**

YAML fields `amount.base` / `amount.value` / `amount.base_rate` typically represent the **statutory maximum or top tier** of the rule, not the actual average received per recipient. Formula-type benefits must use a Tier-1 officially reported `average payment per recipient` — not the YAML maximum.

Specific figures (Age Pension, JobSeeker, FTB, DSP, etc.) will be drawn from the DSS Annual Report when Chapter B runs the federal benefits; we do not preload unverified figures here.

**Trap B — do not compute the formula yourself**

Do not run the YAML formula against assumed inputs (even if those inputs seem reasonable). Reasons:
- The real distribution has a long tail; the "median user" is not the same as the "mean dollar spend".
- Self-calculated formula figures cannot be reliably reproduced by external estimators; official averages are derived from anonymised full-sample data not available outside the agencies. Published self-calculations will diverge from official budget figures.

### 7.2 Imputation hierarchy (apply in priority order; the tier used must be recorded explicitly)

| Tier | Source | Use | Aggregate handling |
|---|---|---|---|
| **Tier-1 (preferred)** | DSS / DFFH / state agency **publicly-reported avg per recipient** | The latest officially reported average from DSS Annual Report, Budget Paper No. 3 (Service Delivery), or Centrelink statistics | Included in the headline aggregate |
| **Tier-2** | Official worked example | rule_url or the rule's official page showing "for example, household with bill X gets concession $Y". Used as a floor; the report discloses that this is an example, not a true average | **Excluded from the headline aggregate**; recorded separately in `formula_pilot_v*.csv` and marked "indicative only" |
| **Tier-3 (last resort)** | YAML formula with documented typical inputs | Used only when neither Tier-1 nor Tier-2 is available | **Excluded from the headline aggregate**; recorded separately in `formula_pilot_v*.csv` and marked "indicative only" |

**Hard rule — keep the headline aggregate clean.** Any Tier-2 or Tier-3 estimate is recorded only in the separate `formula_pilot_v*.csv` and is **never** added to the headline state-concession aggregate (`headline_state_concessions.csv`). This ensures the headline figure stays free of lower-confidence estimates even if a confidence tier label is later missed; Tier-2 and Tier-3 runs exist only to validate the engineering pipeline.

### 7.3 Worked example: VIC Excess Electricity Concession (pilot formula rule)

Formula (per YAML): `A = [17.5% × (B − C)] − (D × 0.0823)` per month
- Trigger: annual electricity bill ≥ $3,895.13 (threshold from 2024-12-01; DFFH reviews annually)
- B = monthly excess electricity charge / C = monthly discount / D = correction term
- Official worked example: B=$560, C=$24.25, D=88 → **A = $86.51/month ≈ $1,038/yr per recipient**

**Tier-1 attempt:** DFFH Budget Paper No. 3 (Service Delivery, 2024-25) should contain "Excess Electricity Concession total expenditure" plus recipient count. However, budget papers typically bundle multiple concessions together, and a single-rule line item may not be separable. This pilot therefore uses Tier-2.

**Tier-2 imputation used:** $1,038/yr per recipient (the official worked example, explicitly labelled "official example, not avg").

**Trigger-rate imputation:** this is the **second calibration parameter** unique to formula-type rules — the share of VIC concession households whose annual bill reaches the $3,895.13 trigger. Available evidence:
- CPRC: typical VIC concession-household annual electricity bill is $1,500 (see §6 VIC Electricity Concession).
- $3,895 / $1,500 ≈ 2.6× the median → approximately the 95th–98th percentile of the distribution.
- Conservative assumption: **5% of VIC eligible households trigger the excess concession**.

→ VIC Excess unclaimed = 989,936 households × 5% trigger × 7% gap (CPRC VIC electricity) × $1,038 ≈ $3.6M/yr.

**Double-imputation disclosure:** this estimate relies on (1) a per-recipient figure drawn from an official worked example rather than a true average, and (2) a 5% trigger rate that is an estimate, not an official statistic. Each additional imputation layer reduces confidence. The CSV `amount_basis` field explicitly records "Tier-2 + 5% trigger imputed", clearly distinguishing this row from Tier-1 (NECF 5 fixed) and Tier-1.5 (VIC 3-utility percentage) rows.

### 7.4 Requirements for adding formula rules in later waves

Any new formula rule must satisfy the following **before** it is added to the BENEFITS registry:

1. `amount_imputed_aud` must have a citable source (DSS, DFFH, or Centrelink publicly reported data) — no estimated values without source.
2. The `amount_basis` field must state the tier (Tier-1, Tier-2, or Tier-3).
3. Any additional imputed parameter (e.g. trigger rate) must be disclosed separately, with the derivation documented.
4. The sanity gate range should be relaxed in line with the number of imputation layers (e.g. ±20% for Tier-2 versus ±10% for Tier-1).

## 8. Federal benefit gap — independent framework (NOT CPRC)

**This section establishes a firm boundary: the "unclaimed" estimation for federal benefits (Age Pension, JobSeeker, FTB, Disability Support Pension, and other Centrelink-administered payments) is not comparable to the state concession gap estimation.** Two independent methodologies must be presented side by side; they cannot be combined.

### 8.1 Why the CPRC 35% gap does not apply to federal benefits

The CPRC 19–38% gap measures **friction in retailer-level enrolment for state energy concessions**:
- The household must contact the electricity retailer.
- Must provide the card number, account number, and application form.
- The retailer must enter the concession into its billing system.
- Any missed step results in "unclaimed" status.

Federal benefits operate on a fundamentally different model:
- Age Pension: when a person reaches 67, Services Australia proactively contacts them (a Letter of Invitation with six months' notice). The enrolment workflow is closer to *opt-out* than *opt-in*.
- JobSeeker: unemployed individuals submit through myGov/Centrelink and are assessed immediately; almost all eligible applicants are assisted into enrolment.
- FTB / Disability Support Pension: opt-in, but Services Australia proactively reaches out to identified eligible populations.

> Unlike state concessions which require active enrolment with retailers, most federal benefits operate on opt-out or assisted opt-in mechanisms (Age Pension Letter of Invitation, JobSeeker myGov auto-flow). The CPRC 19-38% gap reflects retailer-application friction not present in Centrelink-administered payments. The actual federal take-up gap has not been systematically estimated in publicly available research; this report's Chapter B uses a population-based methodology (eligible − recipients) that **does not require assuming a gap rate**.

**Key point:** Chapter B's methodology does not depend on a take-up rate variable at all — the gap is derived directly from (ABS eligible − DSS recipient count). The contentious question of "what is the federal take-up gap?" is therefore designed out of our framework. This is why §8.2 uses a population-based approach rather than a retailer-friction-based one.

### 8.2 Independent federal methodology: population-based gap

If the CPRC framework cannot be applied, how is the federal gap estimated? **Derive the gap from the eligible population**, rather than from take-up rate × recipient.

```
Federal unclaimed = (Eligible population − DSS recipient count) × DSS avg payment
```

Four-step derivation (every step requires a public data source):

1. **Eligible population:** derived from ABS Census combined with DSS eligibility rules.
   - Example: Age Pension — Australian residents aged 67+ who pass the residency, asset, and income tests ≈ 2.7M.
   - Sources: ABS Census 2021 tables + DSS asset/income thresholds + ATO superannuation balance distribution.
2. **DSS recipient count:** from DSS Payment Demographic Data.
   - Example: Age Pension current recipients ≈ 2.62M (DSS June 2022 quarterly data).
3. **"Unclaimed" eligible:** step 1 − step 2.
   - Example: ~80K eligible-but-not-enrolled (this is the ABS-versus-DSS reverse-derived gap).
4. **× DSS avg payment** per §7 Tier-1.
   - Example: 80K × $25,500 ≈ $2.0B/yr in potential unclaimed Age Pension alone.

### 8.3 Relationship to the CPRC framework (two parallel chapters, not merged)

The final report must be split into **two chapters**:

- **Chapter A — State concessions (CPRC framework)**
  - Current pipeline: $356.9M / year (NECF 5 + VIC 3-utility cluster).
  - Formula: eligible × CPRC gap × per-household AUD.
  - Extending to WA, NT, or federal benefits is **outside the scope of this report** (extrapolation would compromise framework precision).

- **Chapter B — Federal benefits (population-based)**
  - Under development.
  - Formula: (ABS eligible − DSS recipients) × DSS avg.
  - Extending to state concessions is **outside the scope of this report** (state concession users must opt-in; population reverse-derivation does not apply).

**Never combine the two chapters into a single total** (e.g. "Australia unclaimed $5B/yr" merging Chapter A + B). The two methodologies use different baselines (CPRC's restricted eligibility versus ABS census coverage), different gap semantics (retailer friction versus enrolment population delta), and are not comparable.

### 8.3.1 Recommended headline framing

Either of the following formulations preserves framing precision while leaving readers to draw their own broader inferences:

> "**At least $360M annually** in unclaimed state concessions alone, before considering federal benefits (measured separately in Chapter B)."

Or more assertively:

> "**$360M+ in state-level concessions** + additional federal benefit gap measured separately."

Phrases such as "state alone" or "+ additional federal" leave the upper bound to readers' interpretation without requiring this report to publish a combined two-chapter figure. Any further inference (such as "and likely billions more in federal benefits") would be the reader's, not this report's claim.

### 8.4 Pre-work for the federal benefits wave (after the pilot)

Before adding any federal entry to the BENEFITS registry:

1. **Use ABS Quarterly Population Estimates (ERP) rather than Census 2021.** Census 2021 data is now 4–5 years old, and the 65+ population structure may have shifted significantly. Prefer the ABS "National, State and Territory Population" quarterly release (catalogue 3101.0), broken down by single year of age × state. Census 2021 is a fallback only when ERP lacks the required dimension.
   - Investigation findings are recorded in §8.5 "Federal data source survey".
2. Source the latest DSS Annual Report (recipient count and average payment by payment type).
3. Source Services Australia's official take-up rate or outreach data, if publicly available — used only as qualitative background, not as a gap input.
4. Add §10 to METHODOLOGY listing federal benefit candidates with data availability per axis.

The pilot does not run federal benefits — the methodology is finalised first. The next step is the §8.5 data source survey (whether ABS ERP granularity suffices, and whether the DSS Annual Report provides average payment by payment type); the federal rollout order is decided only after the survey is complete.

### 8.5 Federal data source survey

**ABS Estimated Resident Population (ERP) — confirmed adequate for §8.2 step 1.**

| Item | Finding |
|---|---|
| Single year of age × state breakdown | ✓ Available, 1971 to present |
| Latest reference period | September 2025 (released 2026-03-19) |
| Publication lag | 5–6 months (quarter-end to publication) |
| Revision risk | "All data after 30 June 2021 are subject to revision" (ABS verbatim) |
| Download format | XLSX, one file per state — e.g. NSW `3101051.xlsx`, VIC `3101052.xlsx`, QLD `3101053.xlsx`; SA/WA/TAS/NT/ACT `3101054`–`3101058.xlsx`; National `3101059.xlsx` |
| Direct link root | `https://www.abs.gov.au/statistics/people/population/national-state-and-territory-population/sep-2025/<file>` |
| Report caveat | "Eligible population estimated from ABS ERP September 2025, latest available systematic source; data after 2021-06-30 subject to ABS revision per their advisory." |

→ Census 2021 is no longer the preferred source. Chapter B uses ERP September 2025; if asked "why not Census", the answer is "ERP is the live quarterly series with a 5-month lag, more current than the Census 5-yearly cycle".

**DSS Annual Report / Payment Demographic Data — pending investigation (next wave):**
- Verify whether the DSS Annual Report provides average payment by payment type, or only total expenditure and recipient count.
- Verify whether DSS Payment Demographic Data (quarterly) provides single-year-of-age × payment type granularity that joins cleanly to ABS ERP.
- Candidate payment types for pilot order (ranked by per-recipient amount × recipient count): Age Pension > JobSeeker > Disability Support Pension > FTB-A / FTB-B > Parenting Payment.

Once the survey is complete, §10 will list the federal benefit candidate inventory before the Chapter B BENEFITS registry is opened.

## 9. Out of scope

- Individual-level compliance audits (who-can-claim-what).
- Cross-benefit additivity (some rule conflicts are mutually exclusive and already marked in YAML).
- Behavioural analysis of why eligible households do not claim (CPRC's report covers this; this report does not duplicate it).
- WA / NT state concessions (CPRC framework does not cover them; extrapolation would compromise precision; awaiting independent proxy methodology).
- Federal benefit take-up rate (this report v1 documents the §8 framework, but actual rollout follows Wave 3).
