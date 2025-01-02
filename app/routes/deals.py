from fastapi import APIRouter, Request, Depends, Query, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models import SessionLocal, Order
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

@router.get("/")
async def show_deals(
    request: Request,
    db: Session = Depends(get_db),
    id: str = Query(None),
    client_order_id: str = Query(None),
    amount: float = Query(None),
    status: str = Query(None),
    customer_name: str = Query(None),
    order_side: str = Query(None),
    payment_method: str = Query(None),
    created_at: str = Query(None),
):
    """
    Отображение списка сделок с возможностью фильтрации.
    """
    try:
        logger.debug("Получение сделок с фильтрацией")

        # Сбор фильтров
        filters = []
        if id:
            filters.append(Order.id.ilike(f"%{id}%"))
        if client_order_id:
            filters.append(Order.client_order_id.ilike(f"%{client_order_id}%"))
        if amount is not None:
            filters.append(Order.amount == amount)
        if status:
            filters.append(Order.status.ilike(f"%{status}%"))
        if customer_name:
            filters.append(Order.customer_name.ilike(f"%{customer_name}%"))
        if order_side:
            filters.append(Order.order_side.ilike(f"%{order_side}%"))
        if payment_method:
            filters.append(Order.payment_method.ilike(f"%{payment_method}%"))
        if created_at:
            filters.append(Order.created_at.ilike(f"%{created_at}%"))

        # Запрос с фильтрами
        if filters:
            deals = db.query(Order).filter(or_(*filters)).all()
        else:
            deals = db.query(Order).all()

        logger.info(f"Всего сделок найдено: {len(deals)}")
        return templates.TemplateResponse("deals.html", {"request": request, "deals": deals})

    except Exception as e:
        logger.error(f"Ошибка при получении сделок: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при загрузке списка сделок")