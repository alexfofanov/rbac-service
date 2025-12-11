# Тестовое задание
Реализовать  backend-приложение – собственную систему аутентификации и авторизации.  
Приложение не должно быть полностью основано на соответствующих фреймворках, идущих «из коробки».
Аутентификация и авторизация должны быть реализованы с использованием Middleware.

# Решение
В рамках выполнения задания создан сервис реализующий аутентификацию на основе JVT токенов и ролевая модель доступа (Role-Based Access Control) для авторизации.
Сервис состоит из набора моделей, middleware для аутентификации и авторизации, служебных функций и правил определения доступа для всех API-эндпоинтов проекта.

## Основные сущности:

### Role — роль пользователя
Определяет набор разрешений.
Примеры ролей: admin, manager, user, guest  
Каждый пользователь связан с одной ролью.

### BusinessElement — бизнес-элемент
Логический модуль или сущность приложения, к которой нужно разграничить доступ.
Примеры элементов: users, products, orders, shops 

### PermissionRule — правило доступа
Связывает роль и бизнес-элемент, определяя, права для внутри этого элемента.

Права:  
read_permission — читать свои  
read_all_permission — читать любые  
create_permission — создавать  
update_permission — редактировать свои  
update_all_permission — редактировать любые
delete_all_permission — удалять любые

Связь с пользователем реализована через ссылку на роль.
Пользователь содержит ссылку на роль:


### Сервис позволяет:
- создавать и удалять пользователей, выполнять логин и лог аут, обновлять токен
- создавать, просматривать, редактировать и удалять роли, бизнес-элементы и правила доступа
- менять роль пользователя


### JWT User Middleware
Этот middleware автоматически извлекает и проверяет JWT-токен из заголовка Authorization каждого запроса.  
Особенности реализации:
- игнорирует запросы без Authorization или с неверным форматом
- проверяет токен по базе заблокированных токенов (BlacklistedToken)
- декодирует JWT через HS256 и SECRET_KEY проекта
- сохраняет в запросе вспомогательные атрибуты: request._jwt_user, request._jwt_token
- не вызывает ошибок при невалидных токенах – просто пропускает как неавторизованного пользователя
- пишет лог

### RBAC Middleware
RBAC Middleware автоматически проверяет права для всех API-запросов, основанных на DRF ViewSet.  
Особенности реализации:
- автоматически определяет действие (read, create, update, delete) по HTTP-методу
- определяет ViewSet, в котором установлено поле element_name
- для операций с конкретным объектом пытается получить owner
- поддерживает свои/чужие объекты
- пропускает публичные пути (/auth/, /admin/, документацию)
- пишет лог

Если доступ запрещён → возвращает 403 Permission denied

#### Использование в ViewSet’ах
Каждый ViewSet задаёт свой бизнес-элемент через поле element_name:
```
class ProductViewSet(ModelViewSet):
    element_name = "products"
```
При создании метода list следует использовать фильтрацию по владельцу если у роли нет права на чтение всех объектов
```
class MockOrderViewSet(ViewSet):
    element_name = 'order'

    def list(self, request: Request):
        user = self.request._jwt_user
        qs = MOCK_ORDERS
        rule = user.get_rule('order')
        qs = filter_queryset_by_owner(qs, user, rule)

        return Response(
            [
                {
                    'id': obj.id,
                    'product_name': obj.product_name,
                    'quantity': obj.quantity,
                    'owner_id': obj.owner_id,
                }
                for obj in qs
            ]
        )
```

Список методов API можно посмотреть при запущенном сервисе по ссылке: http://127.0.0.1:8000/swagger/  
Для демонстрации в проекте реализован Mock сущности заказы и загружен набор тестовых данных.  
Доступ к данным можно получить через административный интерфейс: http://127.0.0.1:8000/admin/  
Пользователь: superuser@example.com, пароль: superuser123 (без роли)

Созданы следующие тестовые пользователи:  
- admin@example.com пароль: admin123 - имеет все права для всех бизнес-элементов. Может создавать, удалять, и назначать роли для пользователей.
- manager@example.com пароль: manager123
- user@example.com пароль: user123


## Установка и запуск
Клонируем репозиторий:
```
git clone https://github.com/alexfofanov/rbac-service.git
```
Переходим в папку проекта:
```
cd rbac-service
```
Создаём и при необходимости редактируем файл настройки проекта .env
```
cp .env.sample .env
```
Запуск сервиса: 
```
docker compose up --build
```
Остановка сервиса: 
```
docker compose down -v
```

## Примеры запросов к API:

### Регистрация пользователя:
```
curl --location 'http://127.0.0.1:8000/api/v1/auth/register/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "ivan@example.com",
    "first_name": "Иван",
    "last_name": "Петров",
    "password": "password"
}'
```

### Логин и получение токена:
```
curl --location 'http://127.0.0.1:8000/api/v1/auth/login/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "ivan@example.com",
    "password": "password"
}'
```

### Получение списка ролей:
```
curl --location 'http://127.0.0.1:8000/api/v1/rbac/roles/' \
--header 'Authorization: Bearer <JWT_ACCESS_TOKEN>'
```

### Задание роли пользователя:
```
curl --location --request PATCH 'http://127.0.0.1:8000/api/v1/users/5/update-role/' \
--header 'Authorization: Bearer <JWT_ACCESS_TOKEN>' \
--header 'Content-Type: application/json' \
--data '{
  "role_id": "2"
}'
```

### Создание правил доступа:
```
curl --location 'http://127.0.0.1:8000/api/v1/rbac/permission-rule/' \
--header 'Authorization: Bearer <JWT_ACCESS_TOKEN>' \
--header 'Content-Type: application/json' \
--data '{
  "role_id": 3,
  "element_id": 2,
  "read_permission": true,
  "read_all_permission": true,
  "create_permission": false,
  "update_permission": false,
  "update_all_permission": false,
  "delete_permission": false,
  "delete_all_permission": false,
}'
```