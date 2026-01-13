import json
from datetime import datetime
import matplotlib.pyplot as plt

# ===== 1. 读取 data.txt =====
with open('data.txt', 'r', encoding='utf-8') as f:
    content = f.read().strip()

# ===== 2. 严谨解析：先整体 JSON，失败再逐行 =====
try:
    raw_data = json.loads(content)

    # 校验：必须是 [[ts, value], ...]
    if not (
        isinstance(raw_data, list)
        and all(
            isinstance(item, list)
            and len(item) == 2
            for item in raw_data
        )
    ):
        raise ValueError("Invalid JSON array format")

except Exception:
    # 回退：逐行解析
    raw_data = []
    for line in content.splitlines():
        line = line.strip()
        if not line:
            continue
        raw_data.append(json.loads(line))

# ===== 3. 时间戳 -> 日期 & 计算 Delta =====
dates = []
values = []
deltas = []

prev_value = None

for ts, value in raw_data:
    date = datetime.utcfromtimestamp(ts / 1000).strftime('%Y-%m-%d')
    dates.append(date)
    values.append(value)

    deltas.append(0 if prev_value is None else value - prev_value)
    prev_value = value

# 去掉第一天
dates, values, deltas = dates[1:], values[1:], deltas[1:]

# ===== 4. 颜色区分 =====
colors = ['#16a34a' if d >= 0 else '#dc2626' for d in deltas]

# ===== 5. 绘图 =====
plt.figure(figsize=(18, 6))
plt.bar(dates, deltas, color=colors)
plt.axhline(0, color='black', linewidth=0.8)

step = max(len(dates) // 12, 1)
plt.xticks(dates[::step], rotation=45)

plt.title('Daily Change of Active Ethereum Validators')
plt.xlabel('Date (UTC)')
plt.ylabel('Δ Validators vs Previous Day')

plt.tight_layout()
plt.show()
