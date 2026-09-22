from fastapi import FastAPI
from src.features.todos.router import router as todos_router


app = FastAPI(title="My First FastAPI Project: Todo App")
app.include_router(todos_router)

@app.get("/")
async def root():
    return {"message": "My First FastAPI Project: Todo App is running"}

