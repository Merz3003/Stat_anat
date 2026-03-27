import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# ДАННЫЕ (пример: Газпромнефть)
# -----------------------------
years = [2021, 2022, 2023, 2024]

revenue = [2389317290000, 2874037264000, 2753475003000, 3046943699000]
staff = [102.4, 104.3, 104.2, 104.7]

df = pd.DataFrame({
    "Year": years,
    "Revenue": revenue,
    "Staff": staff
})

# -----------------------------
# 1. Производительность и индексы
# -----------------------------
df["Productivity"] = df["Revenue"] / df["Staff"]

# базисные индексы
df["Revenue_index"] = df["Revenue"] / df["Revenue"].iloc[0]
df["Prod_index"] = df["Productivity"] / df["Productivity"].iloc[0]

# -----------------------------
# 2. Тренд (линейное выравнивание)
# -----------------------------
x = np.arange(len(df))

coef_rev = np.polyfit(x, df["Revenue_index"], 1)
coef_prod = np.polyfit(x, df["Prod_index"], 1)

df["Trend_rev"] = np.polyval(coef_rev, x)
df["Trend_prod"] = np.polyval(coef_prod, x)

# -----------------------------
# 3. Случайные колебания
# -----------------------------
df["Random_rev"] = df["Revenue_index"] - df["Trend_rev"]
df["Random_prod"] = df["Prod_index"] - df["Trend_prod"]

# -----------------------------
# 4. Экспоненциальное сглаживание
# -----------------------------
alpha = 0.5

def exp_smooth(series, alpha=0.5):
    smoothed = [series.iloc[0]]
    for i in range(1, len(series)):
        smoothed.append(alpha * series.iloc[i] + (1 - alpha) * smoothed[i - 1])
    return smoothed

df["Smooth_rev"] = exp_smooth(df["Revenue_index"], alpha)
df["Smooth_prod"] = exp_smooth(df["Prod_index"], alpha)

# -----------------------------
# 5. Прогноз на следующий год
# -----------------------------
next_year = df["Year"].iloc[-1] + 1
next_x = len(df)

# прогноз по тренду
forecast_rev_trend = np.polyval(coef_rev, next_x)
forecast_prod_trend = np.polyval(coef_prod, next_x)

# прогноз по экспоненциальному сглаживанию
forecast_rev_smooth = df["Smooth_rev"].iloc[-1]
forecast_prod_smooth = df["Smooth_prod"].iloc[-1]

forecast_df = pd.DataFrame({
    "Year": [next_year],
    "Revenue_index_trend_forecast": [forecast_rev_trend],
    "Revenue_index_smooth_forecast": [forecast_rev_smooth],
    "Prod_index_trend_forecast": [forecast_prod_trend],
    "Prod_index_smooth_forecast": [forecast_prod_smooth]
})

# -----------------------------
# 6. График индекса выручки
# -----------------------------
plt.figure(figsize=(12, 5))
plt.plot(df["Year"], df["Revenue_index"], marker='o', label="Индекс выручки")
plt.plot(df["Year"], df["Trend_rev"], linestyle='--', label="Тренд")
plt.bar(df["Year"], df["Random_rev"], alpha=0.3, label="Случайные колебания")
plt.axhline(0, color='black', linewidth=1)
plt.title("Декомпозиция индекса выручки Лукойл")
plt.xlabel("Год")
plt.ylabel("Индекс")
plt.legend()
plt.grid()
plt.show()

# -----------------------------
# 7. График индекса производительности
# -----------------------------
plt.figure(figsize=(12, 5))
plt.plot(df["Year"], df["Prod_index"], marker='o', label="Индекс производительности")
plt.plot(df["Year"], df["Trend_prod"], linestyle='--', label="Тренд")
plt.bar(df["Year"], df["Random_prod"], alpha=0.3, label="Случайные колебания")
plt.axhline(0, color='black', linewidth=1)
plt.title("Декомпозиция индекса производительности труда Лукойл")
plt.xlabel("Год")
plt.ylabel("Индекс")
plt.legend()
plt.grid()
plt.show()

# -----------------------------
# 8. Таблица результатов
# -----------------------------
print("Исходная таблица:")
print(df[[
    "Year",
    "Revenue",
    "Staff",
    "Productivity",
    "Revenue_index",
    "Prod_index",
    "Trend_rev",
    "Trend_prod",
    "Random_rev",
    "Random_prod"
]])

print("\nПрогноз на следующий год:")
print(forecast_df)

print("\nУравнение тренда индекса выручки:")
print(f"y = {coef_rev[0]:.4f}x + {coef_rev[1]:.4f}")

print("\nУравнение тренда индекса производительности:")
print(f"y = {coef_prod[0]:.4f}x + {coef_prod[1]:.4f}")

print("\nПояснение:")
print("Сезонность не оценивалась, так как данные годовые, а не помесячные и не поквартальные.")