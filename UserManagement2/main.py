from fastapi import FastAPI
import models

from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from settings import engine
from router import views1

app = FastAPI(title="UserManagement router",)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.add_middleware(GZipMiddleware)
models.Base.metadata.create_all(bind=engine)

app.include_router(views1.router)













