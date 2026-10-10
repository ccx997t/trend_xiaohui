#!/usr/bin/env python3
"""基于长期统计生成简要月报。"""
from __future__ import annotations
import argparse, csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--month", required=True, help="YYYY-MM"); parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if len(args.month) != 7 or args.month[4] != "-": raise SystemExit("月格式应为 YYYY-MM")
    with (ROOT / "baseline/historical_statistics.csv").open(encoding="utf-8-sig", newline="") as f: rows = [r for r in csv.DictReader(f) if r.get("date", "").startswith(args.month)]
    reviewed = [r for r in rows if r.get("is_third_board") in {"0", "1"}]; promoted = [r for r in reviewed if r["is_third_board"] == "1"]
    rate = f"{len(promoted) / len(reviewed):.1%}" if reviewed else "暂不计算（无已复盘样本）"
    content = f"# {args.month} 月度复盘\n\n## 自动统计\n\n- 二板样本：{len(rows)}\n- 已复盘样本：{len(reviewed)}\n- 次日晋级三板：{len(promoted)}\n- 晋级率：{rate}\n\n## 人工复盘\n\n- 高频成功特征：\n- 高频失败特征：\n- 典型成功案例：\n- 典型失败案例：\n- 已失效规则：\n- 下月继续验证的假设：\n"
    target = ROOT / "data" / "monthly" / f"{args.month}.md"
    if args.dry_run: print(f"检查通过：将生成 {target.relative_to(ROOT)}"); return
    target.parent.mkdir(parents=True, exist_ok=True); target.write_text(content, encoding="utf-8"); print(f"已生成 {target.relative_to(ROOT)}")
if __name__ == "__main__": main()
