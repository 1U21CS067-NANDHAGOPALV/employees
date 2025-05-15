from fastapi import FastAPI
from app.database import Base, engine
from app.routers.user import router as user_router  
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include the employee router with a specific prefix
app.include_router(user_router, prefix="/employee", tags=["Employees"])