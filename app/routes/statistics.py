from fastapi import APIRouter, Depends, Request, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from fastapi.templating import Jinja2Templates
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
async def get_statistics(
    request: Request,
    db: Session = Depends(get_db),
    payment_method: str = Query(None),
):
    """
    Эндпоинт для получения статистики.
    Включает фильтрацию по методу оплаты.
    """
    try:
        logger.debug(f"Запрос статистики для метода оплаты: {payment_method or 'Все методы'}")

        # Общая статистика
        total_orders = db.query(Order).count()
        total_completed_orders = db.query(Order).filter(Order.status == "Completed").count()

        # Фильтрация по методу оплаты
        if payment_method:
            filtered_orders = db.query(Order).filter(Order.payment_method == payment_method)
            total_amount = sum(order.amount for order in filtered_orders)
            filtered_orders_count = filtered_orders.count()
        else:
            total_amount = db.query(func.sum(Order.amount)).scalar() or 0
            filtered_orders_count = total_orders

        logger.info("Статистика успешно загружена")

        return templates.TemplateResponse(
            "statistics.html",
            {
                "request": request,
                "stats": {
                    "total_orders": total_orders,
                    "total_completed_orders": total_completed_orders,
                    "total_amount": total_amount,
                    "filtered_payment_method": payment_method or "Все методы",
                    "filtered_orders_count": filtered_orders_count,
                },
            },
        )

    except Exception as e:
        logger.error(f"Ошибка при загрузке статистики: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при загрузке статистики")