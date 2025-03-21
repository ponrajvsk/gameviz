from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.cricket import router as cricket_router

# FastAPI app
app = FastAPI()
app.include_router(cricket_router, prefix="/cricket", tags=["Cricket"])

# Enable CORS (Allow frontend to call the API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow requests from React app
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)
