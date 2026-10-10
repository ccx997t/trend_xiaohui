# 趋势小辉

用于归档每日连板数据、分析二板（2进3）并逐步沉淀可验证规律的本地研究工程。

## 快速开始

1. 将当天截图或表格保存到 `data/raw/YYYY/MM/`。
2. 将可靠识别出的连板数据填入 `data/structured/YYYY/MM/YYYY-MM-DD.csv`（可复制 `templates/daily_structured.csv`）。
3. 根据 `prompts/daily_analysis.md` 生成当天复盘到 `data/daily/YYYY/MM/`。
4. 次交易日补齐结果，执行：

```bash
python3 scripts/update_daily.py --date YYYY-MM-DD --results path/to/next_day_results.csv
```

5. 周末、月末分别执行：

```bash
python3 scripts/aggregate_weekly.py --week YYYY-Www
python3 scripts/aggregate_monthly.py --month YYYY-MM
```

所有脚本只处理已有的结构化/日线数据；不会读取或修改 `data/raw/`。

## 数据约定

- 不确定字段填 `NA` 或留空，禁止猜测。
- `is_third_board` 使用 `1`、`0` 或空值（尚未复盘）；复盘结果 CSV 可复制 `templates/next_day_results.csv`。
- 日线中候选表必须包含“代码”，供脚本回写统计与结果。
- 脚本生成的周报、月报可以继续人工补充分析内容。

详细规范见 [trend_Codex_v1.0.md](trend_Codex_v1.0.md)。
