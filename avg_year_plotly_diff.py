import json
from datetime import datetime, timedelta
import plotly.graph_objects as go

# 1. 读取数据
with open("data.txt", "r", encoding="utf-8") as f:
    content = f.read().strip()

data = json.loads(content)  # [[timestamp, value], ...]

# 2. 转换时间戳为日期
for i in range(len(data)):
    # 毫秒 -> 秒
    ts_sec = data[i][0] / 1000
    data[i][0] = datetime.fromtimestamp(ts_sec).date()

# 3. 取最近一年的数据
last_date = data[-1][0]
one_year_ago = last_date - timedelta(days=365)
data_last_year = [d for d in data if d[0] >= one_year_ago]

dates = [d[0] for d in data_last_year]
values = [d[1] for d in data_last_year]

# 4. 计算平均值
avg_value = sum(values) / len(values)

# 5. 计算差值（与平均值的差）
diffs = [v - avg_value for v in values]

# 6. 分正负差值，方便颜色区分
pos_diffs = [d if d > 0 else 0 for d in diffs]
neg_diffs = [d if d < 0 else 0 for d in diffs]

# 7. 绘制交互式图表
fig = go.Figure()

fig.add_trace(go.Bar(
    x=dates,
    y=pos_diffs,
    name="高于平均值",
    marker_color='green',
    hovertemplate='日期: %{x}<br>值: %{y:.0f}<br>差值: %{y:.0f}<extra></extra>'
))

fig.add_trace(go.Bar(
    x=dates,
    y=neg_diffs,
    name="低于平均值",
    marker_color='red',
    hovertemplate='日期: %{x}<br>值: %{y:.0f}<br>差值: %{y:.0f}<extra></extra>'
))

# 8. 更新布局
fig.update_layout(
    title="最近一年数据与平均值差异",
    xaxis_title="日期",
    yaxis_title="差值（相对于平均值）",
    barmode='relative',
    hovermode="x unified"
)

fig.show()
