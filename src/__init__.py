from fastapi import FastAPI
from src.books.routes import book_router
from src.auth.routes import auth_router
from contextlib import asynccontextmanager
from src.db.main import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"Server is starting...")
    await init_db()
    yield
    print(f"Server is stopped")

version = 'v1'

app = FastAPI(
    title='Bookly',
    version=version,
    lifespan= lifespan
)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=['books'])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=['auth'])