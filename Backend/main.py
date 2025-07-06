from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from generate_signals import generate_latest_signals, get_accuracy_stats
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/latest-signals")
def latest_signals():
    signals = generate_latest_signals()
    accuracy = get_accuracy_stats()
    return {"signals": signals, "accuracy": accuracy}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
