# CPRC Mind the Gap — Key Extracts

All page numbers refer to printed page numbers in the PDF (cprc-printed footer), not PDF reader page indices.

## 1. Headline figures

### NECF state unclaimed rates (2021-22 Q3 data) — Executive Summary p4 + Map p10

| State | Did NOT receive concession | Received |
|---|---|---|
| **SA**  | **38%** | 62% |
| **NSW** | **35%** | 65% |
| **ACT** | **31%** (revised 2022-11-09; originally 41%) | 69% |
| **QLD** | **29%** | 71% |
| **TAS** | **19%** | 81% |

Source: Figure 3, p11. Also map p10 (Figure 2).

### Victoria (separate methodology — DO NOT mix with NECF) — p4 + p13

| Utility | Did NOT receive concession | Received |
|---|---|---|
| Electricity | **7%** | 93% |
| Gas         | **12%** | 88% |
| Water       | **22%** | 78% |

Source: Figure 4 / Figure 5, p13. CPRC explicit caveat (p9): "NECF and VIC may not be comparable."

## 2. Eligible population data — KEY for downstream calculations

### NECF states (Figure 2, p11) — 2021-22 Q3

| Metric | NSW | QLD | SA | TAS | ACT |
|---|---|---|---|---|---|
| Total eligible concession card **holders** (DSS+DVA, June 2022) | 1,783,270 | 1,251,305 | 486,527 | 164,726 | 59,135 |
| Eligible **households** (cards × 0.70 weighting)                | 1,248,289 |   875,914 | 340,569 | 115,308 | 41,407 |
| Published concessions **claimed** (AER Q3 2021-22)              |   814,313 |   620,614 | 210,584 |  93,889 | 28,505 |

Derived unclaimed households (= eligible_households − claimed):
- NSW: 1,248,289 − 814,313 = 433,976 (matches 35% × 1,248,289 ≈ 436,901)
- QLD: 875,914 − 620,614 = 255,300 (≈ 29%)
- SA:  340,569 − 210,584 = 129,985 (≈ 38%)
- TAS: 115,308 − 93,889 = 21,419 (≈ 19%)
- ACT: 41,407 − 28,505 = 12,902 (≈ 31%)

### Victoria (Figure 4, p13)

| Utility | Eligible card holders | Eligible households | Published claimed |
|---|---|---|---|
| Electricity | 1,414,194 | 989,936 (×0.70) | 924,888 |
| Water       | 1,414,194 | 871,143 (×0.70×0.88) | 680,191 |
| Gas         | 1,414,194 | 752,351 (×0.70×0.76) | 658,831 |

The 0.88 secondary weighting = 88% of VIC concession card holders pay a water bill (DHHS 2015).
The 0.76 secondary weighting = 76% of VIC households have mains gas (Energy Networks Australia 2021).

## 3. Eligibility criteria (Figure 1, p8) — which cards count per state

|  | NSW | QLD | SA | TAS | ACT | VIC |
|---|---|---|---|---|---|---|
| Health Care Card (DSS) | ✓ | ✓ | ✓ | ✓ | ✓* | ✓ |
| Pension Concession Card (DSS) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Gold Veterans Concession Card (DVA) | ✓ | ✓ | ✓ |  | ✓ | ✓ |

*ACT has additional HCC eligibility criteria not modeled (data unavailable). TAS does not include DVA Gold.

CPRC adopted a **more limited eligibility criteria to reduce the incidence of overlaps between various concessions within a single household** (p8). "This approach produces a more conservative estimate of the total number of consumers eligible for an energy concession, and also results in a more conservative estimate of the gap between those eligible for and receiving their concession. Consequently, **the actual gap between eligible and claimed concessions may be greater.**"

## 4. Household dedup formula — Endnote 14, p20

> "We calculated our weighting using the formula `((100/(1+x*R))+((100/(1+x*R)*R)))/100` which is the estimated households per 100 with at least 1 concession, where 'x' = average number of concessions in multi-concession households (2) and 'R' = the ratio of multi-concession and single concession households (42/58 = 0.72)."

→ weight ≈ 0.70 (cards × 0.70 = households)

Source for the 42% figure: DHHS Victoria, *Victorian Utility Consumption Household Survey 2015*, p48 (Endnote 12). 42% in 2015, down from 49% in 2007.

CPRC self-acknowledged limitation (p9):
> "this weighting also assumes two concession cards per multi-concession card household, **though we recognise it is possible, even likely, that there may be three or more concession cards in a multi-concession card household.**"

→ direction: 0.70 may overestimate households (real households fewer) → final unclaimed AUD likely **underestimated** (conservative).

## 5. Conservative bias disclosure (multiple in-text quotes)

p8 (methodology section):
> "...the actual gap between eligible and claimed concessions may be greater."

p9 (assumption section): "we recognise it is possible, even likely, that there may be three or more concession cards"

p9 (retailer switching): "Our analysis has not taken into account the rate of switching between retailers... This may inflate the number of concessions claimed through separate retailer reporting." → cuts the other way (gap may be smaller in raw AER data)

## 6. Independent corroboration sources (Identifying the gap p7)

- **ACCC 2018 Retail Electricity Pricing Inquiry** — ~14% of eligible respondents did not receive an energy concession. "It is unclear how this figure was calculated."
- **NSW Energy Rebates Annual Report 2020-21** — 64% of eligible NSW consumers accessed the Low Income Household Rebate (= **36% did NOT access**); 56% accessed the Gas Rebate (= 44% did not). **This is directly relevant to our pilot benefit AU_NSW_LOW_INCOME_HOUSEHOLD_REBATE_RETAIL**: an independent NSW government source reports 36% unclaimed, virtually matching CPRC's 35% NECF estimate. Strong corroboration.
- **DHHS Victorian Utility Consumption Household Survey 2015** — 87% of eligible VIC concession card holders received electricity concession, 74% gas concession.

## 7. Data source citations (Endnotes p20-21)

- Endnote 8: NSW Department of Planning and Environment, *NSW Energy Rebates Annual Report 2020-21*, 2021, p4.
- Endnote 9: DHHS, *Victorian Utility Consumption Household Survey 2015*, Roy Morgan Research Ltd, Victoria 2016, p153. https://www.dffh.vic.gov.au/publications/victorian-utility-consumption-household-survey
- Endnote 10: DSS, *DSS Payment Demographic Data - Payment recipients by payment type and state and territory*, June 2022, https://data.gov.au/data/dataset/dss-payment-demographic-data ; DVA, Treatment Population Statistics - Table 2: treatment Population by State, Card and Aged Group, March 2022, https://www.dva.gov.au/about-us/overview/research/statistics-about-veteran-population
- Endnote 11: AER, *Retail Market performance*, Q3 2021-22, June 2022. https://www.aer.gov.au/retail-markets/performance-reporting
- Endnote 12: DHHS, *Victorian Utility Consumption Household Survey 2015*, p48 (the 42% figure)
- Endnote 13: AER, *Retail Market performance*, Q3 2021-22 (the published-claimed numbers in Figure 2)
- Endnote 14: The dedup formula (cited above in section 4)
