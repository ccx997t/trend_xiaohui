# 字段定义

结构化日线 CSV 的字段如下。无法可靠识别时写 `NA` 或留空。

| 字段 | 含义 |
|---|---|
| date | 交易日，YYYY-MM-DD |
| code / name | 股票代码、名称 |
| board_count | 当日连板数 |
| open_pct / close_pct | 开盘、收盘涨跌幅（数值） |
| turnover_rate / amount | 换手率、成交金额 |
| first_limit_time / last_limit_time | 首次、最后封板时间 |
| open_board_count / seal_amount | 炸板次数、封单金额 |
| sector | 当日主要题材；无法可靠确认时为 NA |
| sector_strength | 强 / 中 / 弱 / NA，基于同题材涨停广度与梯队，不是主观热度 |
| sector_limit_up_count | 同题材当日涨停家数；来源不完整时为 NA |
| sector_board_count | 同题材当日连板家数；来源不完整时为 NA |
| sector_highest_board | 同题材当日最高连板高度；来源不完整时为 NA |
| sector_ladder | 简短梯队，例如 `4板A → 3板B → 2板本股` |
| sector_source | 板块归属和梯队数据的来源；不可确认时为 NA |
| sector_confidence | 高 / 中 / 低：基于来源完整度与归属明确度 |
| market_role | 在题材中的核心、前排、跟风、补涨、独立或 NA |
| notes | 原始信息无法结构化时的简注 |
| analysis_rank | 可选：当日人工强弱排序；无板块/结构证据而不排序时留空，长期统计不得自动按成交额补排 |

长期统计字段另见 `baseline/historical_statistics.csv` 首行。
