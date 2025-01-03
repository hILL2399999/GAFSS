from fastapi import FastAPI
from app.routes import users, admin, payments

app = FastAPI()

# Подключаем маршруты
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])
app.include_router(payments.router, prefix="/payments", tags=["Payments"])

@app.get("/")
def read_root():
    return {"message": "Welcome to PayGas!"}