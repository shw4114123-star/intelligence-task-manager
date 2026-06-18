from fastapi import FastAPI
from database.db_connection import DBconnection
from routes.agent_routes import router as agent_router
from routes.mission_routes import router as mission_router
from routes.report_routes import router as report_router
import uvicorn


app = FastAPI()
connection = DBconnection()

@app.post("/")
def create_database_and_tables():
    connection.create_database()
    connection.create_tables()

app.include_router(agent_router)
app.include_router(mission_router)
app.include_router(report_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)