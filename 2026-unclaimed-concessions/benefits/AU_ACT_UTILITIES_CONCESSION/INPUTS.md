# Inputs — AU_ACT_UTILITIES_CONCESSION

## Rule (YAML)

| Field | Value | Source |
|---|---|---|
| rule_id | `AU_ACT_UTILITIES_CONCESSION` | YAML rule schedule |
| parent_cluster | ACT Utilities Concession | YAML |
| amount.type | fixed | YAML |
| amount.period | yearly | YAML |
| **amount.value** | **800.00** AUD | YAML (2025-26 permanent uplift +$50, covers electricity + gas + water bundled) |
| entitlement_scope.subject | household | YAML |

### Eligibility (structural)
- `state = ACT`
- `concession_card_type ∈ {PCC, HCC, DVA Gold}`
- `electricity_bill_account_holder = true`
- `principal_place_of_residence = true`

### Notes (comment-only)
- CPRC Fig 1 (p7) ACT column footnote: "*Stakeholders noted additional eligibility criteria for those with HCCs in the ACT - however published data was unavailable for inclusion in our modelling." CPRC's ACT eligible population (59,135 cards / 41,407 households) may slightly over-count HCC cohort due to this unmodelled criterion. Direction: ACT eligible cohort possibly **over**-stated in CPRC → our $10.3M estimate may be slightly **overstated** for ACT (the only non-conservative direction in NECF 5).
- LIHCC counted within HCC per Services Australia data convention.

## Eligible household count (CPRC native)

Source: CPRC *Mind the Gap* Figure 2 (p11), NECF states Q3 2021-22

| | ACT |
|---|---|
| Total eligible concession **holders** (DSS June 2022 + DVA March 2022) | **59,135** |
| Eligible **households** after 0.70 weighting (CPRC formula) | **41,407** |
| Published concessions **claimed** (AER Q3 2021-22) | 28,505 |
| **Implied unclaimed households** (= eligible − claimed) | **12,902** (31.2%) |

Row 5 of `report/data/cprc/cprc_state_rates.csv`.

## Unclaimed rate

| | Value | Source |
|---|---|---|
| ACT NECF gap rate (2021-22 Q3) | **31%** (revised 2022-11 from original 41%) | CPRC Mind the Gap Figure 3 (p11) |
| Independent corroboration | None available | CPRC p7: "could not identify any publicly available data about the size of the gap in other states" |

31% used as the primary rate. Note: original 2022-11 release of CPRC Mind the Gap reported ACT at 41%; this was revised to 31% in the 2022-11-09 update (per CPRC Update notation on cover page). All numbers in this report use the corrected 31%.

## Cluster representative choice

ACT Utilities Concession is a single-rule cluster covering electricity + gas + water as a bundled concession at $800/yr fixed. This makes it structurally different from NECF electricity-only concessions in other states (NSW/QLD/SA/TAS), but CPRC's NECF gap rate is applied uniformly across NECF jurisdictions in the published methodology.

## Conservative direction (qualified)

1. CPRC adopts conservative eligibility criteria — "the actual gap... may be greater" (CPRC p8)
2. 0.70 dedup x=2 assumption likely overestimates households → final AUD underestimated
3. **Qualifier**: ACT-specific HCC criterion not modelled by CPRC may inflate ACT eligible cohort slightly → AUD slightly **overstated** (deviation from other 4 NECF states where direction is conservative)

→ Two conservative + one slight overstatement. Net direction unclear but small magnitude; ACT is only $10.3M of $356.9M headline (2.9%), so the qualifier doesn't materially affect total framing.
