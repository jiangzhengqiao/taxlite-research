# Inputs — AU_VIC_WINTER_GAS_CONCESSION

## Rule (YAML)

| Field | Value | Source |
|---|---|---|
| rule_id | `AU_VIC_WINTER_GAS_CONCESSION` | YAML rule schedule |
| parent_cluster | VIC Gas Concession | YAML |
| amount.type | **percentage** | YAML |
| amount.period | ongoing (winter only: 1 May – 31 Oct) | YAML |
| amount.base_rate | **0.175** (17.5%) | YAML |
| **amount_imputed_aud** (Tier-1.5) | **80.00** AUD / yr | See §"Amount imputation" below |
| entitlement_scope.subject | household | YAML |

### Eligibility (structural)
- `state = VIC`
- `concession_card_type ∈ {PCC, HCC, DVA Gold}`
- `gas_bill_account_holder = true`
- `principal_place_of_residence = true`

### Notes (comment-only)
- Discount applies only to winter gas bills (1 May to 31 Oct). Computation: 17.5% × (winter gas bill − first $62.40 supply charge).
- AU_VIC_EXCESS_GAS_CONCESSION (formula, winter bill > $2,499.14) is a separate rule for very-high-bill cohort; not in pilot.

## Eligible household count (CPRC native)

Source: CPRC *Mind the Gap* Figure 4 (p13), Victoria 2021-22

| | VIC (gas) |
|---|---|
| Total eligible concession **holders** (DSS June 2022 + DVA March 2022) | **1,414,194** |
| Eligible **households** after 0.70 dedup × **0.76 mains-gas secondary weighting** | **752,351** |
| Published concessions **claimed** (DFFH 2021-22) | 658,831 |
| **Implied unclaimed households** (= eligible − claimed) | **93,520** (12.4%) |

Row 7 of `report/data/cprc/cprc_state_rates.csv`.

**Note on 0.76 secondary weighting**: CPRC Fig 4 footnote *** explains that Energy Networks Australia (ENA) 2021 reports 76% of all VIC households have mains gas connections. CPRC applies this rate to estimate the share of concession card holders connected to mains gas (the eligible cohort for the Winter Gas Concession). The 0.70 primary dedup is applied first, then 0.76 secondary.

## Unclaimed rate

| | Value | Source |
|---|---|---|
| VIC gas gap rate (2021-22) | **12%** | CPRC Mind the Gap Figure 5 (p13) |
| Cross-source corroboration (legacy framework) | DHHS 2015 Survey: 74% of VIC concession card households received gas concession (= 26% gap) | CPRC endnote 9 / DHHS *Victorian Utility Consumption Household Survey 2015*, p153 |

12% used as the primary rate (CPRC most recent published systematic estimate). 26% legacy DHHS figure diverges materially; CPRC discussion (p15) acknowledges: "If the true proportion of eligible Victorians receiving a concession on their bill is significantly lower than the reported figures, this would warrant further investigation as to what causes consumers to miss out on their concessions." → Conservative reading: actual gap is likely **larger** than 12%.

## Amount imputation (Tier-1.5: percentage rule with seasonal adjustment)

YAML gives the discount rate (17.5%) and winter-only period (~50% of annual gas usage). Standardisation:

- Typical VIC concession-household **annual gas bill**: ~$900/yr (estimate aligned with retailer reporting)
- **Winter share** of annual gas usage: ~50%
- → Winter spend exposed to concession: ~$450/yr
- **Imputed per-household concession**: 17.5% × $450 ≈ **$80/yr** per gas-eligible household

This is Tier-1.5 with explicit seasonal adjustment disclosed. METHODOLOGY §6 details.

## Cluster representative choice

VIC Gas Concession cluster contains:
- AU_VIC_WINTER_GAS_CONCESSION (this rule, 17.5% winter — full eligible cohort) ← **selected for pilot**
- AU_VIC_EXCESS_GAS_CONCESSION (formula, winter bill > $2,499.14) — narrow high-bill cohort, not in pilot

Winter Gas is the default VIC gas concession covering the broadest cohort.

## Conservative direction

1. CPRC adopts conservative eligibility criteria — "the actual gap... may be greater" (CPRC p8)
2. 0.70 dedup x=2 assumption likely overestimates households → final AUD underestimated
3. **CPRC 12% gap may understate true gap**: DHHS 2015 legacy figure is 26%; CPRC explicitly says further investigation warranted (p15)
4. $80/yr imputed amount excludes Excess Gas Concession high-bill cohort additive → slight underestimate

→ All four directions converge on conservative direction. VIC gas estimate may be **substantially** underestimated relative to DHHS legacy methodology.
