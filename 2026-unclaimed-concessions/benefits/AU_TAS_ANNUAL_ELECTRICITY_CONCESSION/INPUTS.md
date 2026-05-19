# Inputs — AU_TAS_ANNUAL_ELECTRICITY_CONCESSION

## Rule (YAML)

| Field | Value | Source |
|---|---|---|
| rule_id | `AU_TAS_ANNUAL_ELECTRICITY_CONCESSION` | YAML rule schedule |
| parent_cluster | TAS Energy Rebates | YAML |
| amount.type | fixed | YAML |
| amount.period | yearly | YAML |
| **amount.value** | **645.56** AUD | YAML ($1.76866 daily × 365 days) |
| entitlement_scope.subject | household | YAML |

### Eligibility (per YAML)
- `state = TAS`
- `concession_card_type ∈ {PCC, HCC, DVA Gold}`
- `electricity_bill_account_holder = true`
- `principal_place_of_residence = true`

## Eligible household count (CPRC native)

Source: CPRC *Mind the Gap* Figure 2 (p11), NECF states Q3 2021-22

| | TAS |
|---|---|
| Total eligible concession **holders** | **164,726** |
| Eligible **households** after 0.70 weighting | **115,308** |
| Published concessions **claimed** (AER Q3 2021-22) | 93,889 |
| Implied unclaimed households (= eligible − claimed) | 21,419 (≈ 19%) |

## Key methodological note — DVA Gold exclusion

**TAS energy concession eligibility per CPRC *Mind the Gap* Figure 1 (p7 of the PDF, "energy concession/rebate eligibility criteria") excludes DVA Gold cardholders.** TAS is the only NECF state that does not include DVA Gold in its energy concession framework.

CPRC's reported eligible card count of 164,726 for TAS therefore reflects **PCC + HCC only** (not DVA Gold). This is consistent with TAS's actual concession framework (see Aurora Energy / Hydro Tasmania concession registration). Our pilot inherits CPRC's count and methodology.

The YAML rule `concession_card_type` field includes `dva_gold_card` for forward compatibility, but our eligible-population count uses CPRC's published TAS-specific figure which excludes that cohort. There is no double counting and no missing population — TAS DVA Gold holders are not eligible for the Annual Electricity Concession.

Verification path for journalists/editors:
- CPRC Mind the Gap PDF, p7, Figure 1 — the TAS column has no ✓ under "Gold Veterans Concession Card"
- The same Figure 1 footnote 8 confirms the eligibility criteria source: state departmental websites

## Unclaimed rate

| | Value | Source |
|---|---|---|
| TAS NECF gap rate (2021-22 Q3) | **19%** (lowest of NECF 5) | CPRC Mind the Gap Figure 3 (p11) |

CPRC discussion (p15): "Tasmania is served by a single provider for the majority (97%) of residential consumers, which may reduce the incidence of consumers missing out on concessions through switching energy provider and moving residence."

## Conservative direction

Same as other NECF states: CPRC limited eligibility + 0.70 dedup x=2 → AUD likely under-estimated. The TAS framework's exclusion of DVA Gold is reflected in CPRC's count and is not a separate bias.
