#!/usr/bin/env python3
"""基于长期统计生成简要周报。"""
from __future__ import annotations
import argparse, csv
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--week", required=True, help="ISO 周，例如 2026-W39")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        year, week = args.week.split("-W")
        start = date.fromisocalendar(int(year), int(week), 1)
        end = date.fromisocalendar(int(year), int(week), 5)
    except ValueError as exc:
        raise SystemExit("周格式应为 YYYY-Www") from exc
    with (ROOT / "baseline/historical_statistics.csv").open(encoding="utf-8-sig", newline="") as f:
        rows = [r for r in csv.DictReader(f) if start.isoformat() <= r.get("date", "") <= end.isoformat()]
    reviewed = [r for r in rows if r.get("is_third_board") in {"0", "1"}]
    promoted = [r for r in reviewed if r["is_third_board"] == "1"]
    top = [r for r in reviewed if r.get("analysis_rank") == "1"]
    top_promoted = [r for r in top if r["is_third_board"] == "1"]
    content = f"# {args.week} 周度复盘\n\n## 自动统计\n\n- 二板样本：{len(rows)}\n- 已复盘样本：{len(reviewed)}\n- 次日晋级三板：{len(promoted)}\n- 已复盘晋级率：{len(promoted) / len(reviewed):.1%}" if reviewed else f"# {args.week} 周度复盘\n\n## 自动统计\n\n- 二板样本：{len(rows)}\n- 已复盘样本：0（暂不计算晋级率）"
    content += f"\n- 排名第一已复盘：{len(top)}\n- 排名第一晋级：{len(top_promoted)}\n\n## 人工复盘\n\n- 本周总体市场特征：\n- 成功判断：\n- 失败判断：\n- 新增待验证假设：\n- 下周观察点：\n"
    target = ROOT / "data" / "weekly" / f"{args.week}.md"
    if args.dry_run: print(f"检查通过：将生成 {target.relative_to(ROOT)}"); return
    target.parent.mkdir(parents=True, exist_ok=True); target.write_text(content, encoding="utf-8")
    print(f"已生成 {target.relative_to(ROOT)}")
if __name__ == "__main__": main()
