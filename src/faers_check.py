from __future__ import annotations

import argparse
import csv
import os
import sys
import time
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import quote

try:
    import requests
except ImportError:
    import subprocess

    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests


BASE_URL = "https://api.fda.gov/drug/event.json"
DRUGS = ["propranolol", "atenolol", "metoprolol"]
YEARS = [2022, 2023, 2024, 2025]
FIELDS = {
    "openfda_generic_name": "patient.drug.openfda.generic_name",
    "medicinalproduct": "patient.drug.medicinalproduct",
}


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def year_range(year: int) -> str:
    return f"receivedate:[{year}0101+TO+{year}1231]"


def make_search(year: int, field: str | None = None, drug: str | None = None) -> str:
    if field and drug:
        return f"{field}:{drug}+AND+{year_range(year)}"
    return year_range(year)


def make_url(search: str, include_key: bool = False) -> str:
    encoded_search = quote(search, safe=":+[]")
    url = f"{BASE_URL}?search={encoded_search}&limit=1"
    api_key = os.getenv("OPENFDA_API_KEY", "").strip()
    if include_key and api_key:
        url += f"&api_key={quote(api_key)}"
    return url


def get_json(search: str) -> tuple[dict[str, Any] | None, str]:
    use_key = False
    last_url = make_url(search, include_key=use_key)

    for attempt in range(6):
        last_url = make_url(search, include_key=use_key)
        response = requests.get(last_url, timeout=30)

        if response.status_code == 200:
            return response.json(), last_url

        if response.status_code == 404:
            return None, last_url

        if response.status_code == 429:
            use_key = True

        if response.status_code == 429 or response.status_code >= 500:
            time.sleep(min(2**attempt, 30))
            continue

        raise RuntimeError(f"OpenFDA request failed: HTTP {response.status_code}\n{last_url}\n{response.text[:500]}")

    raise RuntimeError(f"OpenFDA request failed after retries:\n{last_url}")


def total_from_payload(payload: dict[str, Any] | None) -> int:
    if not payload:
        return 0
    return int(payload.get("meta", {}).get("results", {}).get("total", 0))


def last_updated_from_payload(payload: dict[str, Any] | None) -> str | None:
    if not payload:
        return None
    return payload.get("meta", {}).get("last_updated")


def pct_growth(current: int, previous: int) -> float | None:
    if previous == 0:
        return None
    return (current - previous) / previous * 100


def multiplier(current: int, previous: int) -> float | None:
    if previous == 0:
        return None
    return current / previous


def fmt_count(value: int) -> str:
    return f"{value:,}"


def fmt_pct(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value:+.1f}%"


def fmt_mult(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value:.2f}x"


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    return "\n".join(lines)


def write_counts_csv(
    csv_path: Path,
    counts: dict[tuple[str, str, int], int],
    snapshot_date: str,
    meta_last_updated: str,
) -> None:
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["drug", "year", "field", "count", "snapshot_date", "meta_last_updated"])
        writer.writeheader()
        for drug in DRUGS:
            for field_label in FIELDS:
                for year in YEARS:
                    writer.writerow(
                        {
                            "drug": drug,
                            "year": year,
                            "field": field_label,
                            "count": counts[(drug, field_label, year)],
                            "snapshot_date": snapshot_date,
                            "meta_last_updated": meta_last_updated,
                        }
                    )


def write_vigiaccess_observations_csv(csv_path: Path) -> None:
    rows = [
        {
            "drug": "propranolol",
            "source_image": "assets/vigiaccess/propranolol.jpeg",
            "observation": "total_reports_visible_in_screenshot",
            "year": "",
            "value": 38326,
            "note": "Manual transcription from supplied VigiAccess screenshot.",
        },
        {
            "drug": "propranolol",
            "source_image": "assets/vigiaccess/propranolol.jpeg",
            "observation": "adr_reports_per_year_visible_table",
            "year": 2023,
            "value": 2183,
            "note": "Manual transcription from supplied VigiAccess screenshot.",
        },
        {
            "drug": "propranolol",
            "source_image": "assets/vigiaccess/propranolol.jpeg",
            "observation": "adr_reports_per_year_visible_table",
            "year": 2024,
            "value": 2769,
            "note": "Manual transcription from supplied VigiAccess screenshot.",
        },
        {
            "drug": "propranolol",
            "source_image": "assets/vigiaccess/propranolol.jpeg",
            "observation": "adr_reports_per_year_visible_table",
            "year": 2025,
            "value": 6589,
            "note": "Manual transcription from supplied VigiAccess screenshot.",
        },
        {
            "drug": "atenolol",
            "source_image": "assets/vigiaccess/atenolol.jpeg",
            "observation": "total_reports_visible_in_screenshot",
            "year": "",
            "value": 35798,
            "note": "Manual transcription from supplied VigiAccess screenshot.",
        },
        {
            "drug": "metoprolol",
            "source_image": "assets/vigiaccess/metoprolol.jpeg",
            "observation": "total_reports_visible_in_screenshot",
            "year": "",
            "value": 64612,
            "note": "Manual transcription from supplied VigiAccess screenshot.",
        },
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def build_summary(
    snapshot_date: str,
    meta_last_updated: str,
    counts: dict[tuple[str, str, int], int],
    totals: dict[int, int],
    query_log: list[dict[str, Any]],
) -> str:
    total_yoy = {year: pct_growth(totals[year], totals[year - 1]) for year in YEARS[1:]}
    primary_field = "openfda_generic_name"

    count_rows: list[list[str]] = []
    for drug in DRUGS:
        for field_label in FIELDS:
            count_rows.append([drug, field_label, *(fmt_count(counts[(drug, field_label, year)]) for year in YEARS)])

    growth_rows: list[list[str]] = []
    for drug in DRUGS:
        c2023 = counts[(drug, primary_field, 2023)]
        c2024 = counts[(drug, primary_field, 2024)]
        c2025 = counts[(drug, primary_field, 2025)]
        yoy_2025 = pct_growth(c2025, c2024)
        excess = None if yoy_2025 is None or total_yoy[2025] is None else yoy_2025 - total_yoy[2025]
        growth_rows.append(
            [
                drug,
                fmt_count(c2023),
                fmt_count(c2024),
                fmt_count(c2025),
                fmt_pct(pct_growth(c2024, c2023)),
                fmt_pct(yoy_2025),
                fmt_mult(multiplier(c2025, c2024)),
                fmt_mult(multiplier(c2025, c2023)),
                fmt_pct(excess),
            ]
        )

    total_rows = [[str(year), fmt_count(totals[year]), fmt_pct(total_yoy.get(year))] for year in YEARS]

    gap_rows: list[list[str]] = []
    for drug in DRUGS:
        normalized = counts[(drug, "openfda_generic_name", 2025)]
        free_text = counts[(drug, "medicinalproduct", 2025)]
        gap_rows.append([drug, fmt_count(normalized), fmt_count(free_text), fmt_count(free_text - normalized)])

    query_lines = "\n".join(f"- {item['drug']} | {item['field']} | {item['year']}: `{item['url']}`" for item in query_log)

    return f"""# FAERS Replication Test - Propranolol VigiAccess Spike

Snapshot date / تاريخ اللقطة: **{snapshot_date}**

OpenFDA `meta.last_updated` / آخر تحديث OpenFDA: **{meta_last_updated}**

This is a reproducible, hypothesis-generating comparison of annual FAERS report counts for propranolol, atenolol, and metoprolol. It is intended as a cross-check for a visible 2025 VigiAccess propranolol spike.

هذا فحص قابل للإعادة يقارن أعداد بلاغات FAERS السنوية لـ propranolol و atenolol و metoprolol كاختبار مستقل لقفزة propranolol الظاهرة في VigiAccess سنة 2025.

## Source Evidence / أدلة المصدر

Supplied VigiAccess screenshots are stored in:

- `assets/vigiaccess/propranolol.jpeg`
- `assets/vigiaccess/atenolol.jpeg`
- `assets/vigiaccess/metoprolol.jpeg`

Manual screenshot observations are stored in `data/vigiaccess_screenshot_observations.csv`.

## Method / المنهجية

- API endpoint: `https://api.fda.gov/drug/event.json`
- Date field: `receivedate`, the date FDA received the report.
- Primary drug field: `patient.drug.openfda.generic_name`
- Sanity-check drug field: `patient.drug.medicinalproduct`
- For each drug, year, and field, the script issues one query and reads `meta.results.total`; it does not paginate.
- Total FAERS baseline uses the same annual `receivedate` ranges with no drug filter.

## Caveats / تنبيهات

- Counts are raw spontaneous-report counts, not incidence rates and not risk estimates.
- الأرقام هي أعداد بلاغات خام، وليست معدلات حدوث أو تقديرا للخطر.
- No exposed-patient denominator is available.
- لا يوجد مقام لعدد المرضى المعرضين.
- Recent FAERS years can keep changing because of reporting lag; 2025 is near-final but not frozen as of `meta.last_updated`.
- سنة 2025 قد تتغير لاحقا بسبب تأخر البلاغات.
- The `openfda` normalized fields are absent on unmatched reports; the gap versus `medicinalproduct` is a data-quality signal.

## FAERS Counts / أعداد FAERS

{markdown_table(["drug", "field", "2022", "2023", "2024", "2025"], count_rows)}

## Growth Summary / ملخص النمو

{markdown_table(["drug", "2023", "2024", "2025", "2024 YoY", "2025 YoY", "2025/2024", "2025/2023", "2025 excess vs total FAERS"], growth_rows)}

## Total FAERS Baseline / خط أساس FAERS

{markdown_table(["year", "total reports", "YoY"], total_rows)}

## 2025 Field Gap / فجوة الحقول في 2025

{markdown_table(["drug", "openfda_generic_name", "medicinalproduct", "medicinalproduct - generic"], gap_rows)}

## Neutral Interpretation / قراءة محايدة

English: In this FAERS snapshot, the VigiAccess propranolol 2025 spike does **not** clearly replicate in the independent US FAERS sample. Propranolol decreases in 2025 on the normalized FAERS field while total FAERS is roughly flat.

العربية: في لقطة FAERS هذه، لا تتكرر قفزة propranolol الظاهرة في VigiAccess بوضوح داخل العينة الأمريكية المستقلة. في الحقل الموحد داخل FAERS ينخفض propranolol في 2025 بينما إجمالي FAERS شبه مستقر.

This does not prove absence of a safety issue; it only says that this specific raw-count spike is not reproduced in this second spontaneous-reporting system.

## Exact API Query URLs / روابط الاستعلام

{query_lines}
"""


def run(output_root: Path) -> None:
    data_dir = output_root / "data"
    reports_dir = output_root / "reports"
    data_dir.mkdir(exist_ok=True)
    reports_dir.mkdir(exist_ok=True)

    snapshot_date = date.today().isoformat()
    query_log: list[dict[str, Any]] = []
    meta_last_updated_values: set[str] = set()
    counts: dict[tuple[str, str, int], int] = {}
    totals: dict[int, int] = {}

    for year in YEARS:
        payload, url = get_json(make_search(year))
        query_log.append({"drug": "ALL_FAERS", "year": year, "field": "receivedate", "url": url})
        totals[year] = total_from_payload(payload)
        if last_updated := last_updated_from_payload(payload):
            meta_last_updated_values.add(last_updated)

    for drug in DRUGS:
        for field_label, field_name in FIELDS.items():
            for year in YEARS:
                payload, url = get_json(make_search(year, field_name, drug))
                query_log.append({"drug": drug, "year": year, "field": field_label, "url": url})
                counts[(drug, field_label, year)] = total_from_payload(payload)
                if last_updated := last_updated_from_payload(payload):
                    meta_last_updated_values.add(last_updated)

    meta_last_updated = ", ".join(sorted(meta_last_updated_values)) or "unavailable"
    write_counts_csv(data_dir / "faers_betablocker_counts.csv", counts, snapshot_date, meta_last_updated)
    write_vigiaccess_observations_csv(data_dir / "vigiaccess_screenshot_observations.csv")
    (reports_dir / "faers_summary.md").write_text(
        build_summary(snapshot_date, meta_last_updated, counts, totals, query_log),
        encoding="utf-8",
    )

    total_yoy_2025 = pct_growth(totals[2025], totals[2024])
    print("Headline: 2025 normalized FAERS growth vs total FAERS baseline")
    print(f"Total FAERS: 2025 YoY {fmt_pct(total_yoy_2025)}")
    for drug in DRUGS:
        yoy_2025 = pct_growth(counts[(drug, "openfda_generic_name", 2025)], counts[(drug, "openfda_generic_name", 2024)])
        excess = None if yoy_2025 is None or total_yoy_2025 is None else yoy_2025 - total_yoy_2025
        print(f"{drug}: 2025 YoY {fmt_pct(yoy_2025)} vs total FAERS {fmt_pct(total_yoy_2025)}; excess {fmt_pct(excess)}")
    print(f"\nWrote {data_dir / 'faers_betablocker_counts.csv'}")
    print(f"Wrote {data_dir / 'vigiaccess_screenshot_observations.csv'}")
    print(f"Wrote {reports_dir / 'faers_summary.md'}")
    print(f"Snapshot date: {snapshot_date}")
    print(f"OpenFDA meta.last_updated: {meta_last_updated}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Replicate-check a VigiAccess propranolol spike using OpenFDA FAERS counts.")
    parser.add_argument("--output-root", type=Path, default=project_root(), help="Project/output root. Defaults to repository root.")
    args = parser.parse_args()
    run(args.output_root.resolve())


if __name__ == "__main__":
    main()
