from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "FastAPI with Docker Compose pushed from local 🚀"}

@app.get("/health")
def health():
    return {"status": "healthy pushed from local"}
