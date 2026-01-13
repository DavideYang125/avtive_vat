import json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# 读取数据
with open('data.txt', 'r', encoding='utf-8') as f:
    content = f.read()

data = json.loads(content)

# 转换为 datetime 和数值
dates = [datetime.fromtimestamp(item[0]/1000) for item in data]
values = [item[1] for item in data]

# 只保留最近一年的数据
end_date = dates[-1]
start_date = end_date - timedelta(days=365)

filtered_dates = []
filtered_values = []

for d, v in zip(dates, values):
    if d >= start_date:
        filtered_dates.append(d)
        filtered_values.append(v)

# 计算每日变化量
diffs = [filtered_values[i] - filtered_values[i-1] for i in range(1, len(filtered_values))]
diff_dates = filtered_dates[1:]

# 分别处理增加和减少
diffs_pos = [d if d > 0 else 0 for d in diffs]
diffs_neg = [d if d < 0 else 0 for d in diffs]

# 画图
plt.figure(figsize=(15,6))
plt.bar(diff_dates, diffs_pos, color='green', label='Increase')
plt.bar(diff_dates, diffs_neg, color='red', label='Decrease')
plt.xticks(rotation=45)
plt.title('Daily Change in Value (Last 1 Year)')
plt.ylabel('Change')
plt.xlabel('Date')
plt.legend()
plt.tight_layout()
plt.show()
