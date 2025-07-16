from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "ok", "message": "SupportTool API running"}

if __name__ == "__main__":
    uvicorn.run("mock_supporttool:app", host="0.0.0.0", port=60000)
