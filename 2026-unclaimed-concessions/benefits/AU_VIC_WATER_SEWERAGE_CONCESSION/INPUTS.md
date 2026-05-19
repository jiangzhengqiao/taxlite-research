# Inputs — AU_VIC_WATER_SEWERAGE_CONCESSION

## Rule (YAML)

| Field | Value | Source |
|---|---|---|
| rule_id | `AU_VIC_WATER_SEWERAGE_CONCESSION` | YAML rule schedule (card-linked) |
| parent_cluster | VIC Water Concession | YAML |
| amount.type | **percentage** with cap | YAML |
| amount.period | ongoing | YAML |
| amount.base_rate | **0.50** (50% discount) | YAML |
| amount.cap | **$372.10/yr** water + sewerage (2025-26 DFFH official); water-only cap $186.05/yr | YAML |
| **amount_imputed_aud** (Tier-1.5) | **250.00** AUD / yr | See §"Amount imputation" below |
| entitlement_scope.subject | household | YAML |

### Eligibility (structural)
- `state = VIC`
- `concession_card_type ∈ {PCC, DVA Gold}` ← **HCC NOT accepted by actual DFFH rule**
- `is_water_account_holder = true`
- `principal_place_of_residence = true`

### Notes (comment-only)
- **HCC exclusion**: The actual DFFH rule for Water & Sewerage Concession accepts only PCC + DVA Gold. HCC holders are NOT eligible (per services.dffh.vic.gov.au/water-and-sewerage-concession YAML rule_url confirms).
- Water-only households cap is $186.05/yr; combined water + sewerage cap is $372.10/yr.

## Eligible household count (CPRC native — with methodology discrepancy)

Source: CPRC *Mind the Gap* Figure 4 (p13), Victoria 2021-22

| | VIC (water) |
|---|---|
| Total eligible concession **holders** (DSS June 2022 + DVA March 2022) | **1,414,194** |
| Eligible **households** after 0.70 dedup × **0.88 water-bill-payer secondary weighting** | **871,143** |
| Published concessions **claimed** (DFFH 2021-22) | 680,191 |
| **Implied unclaimed households** (= eligible − claimed) | **190,952** (21.9%, rounds to 22%) |

Row 8 of `report/data/cprc/cprc_state_rates.csv`.

**Note on 0.88 secondary weighting**: CPRC Fig 4 footnote ** explains: "DHHS 2015 survey found 88% of concession card holders paid a water bill. Absent a more current update we've applied this secondary weighting of 0.88 to estimate the total number of eligible concession households." The 0.70 primary dedup is applied first, then 0.88 secondary.

## Critical methodological discrepancy — CPRC denominator vs DFFH rule eligibility

CPRC's VIC water denominator (1,414,194 cards / 871,143 households) uses the SAME source population as VIC electricity and VIC gas — i.e. it **includes HCC holders**. But the actual DFFH Water & Sewerage Concession rule **excludes HCC holders** (PCC + DVA Gold only).

**Direction of effect**:
- CPRC denominator is INFLATED (includes HCC who are not eligible)
- Published claimed count (DFFH 680,191) is correct (DFFH only enrols PCC + DVA Gold)
- Therefore the 22% CPRC gap rate is inflated upward
- Our $47.9M VIC water estimate likely slightly **overstates** the true unclaimed amount

**This is the only line in the headline aggregate where the conservative-direction guarantee breaks**. METHODOLOGY §6 includes full disclosure. The over-statement magnitude is bounded: if HCC share among PCC+HCC+DVA Gold is ~30% (informed estimate; not separately published by CPRC), the true VIC water unclaimed AUD could be ~$33M instead of $47.9M — still a material number but ~$15M lower than headline.

For the report's framing, this single line is offset by conservative directions on every other line. The headline $356.9M aggregate remains conservative in net direction.

## Unclaimed rate

| | Value | Source |
|---|---|---|
| VIC water gap rate (2021-22) | **22%** | CPRC Mind the Gap Figure 5 (p13) |
| Cross-source corroboration | DHHS 2015 Survey: 78% of VIC concession card households received water concession (= 22% gap, identical) | CPRC endnote 9 / DHHS *Victorian Utility Consumption Household Survey 2015*, p153 |

22% used as the primary rate. DHHS 2015 figure independently aligns at 22% identical to CPRC — strong cross-source consistency. **This 22% gap is 3× the VIC electricity gap (7%) and ~2× the VIC gas gap (12%)** — a CPRC-highlighted anomaly (p14) discussed in our REPORT_V1 §4.

## Amount imputation (Tier-1.5: cap-and-bill standardisation)

Standardisation logic:
- 50% discount up to cap $372.10/yr (2025-26 DFFH official)
- Typical water bill profile: most concession households reach but do not exhaust cap
- **Imputed per-household concession**: **$250/yr** (≈ 67% of cap, conservative)
- Cap-only scenarios would imply $372.10/yr per household → $71M unclaimed; we use $250 → $47.9M

METHODOLOGY §6 details.

## Cluster representative choice

VIC Water Concession cluster contains:
- AU_VIC_WATER_SEWERAGE_CONCESSION (this rule, 50% cap $372.10 — mains water + sewerage cohort) ← **selected for pilot**
- AU_VIC_NON_MAINS_WATER_CONCESSION (separate rule, non-mains carting/tank cohort) — much smaller cohort, not in pilot

## Conservative direction (qualified — water is the exception)

1. CPRC adopts conservative eligibility criteria — "the actual gap... may be greater" (CPRC p8) → conservative
2. 0.70 dedup x=2 assumption likely overestimates households → underestimates AUD → conservative
3. $250/yr imputed amount is ~67% of $372.10 cap → conservative
4. **Qualifier**: CPRC denominator includes HCC but DFFH rule excludes HCC → AUD overstated by ~30% → **non-conservative**

→ Net direction unclear; possibly slight overstatement vs other 7 headline lines. The $47.9M figure is treated transparently in REPORT_V1 with disclosure; aggregate $356.9M remains conservative in net.
