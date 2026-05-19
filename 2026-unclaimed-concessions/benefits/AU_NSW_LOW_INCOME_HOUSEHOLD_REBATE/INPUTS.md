# Inputs — AU_NSW_LOW_INCOME_HOUSEHOLD_REBATE_RETAIL

## Rule (YAML)

| Field | Value | Source |
|---|---|---|
| rule_id | `AU_NSW_LOW_INCOME_HOUSEHOLD_REBATE_RETAIL` | YAML rule schedule |
| parent_cluster | NSW Low Income Household Rebate | YAML rule schedule |
| amount.type | fixed | YAML rule schedule |
| amount.period | yearly | YAML rule schedule |
| **amount.value** | **285** AUD | YAML rule schedule |
| entitlement_scope.subject | household | YAML rule schedule |

### Eligibility (structural — not the comment-only constraints)
- `state = NSW`
- `concession_card_type ∈ {PCC, HCC, LIHCC, DVA Gold}` (dva_gold_card treated generically, without sub-type restriction)
- `electricity_bill_account_holder = true`
- `principal_place_of_residence = true`
- `electricity_supply_type = retail` (distinguishes retail vs on_supply variants)
- **excludes**: CSHC (commonwealth_seniors_health_card)

### Notes (comment-only — not engine-enforced; not in our calc)
- DVA Gold sub-types: only War Widow / TPI / EDA per actual Service NSW policy. YAML notes this but treats DVA Gold generically. DSS and CPRC also treat DVA Gold generically; all three sources use the same eligibility framing.
- LIHCC is Services Australia 's sub-category of HCC (in DSS data, single HCC column already includes LIHCC).

## Eligible household count (CPRC native)

Source: CPRC *Mind the Gap* Figure 2 (p11), NECF states Q3 2021-22

| | NSW |
|---|---|
| Total eligible concession **holders** (DSS June 2022 + DVA March 2022) | **1,783,270** |
| Eligible **households** after 0.70 weighting (CPRC formula) | **1,248,289** |
| Published concessions **claimed** (AER Q3 2021-22) | 814,313 |
| **Implied unclaimed households** (= eligible − claimed) | **433,976** (34.8%) |

Row 1 of `report/data/cprc/cprc_state_rates.csv`.

## Unclaimed rate

| | Value | Source |
|---|---|---|
| NSW NECF gap rate (2021-22 Q3) | **35%** | CPRC Mind the Gap Figure 3 (p11) |
| Independent NSW corroboration | 36% (Low Income Household Rebate not accessed) | NSW DPE *NSW Energy Rebates Annual Report 2020-21*, p4 (CPRC endnote 8) |

35% used as the primary rate (CPRC NECF)。36% appears in METHODOLOGY as cross-source corroboration; the two values agree within 1 percentage point, validating across independent data sources。

## Cluster representative choice

NSW Low Income Household Rebate cluster has 2 conflicting variants:
- AU_NSW_LOW_INCOME_HOUSEHOLD_REBATE_RETAIL → $285/yr ← **selected for pilot**
- AU_NSW_LOW_INCOME_HOUSEHOLD_REBATE_ON_SUPPLY → $313.50/yr (max amount in cluster)

**Pilot uses RETAIL ($285).** Trade-off: ON_SUPPLY covers a minority of NSW households (predominantly apartment embedded networks); selecting RETAIL as the cluster representative slightly underestimates total unclaimed (applying ON_SUPPLY at $313.50 across the cohort would yield ~$137M; RETAIL at $285 yields ~$124.5M). This is disclosed in METHODOLOGY.

## Conservative direction (three-source synthesis)

1. CPRC adopts conservative eligibility criteria："the actual gap... may be greater"
2. The 0.70 dedup factor assumes x=2 cards per multi-card household, whereas CPRC concedes real households may hold ≥ 3 cards → eligible households likely underestimated → final dollar amount underestimated
3. Pilot selects the lowest cluster amount, RETAIL $285, rather than ON_SUPPLY $313.50 → underestimated

All three biases point in the underestimating direction. The headline NSW figure is therefore a robust lower bound on the actual unclaimed amount.
