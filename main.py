from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware


from database import Base, engine
from src.endpoints import user

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(user.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Server up"}
