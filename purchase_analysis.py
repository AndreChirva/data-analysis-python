import psycopg2
from psycopg2.extras import RealDictCursor


def get_purchases():
    connection_params = {
        'host': 'localhost',
        'port': '5432',
        'user': 'postgres',
        'password': 'cdby7887',
        'database': 'postgres'

    }

    purchases = []
    conn = None

    try:
        # Подключаемся к базе данных
        conn = psycopg2.connect(**connection_params)

        # Используем RealDictCursor для получения результатов в виде словаря
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:


            # Выполняем запрос
            cursor.execute("SELECT item, category, price, quantity FROM purchases")

            # Получаем все записи
            rows = cursor.fetchall()

            # Конвертируем каждую запись в словарь нужного формата
            for row in rows:
                purchase = {
                    "item": row["item"],
                    "category": row["category"],
                    "price": float(row["price"]),  # Исправлено: было row["'price"]
                    "quantity": row["quantity"]
                }
                purchases.append(purchase)

    except Exception as e:
        print(f"Ошибка при подключении к базе данных: {e}")
    finally:
        if conn:  
            conn.close()

    return purchases


if __name__ == "__main__":
    purchases = get_purchases()
    print(purchases)

def total_revenue(purchases):
    return sum(item["price"] * item["quantity"] for item in purchases)

def items_by_category(purchases):
    categories = {}

    for purchase in purchases:
        category = purchase["category"]
        item = purchase["item"]

        # Если категории еще нет в словаре, создаем пустой список
        if category not in categories:
            categories[category] = []

        # Добавляем товар, только если его еще нет в списке
        if item not in categories[category]:
            categories[category].append(item)

    return categories

def expensive_purchases(purchases, min_price):
    return [purchase for purchase in purchases if purchase["price"] >= min_price]

def average_price_by_category(purchases):
    category_stats = {}
    for purchase in purchases:
        category = purchase["category"]
        price = purchase["price"]
        if category not in category_stats:
            category_stats[category] = {"total_price": 0, "count": 0}
        category_stats[category]["total_price"] += price
        category_stats[category]["count"] += 1
    average_prices = {}
    for category, stats in category_stats.items():
        average_prices[category] = stats["total_price"] / stats["count"]

    return average_prices


def most_frequent_category(purchases):
    category_quantities = {}
    for purchase in purchases:
        category = purchase["category"]
        quantity = purchase["quantity"]
        if category in category_quantities:
            category_quantities[category] += quantity
        else:
            category_quantities[category] = quantity

    max_category = None
    max_quantity = 0
    for category, total_quantity in category_quantities.items():
        if total_quantity > max_quantity:
            max_quantity = total_quantity
            max_category = category

    return max_category


# Вычисляем общую выручку
revenue = total_revenue(purchases)
print(f"Общая выручка: {revenue:.1f}")

# Группируем товары по категориям
categorized_items = items_by_category(purchases)
print(f"Товары по категориям: {categorized_items}")
# Покупки дороже: $
exp = expensive_purchases(purchases, 1.0)
print(f"Покупки дороже 1.0: {exp}")
# Средняя цена по категориям
avg_price = average_price_by_category(purchases)
print(f"Средняя цена по категориям: {avg_price}")
#Категория с наибольшим количеством проданных товаров
most_frequent = most_frequent_category(purchases)
print(f"Категория с наибольшим количеством проданных товаров: {most_frequent}")
