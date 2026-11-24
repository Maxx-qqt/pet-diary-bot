import os
import pandas as pd
import matplotlib.pyplot as plt

os.makedirs('images', exist_ok=True)

try:
    df = pd.read_csv('pets_data.csv')
except FileNotFoundError:
    print("Ошибка: Файл pets_data.csv не найден в текущей папке!")
    exit()

df['is_overdue_num'] = df['is_overdue'].replace({'Да': 1, 'Нет': 0})

overdue_counts = df['is_overdue'].value_counts()
plt.figure()
plt.pie(overdue_counts, labels=['Не просрочено', 'Просрочено'], autopct='%1.1f%%', colors=['green', 'red'])
plt.title('Соотношение просроченных и сделанных прививок')
plt.savefig('images/1_overdue_pie.png')
plt.close()


pet_overdue_pct = df.groupby('pet_type')['is_overdue_num'].mean() * 100
plt.figure()
plt.bar(pet_overdue_pct.index, pet_overdue_pct.values, color='blue')
plt.title('Процент просроченных прививок по видам')
plt.xlabel('Вид животного')
plt.ylabel('Процент просрочки (%)')

for i in range(len(pet_overdue_pct)):
    yval = pet_overdue_pct.values[i]
    plt.text(i, yval, f'{yval:.1f}%', ha='center', va='bottom')

plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig('images/2_overdue_by_type.png')
plt.close()


age_overdue_pct = df.groupby('age_years')['is_overdue_num'].mean() * 100
plt.figure()
plt.plot(age_overdue_pct.index, age_overdue_pct.values, marker='o', color='orange')
plt.title('Зависимость пропусков от возраста питомца')
plt.xlabel('Возраст питомца (лет)')
plt.ylabel('Процент просрочки (%)')
plt.grid()
plt.savefig('images/3_overdue_by_age.png')
plt.close()


plt.figure()
plt.hist(df['owner_age'], bins=8, color='skyblue', edgecolor='black')
plt.title('Распределение владельцев по возрасту')
plt.xlabel('Возраст владельца (лет)')
plt.ylabel('Количество человек')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig('images/4_owner_age_hist.png')
plt.close()


vac_stats = df.groupby('vaccine_type').agg(
    total=('pet_id', 'count'),
    overdue_sum=('is_overdue_num', 'sum')
)
vac_stats['overdue_pct'] = vac_stats['overdue_sum'] / vac_stats['total'] * 100

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

ax1.bar(vac_stats.index, vac_stats['total'], color='green')
ax1.set_title('Количество записей по вакцинам')
ax1.set_ylabel('Количество записей')

for i in range(len(vac_stats)):
    yval = vac_stats['total'].values[i]
    ax1.text(i, yval + 0.4, f'{yval:.0f}', ha='center', va='bottom')
ax1.grid(axis='y', linestyle='--', alpha=0.7)

ax2.bar(vac_stats.index, vac_stats['overdue_pct'], color='red')
ax2.set_title('Процент просрочки по вакцинам')
ax2.set_ylabel('Процент просрочки (%)')

for i in range(len(vac_stats)):
    yval = vac_stats['overdue_pct'].values[i]
    ax2.text(i, yval + 0.2, f'{yval:.1f}%', ha='center', va='bottom')
ax2.grid(axis='y', linestyle='--', alpha=0.7)

plt.savefig('images/5_vaccine_analysis.png')
plt.close()

print("Графики готовы")