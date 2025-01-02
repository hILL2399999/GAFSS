from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse, RedirectResponse

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def login_page():
    return """
    <html>
        <head><title>Login</title></head>
        <body>
            <form action="/login" method="post">
                <label>Username:</label><input type="text" name="username" />
                <label>Password:</label><input type="password" name="password" />
                <button type="submit">Login</button>
            </form>
        </body>
    </html>
    """

@router.post("/")
async def login(username: str = Form(...), password: str = Form(...)):
    if username == "admin" and password == "password":
        return RedirectResponse(url="/dashboard", status_code=302)
    return {"error": "Invalid credentials"}