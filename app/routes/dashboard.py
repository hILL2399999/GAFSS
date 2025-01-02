from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def get_dashboard():
    return """
    <html>
        <head><title>Dashboard</title></head>
        <body><h1>Welcome to the Dashboard!</h1></body>
    </html>
    """