from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.apis.users.router import router as users_router
from app.apis.auth.router import router as auth_router
from app.apis.feeds.router import router as feeds_router


swagger_params = {
    "persistAuthorization": True
}

app = FastAPI(
    swagger_ui_parameters=swagger_params
)

@app.get("/")
async def read_root():
    return HTMLResponse("Hello world")

app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(feeds_router, prefix="/feeds", tags=["Feeds"])

