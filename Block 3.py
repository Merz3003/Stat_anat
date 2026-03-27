import matplotlib.pyplot as plt
import numpy as np

# Данные
companies = ["Роснефть", "Татнефть", "Газпромнефть", "Лукойл", "Сургутнефтегаз"]

revenue_index = np.array([1.157332542, 1.422924901, 0.7850151899, 1.275236115, 1.112106711])
prod_index = np.array([1.173969197, 1.30084555, 0.7508568443, 1.247222332, 1.139832363])
fondo_index = np.array([0.9119489668, 1.240583266, 0.6840185099, 1.11204751, 0.6791772157])

# Размер пузырей
sizes = fondo_index * 1800

# Средние значения
mean_revenue = revenue_index.mean()
mean_prod = prod_index.mean()

plt.figure(figsize=(10, 7))

# Пузырьковая диаграмма
plt.scatter(revenue_index, prod_index, s=sizes, alpha=0.6, edgecolors='black')

# Подписи точек
for i, company in enumerate(companies):
    plt.text(revenue_index[i] + 0.01, prod_index[i] + 0.01, company, fontsize=10)

# Линии средних
plt.axvline(mean_revenue, linestyle='--', label='Средний индекс выручки')
plt.axhline(mean_prod, linestyle='--', label='Средний индекс производительности')

# Оформление
plt.title("Карта групп нефтяных компаний (bubble chart)")
plt.xlabel("Индекс выручки 2024")
plt.ylabel("Индекс производительности труда 2024")
plt.legend()
plt.grid(True)
plt.show()