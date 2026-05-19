# Inputs — AU_QLD_ELECTRICITY_REBATE

## Rule (YAML)

| Field | Value | Source |
|---|---|---|
| rule_id | `AU_QLD_ELECTRICITY_REBATE` | YAML rule schedule |
| parent_cluster | QLD Electricity Rebate | YAML |
| amount.type | fixed | YAML |
| amount.period | yearly | YAML |
| **amount.value** | **386.34** AUD | YAML (concessionsfinder.services.qld.gov.au 2025-26 official) |
| entitlement_scope.subject | household | YAML |

### Eligibility (structural)
- `state = QLD`
- `concession_card_type ∈ {PCC, HCC, DVA Gold, Seniors Card QLD}`
- `electricity_bill_account_holder = true`
- `principal_place_of_residence = true`

### Notes (comment-only)
- YAML accepts Seniors Card QLD; CPRC Fig 1 (p7) does NOT include Seniors Card QLD in its NECF eligibility model (only PCC + HCC + DVA Gold). Direction: CPRC denominator is narrower than actual QLD rule → our estimate uses CPRC narrower base → conservative.
- LIHCC counted within HCC per Services Australia data convention.

## Eligible household count (CPRC native)

Source: CPRC *Mind the Gap* Figure 2 (p11), NECF states Q3 2021-22

| | QLD |
|---|---|
| Total eligible concession **holders** (DSS June 2022 + DVA March 2022) | **1,251,305** |
| Eligible **households** after 0.70 weighting (CPRC formula) | **875,914** |
| Published concessions **claimed** (AER Q3 2021-22) | 620,614 |
| **Implied unclaimed households** (= eligible − claimed) | **255,300** (29.1%) |

Row 2 of `report/data/cprc/cprc_state_rates.csv`.

## Unclaimed rate

| | Value | Source |
|---|---|---|
| QLD NECF gap rate (2021-22 Q3) | **29%** | CPRC Mind the Gap Figure 3 (p11) |
| Independent corroboration | None available | CPRC p7: "could not identify any publicly available data about the size of the gap in other states" |

29% used as the primary rate. No second source for QLD; relies on CPRC single-source analysis. NSW corroboration (DPE 36% vs CPRC 35%, ≤1pp) is the proxy validation for the broader NECF methodology.

## Cluster representative choice

QLD Electricity Rebate is a single-rule cluster — no retail/on-supply or sub-variant split. The rule covers the full QLD primary electricity concession cohort.

## Conservative direction

1. CPRC adopts conservative eligibility criteria — "the actual gap... may be greater" (CPRC p8)
2. 0.70 dedup x=2 assumption likely overestimates households (CPRC p9: "may be 3 or more cards") → final AUD underestimated
3. CPRC excludes Seniors Card QLD which the actual rule accepts → eligible cohort narrower than reality → AUD underestimated

→ Three directions converge on conservative direction.
