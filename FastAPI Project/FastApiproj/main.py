from fastapi import FastAPI 

app = FastAPI()

@app.get("/")
async def root():


    return {"message": "Hello World"} 

@app.post("/")
async def create_root():


    return {"message": "Hello World"} 