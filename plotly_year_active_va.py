import json
from datetime import datetime, timedelta
import plotly.graph_objects as go

# 读取数据
with open('data.txt', 'r', encoding='utf-8') as f:
    content = f.read()

data = json.loads(content)

# 转换为 datetime 和数值
dates = [datetime.fromtimestamp(item[0]/1000) for item in data]
values = [item[1] for item in data]

# 最近一年
end_date = dates[-1]
start_date = end_date - timedelta(days=365)

filtered_dates = []
filtered_values = []

for d, v in zip(dates, values):
    if d >= start_date:
        filtered_dates.append(d)
        filtered_values.append(v)

# 计算变化量
diffs = [filtered_values[i] - filtered_values[i-1] for i in range(1, len(filtered_values))]
diff_dates = filtered_dates[1:]
diff_values = filtered_values[1:]

# 准备颜色：增加绿色，减少红色
colors = ['green' if d > 0 else 'red' for d in diffs]

# 创建柱状图
fig = go.Figure(data=[go.Bar(
    x=diff_dates,
    y=diffs,
    marker_color=colors,
    hovertemplate=
    'Date: %{x|%Y-%m-%d}<br>' +
    'Value: %{customdata[0]}<br>' +
    'Change: %{y}<extra></extra>',
    customdata=list(zip(diff_values))
)])

fig.update_layout(
    title='Daily Change in Value (Last 1 Year)',
    xaxis_title='Date',
    yaxis_title='Change',
    bargap=0.1,
    xaxis=dict(tickangle=-45)
)

fig.show()
