from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from routers import v1_router

app = FastAPI()
app.include_router(v1_router)

@app.get("/")
async def root():
    return {"Hello, ": "World!"}