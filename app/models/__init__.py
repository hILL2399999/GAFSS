from sqlalchemy import create_engine, Column, String, Float, DateTime, ForeignKey, Integer, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import logging
from app.config import DATABASE_URL

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Настройка подключения к базе данных
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Модель заказа (Order)
class Order(Base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True, index=True)  # Уникальный идентификатор заказа
    client_order_id = Column(String, index=True)       # Идентификатор клиента
    amount = Column(Float, nullable=False)             # Сумма заказа
    status = Column(String, nullable=False)            # Статус заказа (например, Pending, Completed)
    customer_name = Column(String, nullable=False)     # Имя клиента
    order_side = Column(String, nullable=False)        # Тип заказа (например, Buy или Sell)
    payment_method = Column(String, nullable=False)    # Метод оплаты
    created_at = Column(DateTime, default=datetime.utcnow)  # Дата создания заказа

# Модель диспута (Dispute)
class Dispute(Base):
    __tablename__ = "disputes"

    id = Column(String, primary_key=True, index=True)          # Уникальный идентификатор диспута
    order_id = Column(String, ForeignKey("orders.id"), nullable=False)  # Связанный заказ
    reason = Column(String, nullable=False)                    # Причина диспута
    status = Column(String, default="Open")                    # Статус диспута
    created_at = Column(DateTime, default=datetime.utcnow)      # Дата создания диспута

# Модель пользователя (User)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)         # Уникальный идентификатор пользователя
    username = Column(String, unique=True, nullable=False)     # Имя пользователя
    hashed_password = Column(String, nullable=False)           # Хэшированный пароль
    is_active = Column(Boolean, default=True)                  # Активность пользователя
    created_at = Column(DateTime, default=datetime.utcnow)     # Дата создания

# Создание таблиц
try:
    logger.debug("Создание таблиц базы данных...")
    Base.metadata.create_all(bind=engine)
    logger.debug("Таблицы созданы успешно.")
except Exception as e:
    logger.error(f"Ошибка при создании таблиц: {e}")