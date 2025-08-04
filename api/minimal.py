from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World", "status": "working"}

@app.get("/api/health")
def health():
    return {"status": "healthy"}

# This is required for Vercel
handler = app
