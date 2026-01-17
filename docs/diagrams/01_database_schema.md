# Диаграмма IDEF1X - Схема базы данных

## Описание структуры БД

База данных находится в **3 нормальной форме (3НФ)**.

---

## Таблицы и связи

### 1. accounts_user (Пользователи)
**PK:** id  
**Описание:** Кастомная модель пользователя с ролями

| Поле | Тип | Ограничения | Описание |
|------|-----|-------------|----------|
| id | INTEGER | PK, AUTO_INCREMENT | Идентификатор |
| username | VARCHAR(150) | UNIQUE, NOT NULL | Имя пользователя |
| email | VARCHAR(254) | UNIQUE, NOT NULL | Email |
| password | VARCHAR(128) | NOT NULL | Хеш пароля |
| first_name | VARCHAR(150) | NOT NULL | Имя |
| last_name | VARCHAR(150) | NOT NULL | Фамилия |
| role | VARCHAR(10) | NOT NULL, DEFAULT 'CLIENT' | Роль (CLIENT, MANAGER, ADMIN) |
| phone_number | VARCHAR(17) | | Телефон |
| address | TEXT | | Адрес |
| date_of_birth | DATE | | Дата рождения |
| avatar | VARCHAR(100) | | Путь к аватару |
| is_active | BOOLEAN | DEFAULT TRUE | Активен |
| is_staff | BOOLEAN | DEFAULT FALSE | Сотрудник |
| is_superuser | BOOLEAN | DEFAULT FALSE | Суперпользователь |
| created_at | TIMESTAMP | NOT NULL | Дата регистрации |
| updated_at | TIMESTAMP | NOT NULL | Дата обновления |

---

### 2. inventory_category (Категории)
**PK:** id  
**Описание:** Категории спортивного инвентаря

| Поле | Тип | Ограничения | Описание |
|------|-----|-------------|----------|
| id | INTEGER | PK, AUTO_INCREMENT | Идентификатор |
| name | VARCHAR(100) | UNIQUE, NOT NULL | Название |
| slug | VARCHAR(100) | UNIQUE, NOT NULL | URL-slug |
| description | TEXT | | Описание |
| image | VARCHAR(100) | | Путь к изображению |
| is_active | BOOLEAN | DEFAULT TRUE | Активна |
| created_at | TIMESTAMP | NOT NULL | Дата создания |

---

### 3. inventory_equipment (Инвентарь)
**PK:** id  
**FK:** category_id → inventory_category(id)  
**Описание:** Спортивный инвентарь для аренды

| Поле | Тип | Ограничения | Описание |
|------|-----|-------------|----------|
| id | INTEGER | PK, AUTO_INCREMENT | Идентификатор |
| category_id | INTEGER | FK, NOT NULL | Категория |
| name | VARCHAR(200) | NOT NULL | Название |
| slug | VARCHAR(200) | UNIQUE, NOT NULL | URL-slug |
| description | TEXT | NOT NULL | Описание |
| image | VARCHAR(100) | NOT NULL | Изображение |
| brand | VARCHAR(100) | | Бренд |
| model | VARCHAR(100) | | Модель |
| size | VARCHAR(50) | NOT NULL | Размер |
| condition | VARCHAR(20) | NOT NULL | Состояние (EXCELLENT, GOOD, SATISFACTORY) |
| price_per_day | DECIMAL(10,2) | NOT NULL, CHECK >= 0 | Цена за день (руб.) |
| quantity_total | INTEGER | NOT NULL, CHECK >= 1 | Общее количество |
| quantity_available | INTEGER | NOT NULL, CHECK >= 0 | Доступно |
| is_active | BOOLEAN | DEFAULT TRUE | Активен |
| created_at | TIMESTAMP | NOT NULL | Дата добавления |
| updated_at | TIMESTAMP | NOT NULL | Дата обновления |

**Связь:** category_id → inventory_category.id (PROTECT)

---

### 4. rentals_cart (Корзина)
**PK:** id  
**FK:** user_id → accounts_user(id)  
**Описание:** Корзина пользователя

| Поле | Тип | Ограничения | Описание |
|------|-----|-------------|----------|
| id | INTEGER | PK, AUTO_INCREMENT | Идентификатор |
| user_id | INTEGER | FK, UNIQUE, NOT NULL | Пользователь |
| created_at | TIMESTAMP | NOT NULL | Дата создания |
| updated_at | TIMESTAMP | NOT NULL | Дата обновления |

**Связь:** user_id → accounts_user.id (CASCADE)

---

### 5. rentals_cartitem (Позиции корзины)
**PK:** id  
**FK:** cart_id → rentals_cart(id), equipment_id → inventory_equipment(id)  
**Описание:** Товары в корзине

| Поле | Тип | Ограничения | Описание |
|------|-----|-------------|----------|
| id | INTEGER | PK, AUTO_INCREMENT | Идентификатор |
| cart_id | INTEGER | FK, NOT NULL | Корзина |
| equipment_id | INTEGER | FK, NOT NULL | Инвентарь |
| quantity | INTEGER | NOT NULL, CHECK >= 1 | Количество |
| start_date | DATE | NOT NULL | Дата начала |
| end_date | DATE | NOT NULL | Дата окончания |
| added_at | TIMESTAMP | NOT NULL | Дата добавления |

**Связи:**
- cart_id → rentals_cart.id (CASCADE)
- equipment_id → inventory_equipment.id (CASCADE)

**UNIQUE:** (cart_id, equipment_id, start_date, end_date)

---

### 6. rentals_rental (Аренда)
**PK:** id  
**FK:** user_id → accounts_user(id), confirmed_by_id → accounts_user(id)  
**Описание:** Заказы аренды

| Поле | Тип | Ограничения | Описание |
|------|-----|-------------|----------|
| id | INTEGER | PK, AUTO_INCREMENT | Идентификатор |
| user_id | INTEGER | FK, NOT NULL | Клиент |
| status | VARCHAR(20) | NOT NULL | Статус (PENDING, CONFIRMED, ACTIVE, COMPLETED, CANCELLED) |
| start_date | DATE | NOT NULL | Дата начала |
| end_date | DATE | NOT NULL | Дата окончания |
| total_price | DECIMAL(10,2) | NOT NULL, CHECK >= 0 | Общая стоимость |
| comment | TEXT | | Комментарий |
| created_at | TIMESTAMP | NOT NULL | Дата создания |
| updated_at | TIMESTAMP | NOT NULL | Дата обновления |
| confirmed_at | TIMESTAMP | | Дата подтверждения |
| confirmed_by_id | INTEGER | FK, NULL | Кто подтвердил |

**Связи:**
- user_id → accounts_user.id (CASCADE)
- confirmed_by_id → accounts_user.id (SET_NULL)

---

### 7. rentals_rentalitem (Позиции аренды)
**PK:** id  
**FK:** rental_id → rentals_rental(id), equipment_id → inventory_equipment(id)  
**Описание:** Товары в заказе аренды

| Поле | Тип | Ограничения | Описание |
|------|-----|-------------|----------|
| id | INTEGER | PK, AUTO_INCREMENT | Идентификатор |
| rental_id | INTEGER | FK, NOT NULL | Заказ |
| equipment_id | INTEGER | FK, NOT NULL | Инвентарь |
| quantity | INTEGER | NOT NULL, CHECK >= 1 | Количество |
| price_per_day | DECIMAL(10,2) | NOT NULL, CHECK >= 0 | Цена за день (на момент заказа) |
| days | INTEGER | NOT NULL, CHECK >= 1 | Количество дней |
| subtotal | DECIMAL(10,2) | NOT NULL, CHECK >= 0 | Подытог |

**Связи:**
- rental_id → rentals_rental.id (CASCADE)
- equipment_id → inventory_equipment.id (PROTECT)

**UNIQUE:** (rental_id, equipment_id)

---

### 8. rentals_review (Отзывы)
**PK:** id  
**FK:** user_id, equipment_id, rental_id  
**Описание:** Отзывы клиентов

| Поле | Тип | Ограничения | Описание |
|------|-----|-------------|----------|
| id | INTEGER | PK, AUTO_INCREMENT | Идентификатор |
| user_id | INTEGER | FK, NOT NULL | Пользователь |
| equipment_id | INTEGER | FK, NOT NULL | Инвентарь |
| rental_id | INTEGER | FK, NOT NULL | Заказ |
| rating | INTEGER | NOT NULL, CHECK 1-5 | Оценка (1-5) |
| comment | TEXT | NOT NULL | Комментарий |
| created_at | TIMESTAMP | NOT NULL | Дата создания |

**Связи:**
- user_id → accounts_user.id (CASCADE)
- equipment_id → inventory_equipment.id (CASCADE)
- rental_id → rentals_rental.id (CASCADE)

**UNIQUE:** (user_id, equipment_id, rental_id)

---

## ER-диаграмма (текстовое представление)
```
┌─────────────────┐
│ accounts_user   │
│ (Пользователи)  │
├─────────────────┤
│ PK id           │
│    username     │
│    email        │
│    role         │
│    ...          │
└────────┬────────┘
         │
         │ 1:1
         │
┌────────▼────────┐      ┌──────────────────┐
│ rentals_cart    │  1:N │ rentals_cartitem │
│ (Корзина)       ├──────┤ (Позиции корзины)│
├─────────────────┤      ├──────────────────┤
│ PK id           │      │ PK id            │
│ FK user_id      │      │ FK cart_id       │
│    ...          │      │ FK equipment_id  │
└─────────────────┘      │    quantity      │
                         │    start_date    │
                         │    end_date      │
                         └────────┬─────────┘
                                  │
         ┌────────────────────────┘
         │
         │
┌────────▼────────┐      ┌──────────────────┐
│ inventory_      │  1:N │ inventory_       │
│ category        ├──────┤ equipment        │
│ (Категории)     │      │ (Инвентарь)      │
├─────────────────┤      ├──────────────────┤
│ PK id           │      │ PK id            │
│    name         │      │ FK category_id   │
│    slug         │      │    name          │
│    ...          │      │    price_per_day │
└─────────────────┘      │    quantity_...  │
                         │    ...           │
                         └────────┬─────────┘
                                  │
                                  │ N:1
                                  │
         ┌────────────────────────┴──────────────┐
         │                                       │
┌────────▼────────┐      ┌──────────────────┐   │
│ rentals_rental  │  1:N │ rentals_         │   │
│ (Аренда)        ├──────┤ rentalitem       │   │
├─────────────────┤      │ (Позиции аренды) │   │
│ PK id           │      ├──────────────────┤   │
│ FK user_id      │      │ PK id            │   │
│ FK confirmed_by │      │ FK rental_id     │   │
│    status       │      │ FK equipment_id──┼───┘
│    total_price  │      │    quantity      │
│    ...          │      │    price_per_day │
└────────┬────────┘      │    days          │
         │               │    subtotal      │
         │               └──────────────────┘
         │
         │ 1:N
         │
┌────────▼────────┐
│ rentals_review  │
│ (Отзывы)        │
├─────────────────┤
│ PK id           │
│ FK user_id      │
│ FK equipment_id │
│ FK rental_id    │
│    rating       │
│    comment      │
└─────────────────┘
```

---

## Проверка на 3НФ

### 1НФ (Первая нормальная форма):
✅ Все атрибуты атомарны  
✅ Нет повторяющихся групп  
✅ Каждая таблица имеет первичный ключ

### 2НФ (Вторая нормальная форма):
✅ Выполнена 1НФ  
✅ Все неключевые атрибуты полностью зависят от первичного ключа  
✅ Нет частичных зависимостей

### 3НФ (Третья нормальная форма):
✅ Выполнена 2НФ  
✅ Отсутствуют транзитивные зависимости  
✅ Все неключевые атрибуты зависят только от первичного ключа

**Вывод:** База данных соответствует 3НФ ✅