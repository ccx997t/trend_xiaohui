# 月度复盘

生成 `{YEAR}-{MONTH}` 月度复盘。优先读取本月 weekly、长期基线和历史统计；仅统计异常时回查 daily，仍无法确认时才回查 raw。

输出到 `data/monthly/{YEAR}-{MONTH}.md`；必要时更新长期基线，并在 `baseline/rule_changelog.md` 记录规则变更。
