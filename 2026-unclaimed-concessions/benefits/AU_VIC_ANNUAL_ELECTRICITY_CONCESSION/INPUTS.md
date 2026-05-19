# Inputs — AU_VIC_ANNUAL_ELECTRICITY_CONCESSION

## Rule (YAML)

| Field | Value | Source |
|---|---|---|
| rule_id | `AU_VIC_ANNUAL_ELECTRICITY_CONCESSION` | YAML rule schedule |
| parent_cluster | VIC Electricity Concession | YAML |
| amount.type | **percentage** | YAML |
| amount.period | ongoing | YAML |
| amount.base_rate | **0.175** (17.5%) | YAML |
| **amount_imputed_aud** (Tier-1.5) | **262.50** AUD / yr | See §"Amount imputation" below |
| entitlement_scope.subject | household | YAML |

### Eligibility (structural)
- `state = VIC`
- `concession_card_type ∈ {PCC, HCC, DVA Gold}`
- `electricity_bill_account_holder = true`
- `principal_place_of_residence = true`
- **excludes**: CSHC + Seniors Card

### Notes (comment-only)
- Formula structurally: 17.5% × (annual electricity bill − first $171.60 supply charge). Excess Electricity Concession (AU_VIC_EXCESS_ELECTRICITY_CONCESSION) replaces this when annual bill > $3,895.13 — see formula_pilot_v1.csv (out of headline).

## Eligible household count (CPRC native)

Source: CPRC *Mind the Gap* Figure 4 (p13), Victoria 2021-22

| | VIC (electricity) |
|---|---|
| Total eligible concession **holders** (DSS June 2022 + DVA March 2022) | **1,414,194** |
| Eligible **households** after 0.70 dedup weighting | **989,936** |
| Published concessions **claimed** (DFFH 2021-22) | 924,888 |
| **Implied unclaimed households** (= eligible − claimed) | **65,048** (6.6%, rounds to 7%) |

Row 6 of `report/data/cprc/cprc_state_rates.csv`.

## Unclaimed rate

| | Value | Source |
|---|---|---|
| VIC electricity gap rate (2021-22) | **7%** (lowest of any AU jurisdiction) | CPRC Mind the Gap Figure 5 (p13) |
| Cross-source corroboration (related framework) | DHHS 2015 Survey: 87% of VIC concession card households received electricity concession (= 13% gap) | CPRC endnote 9 / DHHS *Victorian Utility Consumption Household Survey 2015*, p153 |

7% used as the primary rate (CPRC most recent published systematic estimate). 13% legacy figure aligns to within 6pp, indicating order-of-magnitude consistency.

**Important**: CPRC explicitly warns (p9): "NECF and VIC may not be comparable" — different methodology (DFFH retailer monthly returns vs AER quarterly returns). VIC and NECF should NEVER be combined in a single weighted gap rate.

## Amount imputation (Tier-1.5: percentage rule with retailer-data-backed standard)

YAML gives the discount rate (17.5%) but not a dollar amount. To compute unclaimed AUD we standardise on a typical concession-household electricity bill.

- **Standardised annual electricity bill**: **$1,500/yr** per VIC concession household
- Source: AER Retail Market Performance Q3 2021-22 retailer reporting on actual concession-household median bills (CPRC endnote 11). Conservative against the unrestricted-population benchmark of ~$2,000/yr.
- **Imputed per-household concession**: 17.5% × $1,500 = **$262.50/yr**

This is one tier below Tier-1 (DSS publicly reported avg per recipient) because the imputation chain involves both a published bill figure and a multiplication step. METHODOLOGY §6 details.

## Cluster representative choice

VIC Electricity Concession cluster contains multiple rules:
- AU_VIC_ANNUAL_ELECTRICITY_CONCESSION (this rule, 17.5% — covers full eligible cohort) ← **selected for pilot**
- AU_VIC_CONTROLLED_LOAD_ELECTRICITY (13% off, controlled load tariff, narrower cohort) — not in pilot
- AU_VIC_EXCESS_ELECTRICITY_CONCESSION (formula, bill > $3,895.13 — narrow high-bill cohort) — in formula_pilot_v1.csv, not in headline
- AU_VIC_MEDICAL_COOLING_CONCESSION (17.5%, narrow medical cohort) — not in pilot

Annual Electricity Concession is the primary / default VIC electricity concession covering the broadest cohort, hence used as cluster representative for headline.

## Conservative direction

1. CPRC adopts conservative eligibility criteria — "the actual gap... may be greater" (CPRC p8)
2. 0.70 dedup x=2 assumption likely overestimates households → final AUD underestimated
3. $1,500 standardised bill is at lower end of retailer-reported median range (vs $2,000 unrestricted-population) → AUD underestimated
4. Cluster representative chosen as Annual variant; ignoring Controlled Load + Medical Cooling additive sub-cohorts → AUD slightly underestimated

→ All four directions converge on conservative direction.
