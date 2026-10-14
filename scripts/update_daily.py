#!/usr/bin/env python3
"""将已填写次日结果的二板候选同步至长期统计。"""
from __future__ import annotations

import argparse
import csv
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIELDS = [
    "date", "code", "name", "sector", "board_count", "analysis_rank",
    "next_open_pct", "is_third_board", "first_limit_time", "open_board_count",
    "turnover_rate", "amount", "seal_amount", "sector_strength", "sector_limit_up_count",
    "sector_board_count", "sector_highest_board", "sector_ladder", "sector_source",
    "sector_confidence", "market_role",
    "judgment_basis", "failure_reason", "tags", "source_daily", "updated_at",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def amount_as_yi(value: str) -> float:
    """将截图常见的“亿/万”成交额转换为可排序数值；无法识别时置后。"""
    try:
        if value.endswith("亿"):
            return float(value[:-1])
        if value.endswith("万"):
            return float(value[:-1]) / 10000
    except ValueError:
        pass
    return -1.0


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", required=True, help="二板发生日，YYYY-MM-DD")
    parser.add_argument("--results", type=Path, help="可选：次日结果 CSV，至少含 code、next_open_pct、is_third_board")
    parser.add_argument("--dry-run", action="store_true", help="仅检查，不写文件")
    args = parser.parse_args()
    day = date.fromisoformat(args.date)
    structured = ROOT / "data" / "structured" / f"{day:%Y}" / f"{day:%m}" / f"{day}.csv"
    if not structured.exists():
        raise SystemExit(f"未找到结构化文件：{structured.relative_to(ROOT)}")

    candidates = [row for row in read_csv(structured) if row.get("board_count", "").strip() == "2"]
    sector_context_path = structured.with_name(f"{day}_sector_context.csv")
    if sector_context_path.exists():
        sector_context = {
            row.get("code", "").strip(): row
            for row in read_csv(sector_context_path)
            if row.get("code", "").strip()
        }
        candidates = [
            {**row, **sector_context.get(row.get("code", "").strip(), {})}
            for row in candidates
        ]
    ranked = [row for row in candidates if row.get("analysis_rank", "").strip().isdigit()]
    if ranked:
        candidates.sort(
            key=lambda row: int(row["analysis_rank"])
            if row.get("analysis_rank", "").strip().isdigit()
            else 9999
        )
    results: dict[str, dict[str, str]] = {}
    if args.results:
        if not args.results.exists():
            raise SystemExit(f"未找到结果文件：{args.results}")
        results = {row.get("code", "").strip(): row for row in read_csv(args.results) if row.get("code", "").strip()}
    stats_path = ROOT / "baseline" / "historical_statistics.csv"
    old = read_csv(stats_path) if stats_path.exists() else []
    retained = [row for row in old if row.get("date") != args.date]
    records = []
    for row in candidates:
        record = {field: "" for field in FIELDS}
        record.update({
            "date": args.date, "code": row.get("code", ""), "name": row.get("name", ""),
            "sector": row.get("sector", ""), "board_count": "2", "analysis_rank": row.get("analysis_rank", "").strip(),
            "first_limit_time": row.get("first_limit_time", ""),
            "open_board_count": row.get("open_board_count", ""),
            "turnover_rate": row.get("turnover_rate", ""), "amount": row.get("amount", ""),
            "seal_amount": row.get("seal_amount", ""), "sector_strength": row.get("sector_strength", ""),
            "sector_limit_up_count": row.get("sector_limit_up_count", ""),
            "sector_board_count": row.get("sector_board_count", ""),
            "sector_highest_board": row.get("sector_highest_board", ""),
            "sector_ladder": row.get("sector_ladder", ""),
            "sector_source": row.get("sector_source", ""),
            "sector_confidence": row.get("sector_confidence", ""),
            "market_role": row.get("market_role", ""), "judgment_basis": row.get("notes", ""),
            "source_daily": f"data/daily/{day:%Y}/{day:%m}/{day}.md", "updated_at": str(date.today()),
        })
        result = results.get(record["code"])
        if result:
            record.update({
                "next_open_pct": result.get("next_open_pct", ""),
                "is_third_board": result.get("is_third_board", ""),
                "failure_reason": result.get("failure_reason", ""),
                "tags": result.get("notes", ""),
            })
        records.append(record)
    if args.dry_run:
        print(f"检查通过：{len(records)} 个二板候选将写入 {stats_path.relative_to(ROOT)}")
        return
    with stats_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(retained + records)
    print(f"已同步 {len(records)} 个二板候选；已匹配 {sum(r['code'] in results for r in records)} 条次日结果。")


if __name__ == "__main__":
    main()
