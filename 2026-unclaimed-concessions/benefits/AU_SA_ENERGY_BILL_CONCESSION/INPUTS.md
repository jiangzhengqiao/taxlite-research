# Inputs — AU_SA_ENERGY_BILL_CONCESSION

## Rule (YAML)

| Field | Value | Source |
|---|---|---|
| rule_id | `AU_SA_ENERGY_BILL_CONCESSION` | YAML rule schedule |
| parent_cluster | SA Energy Bill Concession | YAML |
| amount.type | fixed | YAML |
| amount.period | yearly | YAML |
| **amount.value** | **281.78** AUD | YAML (2025-26 official, applied daily on bill) |
| entitlement_scope.subject | household | YAML |

### Eligibility (structural)
- `state = SA`
- `concession_card_type ∈ {PCC, DVA Gold, HCC, CSHC}`
- `electricity_bill_account_holder = true`
- `principal_place_of_residence = true`

### Notes (comment-only)
- YAML accepts CSHC (Commonwealth Seniors Health Card); CPRC Fig 1 (p7) does NOT include CSHC in its NECF eligibility model. Direction: CPRC denominator is narrower than actual SA rule → our estimate uses CPRC narrower base → conservative.
- LIHCC counted within HCC per Services Australia data convention.

## Eligible household count (CPRC native)

Source: CPRC *Mind the Gap* Figure 2 (p11), NECF states Q3 2021-22

| | SA |
|---|---|
| Total eligible concession **holders** (DSS June 2022 + DVA March 2022) | **486,527** |
| Eligible **households** after 0.70 weighting (CPRC formula) | **340,569** |
| Published concessions **claimed** (AER Q3 2021-22) | 210,584 |
| **Implied unclaimed households** (= eligible − claimed) | **129,985** (38.2%) |

Row 3 of `report/data/cprc/cprc_state_rates.csv`.

## Unclaimed rate

| | Value | Source |
|---|---|---|
| SA NECF gap rate (2021-22 Q3) | **38%** (highest of NECF 5) | CPRC Mind the Gap Figure 3 (p11) |
| Independent corroboration | None available | CPRC p7: "could not identify any publicly available data about the size of the gap in other states" |

38% used as the primary rate — the highest NECF state gap. CPRC discussion (p15) does not attribute a specific cause for SA's higher gap, but notes SA's restrictive caveat that excludes households with another member earning more than $3,000/yr (per CPRC p17 quoting Marks & Ogle 2021 *The State of Concessions in South Australia*). This restrictive eligibility may correlate with administrative complexity → take-up friction.

## Cluster representative choice

SA Energy Bill Concession is a single-rule cluster. Note: SA also has separate AU_SA_COST_OF_LIVING_CONCESSION and AU_SA_SACEDO (SA Concessional Energy Discount Offer) which are different programs — not included in this pilot's primary-electricity-concession scope.

## Conservative direction

1. CPRC adopts conservative eligibility criteria — "the actual gap... may be greater" (CPRC p8)
2. 0.70 dedup x=2 assumption likely overestimates households → final AUD underestimated
3. CPRC excludes CSHC which actual SA rule accepts → eligible cohort narrower than reality → AUD underestimated

→ Three directions converge on conservative direction.
