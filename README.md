# inter-1s-bitrix

Django-проект для двусторонней синхронизации данных между Bitrix и 1C.

Что уже есть:

- HTTP JSON интеграция в обе стороны: `Bitrix -> 1C` и `1C -> Bitrix`
- ручной запуск через веб-страницу `/`
- ручной запуск через management-команду
- журнал запусков в БД и в Django Admin

## Установка

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Docker

```bash
make build
make run
```

Приложение будет доступно на `http://127.0.0.1:8081/`.

## Настройка

Основные параметры лучше задавать через переменные окружения:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`
- `BITRIX_BASE_URL`
- `BITRIX_SOURCE_PATH`
- `BITRIX_TARGET_PATH`
- `BITRIX_AUTH_TOKEN`
- `ONEC_BASE_URL`
- `ONEC_INVOICE_LIST_PATH`
- `ONEC_TARGET_PATH`
- `ONEC_USERNAME`
- `ONEC_PASSWORD`

Пример:

```bash
export DJANGO_SECRET_KEY='change-me'
export BITRIX_BASE_URL='https://company.bitrix24.ru/rest'
export BITRIX_SOURCE_PATH='/crm/export'
export BITRIX_TARGET_PATH='/crm/import'
export BITRIX_AUTH_TOKEN='token'
export ONEC_BASE_URL='https://1c.local'
export ONEC_INVOICE_LIST_PATH='/ut/hs/bitrixintegration/invoice/list'
export ONEC_TARGET_PATH='/api/import'
export ONEC_USERNAME='user'
export ONEC_PASSWORD='password'
```

Ожидаемый контракт API:

- source endpoint возвращает JSON-массив объектов или объект вида `{"items": [...]}`
- target endpoint принимает `POST` с JSON-объектом

## Ручной запуск

Веб:

- откройте `http://127.0.0.1:8000/`
- сначала выберите действие `Получить список`
- задайте `date_from`, `date_to`, `inn`, если нужны фильтры
- после проверки списка переключите действие на `Запустить синхронизацию`

CLI:

```bash
python manage.py run_sync --direction both
python manage.py run_sync --direction 1c_to_bitrix --date-from 2026-01-01 --date-to 2026-01-31 --inn 7701234567
```

## Структура

- `sync_bridge/clients.py` - HTTP-клиенты
- `sync_bridge/services.py` - логика синхронизации
- `sync_bridge/models.py` - журнал запусков
- `sync_bridge/views.py` - ручной запуск через UI
