from fastapi import APIRouter, Form, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.security import authenticate_user

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/login")
async def login_page(request: Request):
    """Отображает страницу входа."""
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def login_user(
    username: str = Form(...),
    password: str = Form(...),
):
    """Проверяет учетные данные и устанавливает сессию."""
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    response = RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="current_user", value=username, httponly=True)
    return response

@router.get("/logout")
async def logout_user():
    """Выход пользователя и удаление данных о пользователе."""
    response = RedirectResponse(url="/auth/login", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key="current_user")
    return response