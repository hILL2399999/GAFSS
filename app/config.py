"""
Файл конфигурации приложения.
Содержит настройки для подключения к API агрегатора и магазина.
"""

# Настройки API агрегатора
AGGREGATOR_API_KEY = "ваш_ключ_агрегатора"  # API ключ для агрегатора
AGGREGATOR_BASE_URL = "https://api.luckypay.com"  # Базовый URL для API агрегатора

# Настройки API магазина
STORE_API_KEY = "ваш_ключ_магазина"  # API ключ для магазина
STORE_BASE_URL = "https://api.store.com"  # Базовый URL для API магазина

# Настройки базы данных
DATABASE_URL = "sqlite:///./orders.db"  # Подключение к базе данных SQLite

# Логирование
LOGGING_LEVEL = "DEBUG"  # Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)

# Административные настройки
ADMIN_USERNAME = "admin"  # Логин администратора
ADMIN_PASSWORD = "password"  # Пароль администратора (рекомендуется заменить)

# Дополнительные настройки
DEFAULT_PAGE_SIZE = 10  # Количество записей на странице
ENABLE_FEATURE_X = True  # Включение или отключение определённых функций