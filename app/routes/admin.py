from fastapi import APIRouter, Depends, HTTPException, Request, Form
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.models import SessionLocal, Order, Dispute
from app.config import ADMIN_USERNAME, ADMIN_PASSWORD
import logging

# Настройка логирования
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
security = HTTPBasic()

# Функция для подключения к базе данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Функция проверки авторизации администратора
def admin_auth(credentials: HTTPBasicCredentials):
    if credentials.username != ADMIN_USERNAME or credentials.password != ADMIN_PASSWORD:
        logger.warning(f"Неудачная попытка авторизации: {credentials.username}")
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")

# Административная панель: главная страница
@router.get("/")
async def admin_dashboard(request: Request, credentials: HTTPBasicCredentials = Depends(security)):
    admin_auth(credentials)
    return templates.TemplateResponse("admin_dashboard.html", {"request": request})

# Управление заказами: список
@router.get("/orders")
async def admin_orders(request: Request, db: Session = Depends(get_db), credentials: HTTPBasicCredentials = Depends(security)):
    admin_auth(credentials)
    orders = db.query(Order).all()
    return templates.TemplateResponse("admin_orders.html", {"request": request, "orders": orders})

# Управление заказами: редактирование
@router.get("/orders/edit/{order_id}")
async def edit_order(request: Request, order_id: str, db: Session = Depends(get_db), credentials: HTTPBasicCredentials = Depends(security)):
    admin_auth(credentials)
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        logger.error(f"Заказ с ID {order_id} не найден")
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return templates.TemplateResponse("admin_edit_order.html", {"request": request, "order": order})

# Управление заказами: обновление
@router.post("/orders/edit/{order_id}")
async def update_order(
    order_id: str,
    client_order_id: str = Form(...),
    order_side: str = Form(...),
    amount: float = Form(...),
    status: str = Form(...),
    payment_method: str = Form(...),
    customer_name: str = Form(...),
    db: Session = Depends(get_db),
    credentials: HTTPBasicCredentials = Depends(security),
):
    admin_auth(credentials)
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        logger.error(f"Заказ с ID {order_id} не найден")
        raise HTTPException(status_code=404, detail="Заказ не найден")
    order.client_order_id = client_order_id
    order.order_side = order_side
    order.amount = amount
    order.status = status
    order.payment_method = payment_method
    order.customer_name = customer_name
    db.commit()
    logger.info(f"Заказ {order_id} обновлен")
    return RedirectResponse(url="/admin/orders", status_code=303)

# Управление заказами: удаление
@router.post("/orders/delete/{order_id}")
async def delete_order(order_id: str, db: Session = Depends(get_db), credentials: HTTPBasicCredentials = Depends(security)):
    admin_auth(credentials)
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        logger.error(f"Заказ с ID {order_id} не найден")
        raise HTTPException(status_code=404, detail="Заказ не найден")
    db.delete(order)
    db.commit()
    logger.info(f"Заказ {order_id} удален")
    return RedirectResponse(url="/admin/orders", status_code=303)