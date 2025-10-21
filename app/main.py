from fastapi import FastAPI

app = FastAPI(title="BTBee")

@app.get("/")
def read_root():
    return {"message": "Welcome to BTBee API 🚀"}
