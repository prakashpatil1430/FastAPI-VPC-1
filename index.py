from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def fast_api():
    return {'wish': 'hello i am fastapi'}