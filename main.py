from fastapi import FastAPI, Request
app = FastAPI()

@app.post("/get")
async def get(info : Request):
    req_info = await info.json()
    return {
        "status" : "SUCCESS",
        "data" : req_info
    }