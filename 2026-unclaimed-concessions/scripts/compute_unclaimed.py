#!/usr/bin/env python3
"""
Taxlite Research — AU Unclaimed Welfare Estimator

Wave 1: NECF 5 states primary electricity concessions (all fixed yearly amount)
  - AU_NSW_LOW_INCOME_HOUSEHOLD_REBATE  (RETAIL variant, $285/yr)
  - AU_QLD_ELECTRICITY_REBATE                          ($386.34/yr)
  - AU_SA_ENERGY_BILL_CONCESSION                       ($281.78/yr)
  - AU_TAS_ANNUAL_ELECTRICITY_CONCESSION               ($645.56/yr)
  - AU_ACT_UTILITIES_CONCESSION                        ($800.00/yr)

Wave 2: VIC 3-utility cluster (percentage; uses imputed per-household amount)
  - AU_VIC_ANNUAL_ELECTRICITY_CONCESSION  (17.5% off → imputed $262.50/yr)
  - AU_VIC_WINTER_GAS_CONCESSION          (17.5% off winter → imputed $80/yr)
  - AU_VIC_WATER_SEWERAGE_CONCESSION      (50% off cap $372.10 → imputed $250/yr)

Usage:
    python3 report/scripts/compute_unclaimed.py --benefit <KEY>
    python3 report/scripts/compute_unclaimed.py --all              # run all benefits + emit aggregate CSV

Inputs:
    rules/<state>/energy.yaml                       ← amount.value
    report/data/cprc/cprc_state_rates.csv           ← state-level eligible_households + unclaimed_rate

Outputs:
    report/benefits/<BENEFIT_KEY>/working.json
    report/benefits/<BENEFIT_KEY>/unclaimed.csv
    report/aggregates/necf_electricity_v1.csv       ← in --all mode: 5-row aggregate + total

Sanity gate: if actual_aud falls outside manual_check range, exit 1 without writing CSV.

Methodological choice: use CPRC Mind the Gap Figure 2 (p11) pre-aggregated eligible_households count
(same source, same quarter, same dedup; 100% comparable to CPRC gap rate). See METHODOLOGY.md.
"""
import argparse
import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[2]


# ============================================================
# Benefit registry
# ============================================================

BENEFITS = {
    "AU_NSW_LOW_INCOME_HOUSEHOLD_REBATE": {
        "rule_id": "AU_NSW_LOW_INCOME_HOUSEHOLD_REBATE_RETAIL",
        "rule_yaml": "rules/nsw/energy.yaml",
        "cluster_id": "NSW Low Income Household Rebate",
        "jurisdiction": "NSW",
        "cprc_rate_row": {"jurisdiction": "NSW", "framework": "NECF"},
        "card_types_included": [
            "pensioner_concession_card",
            "health_care_card (incl. LIHCC)",
            "dva_gold_card (generic)",
        ],
        "manual_check": {
            "expected_aud_low":  115_000_000,
            "expected_aud_high": 135_000_000,
            "rationale": "1,248,289 NSW eligible households × 0.35 NECF gap × $285 ≈ $124.5M",
        },
        "corroboration_source": "NSW DPE, NSW Energy Rebates Annual Report 2020-21, p4: 36% Low Income Household Rebate not accessed (CPRC NECF estimate 35%, ≤1pp difference)",
        "variant_note": "RETAIL variant. ON_SUPPLY variant ($313.50) covers ~5% embedded-network households; including it would raise estimate <1%.",
    },
    "AU_QLD_ELECTRICITY_REBATE": {
        "rule_id": "AU_QLD_ELECTRICITY_REBATE",
        "rule_yaml": "rules/qld/energy.yaml",
        "cluster_id": "QLD Electricity Rebate",
        "jurisdiction": "QLD",
        "cprc_rate_row": {"jurisdiction": "QLD", "framework": "NECF"},
        "card_types_included": [
            "pensioner_concession_card",
            "health_care_card (incl. LIHCC)",
            "dva_gold_card (generic)",
        ],
        "manual_check": {
            "expected_aud_low":   90_000_000,
            "expected_aud_high": 108_000_000,
            "rationale": "875,914 QLD eligible households × 0.29 NECF gap × $386.34 ≈ $98.1M",
        },
        "corroboration_source": "No independent corroboration available — CPRC p7: \"could not identify any publicly available data about the size of the gap... in other states\"",
        "variant_note": "Single-rule cluster; YAML eligibility also accepts Seniors Card QLD (CPRC excludes; conservative direction preserved).",
    },
    "AU_SA_ENERGY_BILL_CONCESSION": {
        "rule_id": "AU_SA_ENERGY_BILL_CONCESSION",
        "rule_yaml": "rules/sa/energy.yaml",
        "cluster_id": "SA Energy Bill Concession",
        "jurisdiction": "SA",
        "cprc_rate_row": {"jurisdiction": "SA", "framework": "NECF"},
        "card_types_included": [
            "pensioner_concession_card",
            "health_care_card (incl. LIHCC)",
            "dva_gold_card (generic)",
        ],
        "manual_check": {
            "expected_aud_low": 33_000_000,
            "expected_aud_high": 40_000_000,
            "rationale": "340,569 SA eligible households × 0.38 NECF gap × $281.78 ≈ $36.5M",
        },
        "corroboration_source": "No independent corroboration available",
        "variant_note": "Single-rule cluster; YAML eligibility also accepts CSHC (CPRC excludes; conservative direction preserved).",
    },
    "AU_TAS_ANNUAL_ELECTRICITY_CONCESSION": {
        "rule_id": "AU_TAS_ANNUAL_ELECTRICITY_CONCESSION",
        "rule_yaml": "rules/tas/energy.yaml",
        "cluster_id": "TAS Annual Electricity Concession",
        "jurisdiction": "TAS",
        "cprc_rate_row": {"jurisdiction": "TAS", "framework": "NECF"},
        "card_types_included": [
            "pensioner_concession_card",
            "health_care_card (incl. LIHCC)",
        ],
        "manual_check": {
            "expected_aud_low": 12_700_000,
            "expected_aud_high": 15_500_000,
            "rationale": "115,308 TAS eligible households × 0.19 NECF gap × $645.56 ≈ $14.1M",
        },
        "corroboration_source": "No independent corroboration available",
        "variant_note": "Single-rule cluster. TAS does not accept DVA Gold per CPRC Fig 1 (already reflected in 115,308 households count).",
    },
    "AU_ACT_UTILITIES_CONCESSION": {
        "rule_id": "AU_ACT_UTILITIES_CONCESSION",
        "rule_yaml": "rules/act/energy.yaml",
        "cluster_id": "ACT Utilities Concession",
        "jurisdiction": "ACT",
        "cprc_rate_row": {"jurisdiction": "ACT", "framework": "NECF"},
        "card_types_included": [
            "pensioner_concession_card",
            "health_care_card (incl. LIHCC)",
            "dva_gold_card (generic)",
        ],
        "manual_check": {
            "expected_aud_low":  9_000_000,
            "expected_aud_high": 11_500_000,
            "rationale": "41,407 ACT eligible households × 0.31 NECF gap × $800 ≈ $10.3M",
        },
        "corroboration_source": "No independent corroboration available — CPRC Fig 1 notes additional ACT HCC eligibility criteria not modelled (data unavailable)",
        "variant_note": "Single-rule cluster covering electricity + gas + water bundled into one ACT concession.",
    },
    # ── Wave 2: Victoria 3-utility cluster (percentage; imputed per-household AUD) ──
    "AU_VIC_ANNUAL_ELECTRICITY_CONCESSION": {
        "rule_id": "AU_VIC_ANNUAL_ELECTRICITY_CONCESSION",
        "rule_yaml": "rules/vic/energy.yaml",
        "cluster_id": "VIC Electricity Concession",
        "jurisdiction": "VIC",
        "cprc_rate_row": {"jurisdiction": "VIC", "framework": "Victoria_DFFH", "utility": "electricity"},
        "card_types_included": [
            "pensioner_concession_card",
            "health_care_card",
            "dva_gold_card (generic)",
        ],
        "amount_imputed_aud": 262.50,
        "amount_basis": "17.5% × $1,500 typical VIC concession-household annual electricity bill (per CPRC-cited retailer AER reporting; conservative vs $2,000 unrestricted-population benchmark)",
        "manual_check": {
            "expected_aud_low":  16_000_000,
            "expected_aud_high": 20_500_000,
            "rationale": "989,936 VIC eligible households × 0.07 gap × $262.50 imputed ≈ $18.2M",
        },
        "corroboration_source": "Same-source self-corroboration only — CPRC notes 'NECF and VIC may not be comparable' (p9). DHHS 2015 survey 87% receive-rate ≈ 13% gap aligns to within 6pp.",
        "variant_note": "Percentage rule (17.5% off bills, first $171.60 excluded). Pilot uses imputed AUD; cluster also contains Controlled Load (13%), Excess Electricity (formula), Medical Cooling (17.5%) variants not included in pilot.",
    },
    "AU_VIC_WINTER_GAS_CONCESSION": {
        "rule_id": "AU_VIC_WINTER_GAS_CONCESSION",
        "rule_yaml": "rules/vic/energy.yaml",
        "cluster_id": "VIC Gas Concession",
        "jurisdiction": "VIC",
        "cprc_rate_row": {"jurisdiction": "VIC", "framework": "Victoria_DFFH", "utility": "gas"},
        "card_types_included": [
            "pensioner_concession_card",
            "health_care_card",
            "dva_gold_card (generic)",
        ],
        "amount_imputed_aud": 80.00,
        "amount_basis": "17.5% × typical winter (May–Oct) VIC concession-household gas bill, annualised — winter ≈ 50% of annual gas usage; CPRC retailer reporting basis",
        "manual_check": {
            "expected_aud_low":  6_500_000,
            "expected_aud_high":  8_500_000,
            "rationale": "752,351 VIC eligible households × 0.12 gap × $80 imputed ≈ $7.2M",
        },
        "corroboration_source": "Same-source self-corroboration only — DHHS 2015 survey reported 74% gas concession receive-rate (= 26% gap), notably higher than CPRC's 12% — methodology divergence acknowledged by CPRC.",
        "variant_note": "Percentage rule, winter only (1 May – 31 Oct). 752,351 households reflects CPRC's 0.76 secondary weighting (76% mains-gas connection rate, ENA 2021). Cluster also contains Excess Gas (formula) variant.",
    },
    "AU_VIC_WATER_SEWERAGE_CONCESSION": {
        "rule_id": "AU_VIC_WATER_SEWERAGE_CONCESSION",
        "rule_yaml": "rules/vic/card_linked.yaml",
        "cluster_id": "VIC Water Concession",
        "jurisdiction": "VIC",
        "cprc_rate_row": {"jurisdiction": "VIC", "framework": "Victoria_DFFH", "utility": "water"},
        "card_types_included": [
            "pensioner_concession_card",
            "dva_gold_card (generic)",
            "health_care_card (note: per actual DFFH rule HCC is INELIGIBLE for water — but CPRC denominator includes HCC; see disclosure)",
        ],
        "amount_imputed_aud": 250.00,
        "amount_basis": "Bill-capped at $372.10/yr (2025-26 DFFH official); imputed $250 assumes typical water bills reach ~67% of cap before hitting it (conservative). Cap-only scenarios would imply $372.10.",
        "manual_check": {
            "expected_aud_low": 42_000_000,
            "expected_aud_high": 54_000_000,
            "rationale": "871,143 VIC eligible households × 0.22 gap × $250 imputed ≈ $47.9M",
        },
        "corroboration_source": "Same-source self-corroboration only — DHHS 2015 survey reported 78% water concession receive-rate (= 22% gap, identical to CPRC).",
        "variant_note": "Percentage rule (50% off bill, capped). CPRC water denominator (871,143 households) includes HCC holders, but actual DFFH rule excludes HCC — see METHODOLOGY §6 'VIC water HCC discrepancy'. This direction inflates the estimate; the true unclaimed AUD is lower than this row implies.",
    },
    # ── Wave 2.5: Formula rule pilot — methodology_pilot_only, NOT in headline aggregate ──
    # Per METHODOLOGY §7.2 hard rule: Tier-2 / Tier-3 estimates go to formula_pilot_v*.csv,
    # marked "indicative only", never to headline_state_concessions.csv.
    "AU_VIC_EXCESS_ELECTRICITY_CONCESSION": {
        "rule_id": "AU_VIC_EXCESS_ELECTRICITY_CONCESSION",
        "rule_yaml": "rules/vic/energy.yaml",
        "cluster_id": "VIC Electricity Concession (Excess)",
        "jurisdiction": "VIC",
        "cprc_rate_row": {"jurisdiction": "VIC", "framework": "Victoria_DFFH", "utility": "electricity"},
        "card_types_included": [
            "pensioner_concession_card",
            "health_care_card",
            "dva_gold_card (generic)",
        ],
        "amount_imputed_aud": 1038.12,
        "amount_basis": "Tier-2 (official worked example, NOT avg). DFFH formula: A = [17.5% × (B − C)] − (D × 0.0823) per month. Official example: B=$560, C=$24.25, D=88 → A=$86.51/month = $1,038.12/yr per recipient. See METHODOLOGY §7.3.",
        "trigger_rate": 0.05,
        "trigger_rate_basis": "Imputed 5% of VIC eligible households trigger Excess (annual electricity bill ≥ $3,895.13). VIC concession-household typical bill ≈ $1,500 (CPRC retailer data); $3,895 ≈ 95-98th percentile. Conservative imputation, no official source for this share.",
        "manual_check": {
            "expected_aud_low":  2_700_000,
            "expected_aud_high": 4_500_000,
            "rationale": "989,936 × 5% trigger × 7% gap × $1,038 ≈ $3.6M (double-imputed, methodology pilot only)",
        },
        "corroboration_source": "No direct corroboration — Tier-2 official example × imputed trigger rate. CPRC report notes Excess as separate VIC concession (p12) but does not separately report its take-up gap.",
        "variant_note": "Formula rule. Double-imputation (amount Tier-2 + trigger rate imputed). Conflicts with Annual Electricity Concession per YAML — same household can't legitimately receive both since Excess replaces Annual when bill exceeds threshold. If Annual already counts this cohort, adding Excess to headline would double-count.",
        # ↓ Tier-2/3 flag: keep out of headline aggregate per §7.2 hard rule.
        "methodology_pilot_only": True,
    },
}


# ============================================================
# Loaders
# ============================================================

def load_rule(yaml_path: Path, rule_id: str) -> dict:
    with yaml_path.open(encoding="utf-8") as f:
        doc = yaml.safe_load(f)
    for rule in doc.get("rules", []):
        if rule.get("id") == rule_id:
            return rule
    raise SystemExit(f"[FATAL] rule {rule_id!r} not found in {yaml_path}")


def load_cprc_rate(csv_path: Path, jurisdiction: str, framework: str, utility: str | None = None) -> dict:
    with csv_path.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            if row["jurisdiction"] != jurisdiction or row["framework"] != framework:
                continue
            if utility is not None and row["utility"] != utility:
                continue
            return row
    raise SystemExit(f"[FATAL] CPRC row jurisdiction={jurisdiction} framework={framework} utility={utility} not found in {csv_path}")


# ============================================================
# Compute
# ============================================================

def compute(benefit_key: str) -> dict:
    cfg = BENEFITS[benefit_key]
    rule = load_rule(REPO_ROOT / cfg["rule_yaml"], cfg["rule_id"])

    amount = rule["amount"]

    # Amount selection: prefer fixed YAML; non-fixed requires BENEFITS-configured imputed value
    if amount["type"] == "fixed" and amount["period"] == "yearly":
        amount_per_year = float(amount["value"])
        amount_type_label = "fixed_yearly"
        amount_basis = f"YAML {cfg['rule_yaml']} → {cfg['rule_id']}.amount.value (fixed yearly)"
    elif amount["type"] in ("percentage", "formula"):
        if "amount_imputed_aud" not in cfg:
            raise SystemExit(f"[FATAL] {benefit_key}: rule amount.type={amount['type']!r} but BENEFITS has no amount_imputed_aud configured")
        amount_per_year = float(cfg["amount_imputed_aud"])
        amount_type_label = f"{amount['type']}_imputed"
        amount_basis = cfg["amount_basis"]
    else:
        raise SystemExit(f"[FATAL] {benefit_key}: unsupported amount.type={amount['type']!r} / period={amount['period']!r}")

    cprc_row = load_cprc_rate(
        REPO_ROOT / "report/data/cprc/cprc_state_rates.csv",
        cfg["cprc_rate_row"]["jurisdiction"],
        cfg["cprc_rate_row"]["framework"],
        cfg["cprc_rate_row"].get("utility"),
    )
    eligible_cards = int(cprc_row["eligible_cards"])
    eligible_households = int(cprc_row["eligible_households"])
    unclaimed_rate = float(cprc_row["unclaimed_rate"])
    cprc_quarter = cprc_row["quarter"]
    cprc_page = int(cprc_row["page"])
    cprc_utility = cprc_row["utility"]

    dedup_factor = round(eligible_households / eligible_cards, 4)

    # Trigger rate: optional formula-rule filter (e.g., bill > threshold). Default 1.0 = full cohort.
    trigger_rate = float(cfg.get("trigger_rate", 1.0))
    trigger_rate_basis = cfg.get("trigger_rate_basis", "n/a (full eligible cohort)")
    effective_eligible_households = int(round(eligible_households * trigger_rate))
    unclaimed_households = int(round(effective_eligible_households * unclaimed_rate))
    unclaimed_total_aud = int(round(unclaimed_households * amount_per_year))

    cprc_framework = cfg["cprc_rate_row"]["framework"]
    cprc_fig = "Figure 3, p11" if cprc_framework == "NECF" else "Figure 5, p13"

    return {
        "rule_id": cfg["rule_id"],
        "cluster_id": cfg["cluster_id"],
        "jurisdiction": cfg["jurisdiction"],
        "utility": cprc_utility,
        "computed_at": datetime.now(timezone.utc).isoformat(),
        "inputs": {
            "amount_per_year_aud": amount_per_year,
            "amount_type_label": amount_type_label,
            "amount_source": amount_basis,
            "eligible_cards": eligible_cards,
            "eligible_households": eligible_households,
            "dedup_factor": dedup_factor,
            "dedup_factor_source": "CPRC Mind the Gap endnote 14, p20 — ((100/(1+x*R))+((100/(1+x*R)*R)))/100, x=2, R=42/58=0.72",
            "unclaimed_rate": unclaimed_rate,
            "unclaimed_rate_source": f"CPRC Mind the Gap {cprc_fig}, {cprc_framework} {cprc_quarter}",
            "cprc_data_quarter": cprc_quarter,
            "cprc_framework": cprc_framework,
            "card_types_included": cfg["card_types_included"],
        },
        "steps": [
            {"step": 1, "name": "eligible_cards", "value": eligible_cards,
             "source": "CPRC Fig 2 p11 (DSS June 2022 + DVA March 2022)"},
            {"step": 2, "name": "eligible_households", "value": eligible_households,
             "formula": f"eligible_cards × {dedup_factor} (CPRC weighting)",
             "verify": eligible_cards * 0.70},
            {"step": "2b", "name": "effective_eligible_households", "value": effective_eligible_households,
             "formula": f"eligible_households × trigger_rate {trigger_rate}",
             "trigger_rate_basis": trigger_rate_basis},
            {"step": 3, "name": "unclaimed_households", "value": unclaimed_households,
             "formula": f"effective_eligible_households × {unclaimed_rate}"},
            {"step": 4, "name": "unclaimed_total_aud", "value": unclaimed_total_aud,
             "formula": f"unclaimed_households × ${amount_per_year}"},
        ],
        "manual_check": {
            **cfg["manual_check"],
            "actual_aud": unclaimed_total_aud,
            "within_range": (
                cfg["manual_check"]["expected_aud_low"]
                <= unclaimed_total_aud
                <= cfg["manual_check"]["expected_aud_high"]
            ),
        },
        "sources": {
            "cprc_citation": "Consumer Policy Research Centre (CPRC), Mind the Gap — Identifying the gap between energy concession eligibility and concessions received, November 2022. Author: Ben Martin Hobbs.",
            "cprc_landing":   "https://cprc.org.au/report/mind-the-gap/",
            "cprc_pdf":       "https://cprc.org.au/wp-content/uploads/2022/11/Mind-the-Gap_Report_Update-1011.pdf",
            "cprc_local_pdf": "report/data/cprc/mind-the-gap-2022.pdf",
            "dss_data_quarter": "DSS Payment Demographic Data, June 2022 (per CPRC endnote 10) + DVA Treatment Population, March 2022",
            "dss_data_url":     "https://data.gov.au/data/dataset/dss-payment-demographic-data",
            "rule_yaml_path":   cfg["rule_yaml"],
            "corroboration_source": cfg["corroboration_source"],
        },
        "disclosures": [
            "Pilot uses CPRC's already-aggregated eligible household count, not a separate DSS pull, for 100% same-quarter same-source comparability with the gap rate.",
            cfg["variant_note"],
            "0.70 dedup weighting assumes x=2 (cards per multi-card household); CPRC acknowledges 'possible, even likely, that there may be three or more' → 0.70 may overestimate households → final AUD likely underestimated (conservative).",
            "CPRC adopted limited eligibility criteria to avoid household-level double counting → 'actual gap... may be greater' (CPRC p8).",
            "EBRF (federal Energy Bill Relief Fund) does NOT substitute for state-level concessions. State LIHR's 35% unclaimed rate is structural take-up gap, independent of EBRF.",
        ],
    }


# ============================================================
# CSV writer
# ============================================================

CSV_COLUMNS = [
    "cluster_id",
    "rule_id",
    "jurisdiction",
    "utility",
    "cprc_framework",
    "amount_type",
    "amount_per_year_aud",
    "amount_basis",
    "card_types_included",
    "eligible_cards_total",
    "dedup_factor",
    "eligible_households",
    "unclaimed_rate",
    "unclaimed_rate_source",
    "cprc_data_quarter",
    "unclaimed_households",
    "unclaimed_total_aud",
    "dss_data_quarter",
    "dss_data_url",
    "corroboration_source",
    "cprc_citation",
]


def working_to_row(working: dict) -> dict:
    inp = working["inputs"]
    src = working["sources"]
    return {
        "cluster_id": working["cluster_id"],
        "rule_id": working["rule_id"],
        "jurisdiction": working["jurisdiction"],
        "utility": working.get("utility", "electricity"),
        "cprc_framework": inp.get("cprc_framework", "NECF"),
        "amount_type": inp["amount_type_label"],
        "amount_per_year_aud": inp["amount_per_year_aud"],
        "amount_basis": inp["amount_source"],
        "card_types_included": "|".join(inp["card_types_included"]),
        "eligible_cards_total": inp["eligible_cards"],
        "dedup_factor": inp["dedup_factor"],
        "eligible_households": inp["eligible_households"],
        "unclaimed_rate": inp["unclaimed_rate"],
        "unclaimed_rate_source": inp["unclaimed_rate_source"],
        "cprc_data_quarter": inp["cprc_data_quarter"],
        "unclaimed_households": next(s["value"] for s in working["steps"] if s["name"] == "unclaimed_households"),
        "unclaimed_total_aud": next(s["value"] for s in working["steps"] if s["name"] == "unclaimed_total_aud"),
        "dss_data_quarter": src["dss_data_quarter"],
        "dss_data_url": src["dss_data_url"],
        "corroboration_source": src["corroboration_source"],
        "cprc_citation": src["cprc_citation"],
    }


def write_single_csv(csv_path: Path, working: dict) -> None:
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerow(working_to_row(working))


def write_aggregate_csv(csv_path: Path, all_working: list[dict], total_label: str) -> None:
    """Aggregate CSV. TOTAL row leaves amount/gap/rate blank — weighted averages are not physically meaningful; only count columns are summed."""
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    rows = [working_to_row(w) for w in all_working]
    # VIC utility rows (electricity/gas/water) serve the same household cohort — count sums would triple-count VIC households.
    # Only sum counts for geographically disjoint cohorts: NECF 5 states do not overlap; VIC uses the largest cohort (electricity 989,936) as
    # the upper bound on unique VIC eligible households (excludes cross-utility duplication). AUD is non-overlapping across streams, so direct sum is correct.
    necf_rows = [r for r in rows if r["cprc_framework"] == "NECF"]
    vic_rows = [r for r in rows if r["cprc_framework"] == "Victoria_DFFH"]
    vic_unique_cards = max([r["eligible_cards_total"] for r in vic_rows], default=0)
    vic_unique_hh_eligible = max([r["eligible_households"] for r in vic_rows], default=0)  # electricity has full 0.70 weighting
    necf_cards = sum(r["eligible_cards_total"] for r in necf_rows)
    necf_hh = sum(r["eligible_households"] for r in necf_rows)
    rows.append({
        "cluster_id": total_label,
        "rule_id": "",
        "jurisdiction": "TOTAL",
        "utility": "",
        "cprc_framework": "",
        "amount_type": "",                       # blank — mix of fixed_yearly + percentage_imputed, weighted avg meaningless
        "amount_per_year_aud": "",               # blank — weighted average is misleading
        "amount_basis": "see per-row",
        "card_types_included": "",
        "eligible_cards_total": necf_cards + vic_unique_cards,
        "dedup_factor": 0.70,
        "eligible_households": necf_hh + vic_unique_hh_eligible,
        "unclaimed_rate": "",                    # blank — weighted gap rate not physically meaningful
        "unclaimed_rate_source": f"NECF 5 states geographically disjoint; VIC counted once (electricity cohort = {vic_unique_hh_eligible:,d} households shared across all 3 utility rebates). 'unclaimed_households' sum is upper bound — households missing multiple VIC utilities are double-counted across VIC rows.",
        "cprc_data_quarter": "2021-22 Q3",
        "unclaimed_households": sum(r["unclaimed_households"] for r in rows),  # upper bound: VIC households double-counted across utilities
        "unclaimed_total_aud": sum(r["unclaimed_total_aud"] for r in rows),    # true total: different concession streams do not overlap
        "dss_data_quarter": "see per-row",
        "dss_data_url": "https://data.gov.au/data/dataset/dss-payment-demographic-data",
        "corroboration_source": "NSW DPE 36% (LIHR specific); others have no independent state-level corroboration",
        "cprc_citation": "Consumer Policy Research Centre (CPRC), Mind the Gap, November 2022, Ben Martin Hobbs.",
    })
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


# ============================================================
# Driver
# ============================================================

def run_one(benefit_key: str) -> dict:
    out_dir = REPO_ROOT / "report" / "benefits" / benefit_key
    out_dir.mkdir(parents=True, exist_ok=True)

    working = compute(benefit_key)
    working_path = out_dir / "working.json"
    with working_path.open("w", encoding="utf-8") as f:
        json.dump(working, f, ensure_ascii=False, indent=2)

    mc = working["manual_check"]
    print(f"[{benefit_key}]")
    print(f"  expected: ${mc['expected_aud_low']:>13,d} – ${mc['expected_aud_high']:>13,d}")
    print(f"  actual:   ${mc['actual_aud']:>13,d}  (within_range={mc['within_range']})")

    if not mc["within_range"]:
        print(f"[FAIL] {benefit_key} actual_aud outside sanity gate. CSV NOT written.", file=sys.stderr)
        sys.exit(1)

    write_single_csv(out_dir / "unclaimed.csv", working)
    return working


def main():
    parser = argparse.ArgumentParser()
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--benefit", choices=list(BENEFITS))
    g.add_argument("--all", action="store_true")
    args = parser.parse_args()

    if args.all:
        all_working = [run_one(k) for k in BENEFITS]

        # ── Split rows by tier per METHODOLOGY §7.2 ──
        # Headline aggregate: Tier-1 only (fixed_yearly + percentage_imputed with retailer-data-backed amount).
        # Formula pilot aggregate: Tier-2/Tier-3 (methodology_pilot_only=True). Marked "indicative only".
        headline_rows = []
        formula_pilot_rows = []
        for k, w in zip(BENEFITS.keys(), all_working):
            if BENEFITS[k].get("methodology_pilot_only"):
                formula_pilot_rows.append(w)
            else:
                headline_rows.append(w)

        headline_path = REPO_ROOT / "report/aggregates/headline_state_concessions.csv"
        write_aggregate_csv(
            headline_path,
            headline_rows,
            total_label="TOTAL (NECF 5 electricity + VIC 3-utility cluster) — headline",
        )
        headline_total = sum(
            next(s["value"] for s in w["steps"] if s["name"] == "unclaimed_total_aud")
            for w in headline_rows
        )
        print()
        print(f"[OK] headline aggregate → {headline_path.relative_to(REPO_ROOT)}")
        print(f"[OK] HEADLINE state-concession unclaimed total: ${headline_total:,d}/yr (${headline_total/1e6:.1f}M/yr)")

        if formula_pilot_rows:
            pilot_path = REPO_ROOT / "report/aggregates/formula_pilot_v1.csv"
            write_aggregate_csv(
                pilot_path,
                formula_pilot_rows,
                total_label="TOTAL (formula-pilot, INDICATIVE ONLY — NOT INCLUDED IN HEADLINE)",
            )
            pilot_total = sum(
                next(s["value"] for s in w["steps"] if s["name"] == "unclaimed_total_aud")
                for w in formula_pilot_rows
            )
            print(f"[OK] formula pilot   → {pilot_path.relative_to(REPO_ROOT)}")
            print(f"     (indicative only, not in headline): ${pilot_total:,d}/yr (${pilot_total/1e6:.1f}M/yr)")
    else:
        run_one(args.benefit)


if __name__ == "__main__":
    main()
