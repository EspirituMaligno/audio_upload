from fastapi.staticfiles import StaticFiles
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api import main_router

app = FastAPI(title="Audio Upload", docs_url="/docs")
app.mount("/static", StaticFiles(directory="static"), name="static")

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(main_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, log_level="info", reload=True)
