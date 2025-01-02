from fastapi.testclient import TestClient
from main import app
from app.models import Base, engine, SessionLocal, Order

# Создаём клиент для тестов
client = TestClient(app)

# Создаём тестовую базу данных
Base.metadata.create_all(bind=engine)

# Функция для очистки базы данных после каждого теста
def clear_db():
    db = SessionLocal()
    try:
        db.query(Order).delete()
        db.commit()
    finally:
        db.close()

def test_create_order():
    clear_db()
    response = client.post("/orders/create", data={
        "client_order_id": "12345",
        "order_side": "Buy",
        "amount": 1000,
        "customer_name": "Иван Иванов",
        "payment_method": "СБП"
    })
    assert response.status_code == 303  # Ожидается редирект
    assert "/orders" in response.headers["location"]

def test_list_orders():
    clear_db()
    # Создаём тестовые заказы
    client.post("/orders/create", data={
        "client_order_id": "12345",
        "order_side": "Buy",
        "amount": 1000,
        "customer_name": "Иван Иванов",
        "payment_method": "СБП"
    })
    client.post("/orders/create", data={
        "client_order_id": "12346",
        "order_side": "Sell",
        "amount": 2000,
        "customer_name": "Петр Петров",
        "payment_method": "Любой банк"
    })

    response = client.get("/orders/")
    assert response.status_code == 200
    assert "Иван Иванов" in response.text
    assert "Петр Петров" in response.text

def test_filter_orders_by_payment_method():
    clear_db()
    client.post("/orders/create", data={
        "client_order_id": "12345",
        "order_side": "Buy",
        "amount": 1000,
        "customer_name": "Иван Иванов",
        "payment_method": "СБП"
    })
    client.post("/orders/create", data={
        "client_order_id": "12346",
        "order_side": "Sell",
        "amount": 2000,
        "customer_name": "Петр Петров",
        "payment_method": "Любой банк"
    })

    response = client.get("/orders/?payment_method=СБП")
    assert response.status_code == 200
    assert "Иван Иванов" in response.text
    assert "Петр Петров" not in response.text

def test_create_order_missing_field():
    clear_db()
    response = client.post("/orders/create", data={
        "client_order_id": "12345",
        "order_side": "Buy",
        "amount": 1000,
        # "customer_name" is missing
        "payment_method": "СБП"
    })
    assert response.status_code == 422  # Ошибка валидации