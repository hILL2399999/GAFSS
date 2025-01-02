from fastapi import APIRouter, HTTPException, Depends, Request, Form
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from app.models import SessionLocal, Dispute, Order
import logging
from uuid import uuid4

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


@router.post("/create")
async def create_dispute(
        request: Request,
        order_id: str = Form(...),
        reason: str = Form(...),
        db: Session = Depends(get_db),
):
    """
    Создание нового диспута через форму.
    """
    try:
        logger.debug(f"Получены данные для диспута: order_id={order_id}, reason={reason}")

        # Проверка существования заказа
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            logger.error(f"Заказ с ID {order_id} не найден")
            raise HTTPException(status_code=404, detail="Заказ не найден")

        # Создание диспута
        new_dispute = Dispute(
            id=str(uuid4()),
            order_id=order_id,
            reason=reason,
            status="Open",
        )
        db.add(new_dispute)
        db.commit()
        db.refresh(new_dispute)

        logger.info(f"Диспут создан: ID={new_dispute.id}")
        return RedirectResponse(url="/disputes", status_code=303)

    except HTTPException as e:
        logger.error(f"Ошибка при создании диспута: {e.detail}")
        raise e
    except Exception as e:
        logger.exception("Ошибка при создании диспута")
        raise HTTPException(status_code=500, detail="Ошибка при создании диспута")


@router.get("/")
async def list_disputes(request: Request, db: Session = Depends(get_db)):
    """
    Получить список всех диспутов.
    """
    try:
        logger.debug("Получение списка диспутов")
        disputes = db.query(Dispute).all()
        logger.info(f"Найдено диспутов: {len(disputes)}")
        return templates.TemplateResponse("disputes.html", {"request": request, "disputes": disputes})

    except Exception as e:
        logger.error(f"Ошибка при получении списка диспутов: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при загрузке диспутов")