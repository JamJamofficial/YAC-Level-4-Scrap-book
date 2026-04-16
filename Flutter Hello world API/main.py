from fastapi import FastAPI

app = FastAPI()

count = 0

@app.get("/count")
def get_count():
    return {"count": count}

@app.post("/increment")
def increment():
    global count
    count += 1
    return {"count": count}