from fastapi import APIRouter, HTTPException, Form, Depends, Request
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from app.models import SessionLocal, Order
from uuid import uuid4
import logging

# Настройка логирования
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Функция для подключения к базе данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/create")
async def show_create_order_form(request: Request):
    """
    Форма для создания нового заказа.
    """
    logger.debug("Открыта форма создания нового заказа")
    return templates.TemplateResponse("create_order.html", {"request": request})

@router.post("/create")
async def create_order(
    client_order_id: str = Form(...),
    order_side: str = Form(...),
    amount: float = Form(...),
    customer_name: str = Form(...),
    payment_method: str = Form(...),
    db: Session = Depends(get_db),
):
    """
    Создание нового заказа через форму.
    """
    try:
        logger.debug("Получены данные для создания заказа")
        new_order = Order(
            id=str(uuid4()),
            client_order_id=client_order_id,
            order_side=order_side,
            amount=amount,
            customer_name=customer_name,
            status="Pending",
            payment_method=payment_method,
        )
        db.add(new_order)
        db.commit()
        db.refresh(new_order)

        logger.info(f"Заказ создан: ID={new_order.id}")
        return RedirectResponse(url="/orders", status_code=303)

    except Exception as e:
        logger.error(f"Ошибка при создании заказа: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при создании заказа")

@router.get("/")
async def list_orders(request: Request, db: Session = Depends(get_db)):
    """
    Получить список всех заказов.
    """
    try:
        logger.debug("Получение списка заказов")
        orders = db.query(Order).all()
        logger.info(f"Найдено заказов: {len(orders)}")
        return templates.TemplateResponse("orders.html", {"request": request, "orders": orders})

    except Exception as e:
        logger.error(f"Ошибка при получении списка заказов: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при загрузке списка заказов")