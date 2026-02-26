from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
from src.routes import router
from src.helper.handler import BaseAppException
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from settings import settings

app = FastAPI()

origins = [
    "http://localhost:5173",   
    "http://127.0.0.1:5173",
    "http://192.168.160.225:3000",
    "machine-mgt.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # URLs allowed to access API
    allow_credentials=True,
    allow_methods=["*"],          # GET, POST, PUT, DELETE...
    allow_headers=["*"],          # Allow all headers
)

app.include_router(router, prefix="/api")

def run():
    uvicorn.run("main:app",host="0.0.0.0",port=settings.PORT)

@app.exception_handler(BaseAppException)
async def base_app_exception_handler(
    request: Request, exc: BaseAppException
):
    print(exc.payload)
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "code": exc.code,
            "message": exc.message,
            "payload": exc.payload,
        },
    )

if __name__== "__main__":
    run()

