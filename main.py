from fastapi import FastAPI, Request
app = FastAPI()

@app.post("/summarize")
async def summarize(info : Request):
    req_info = await info.json()
    # token = req.headers["Authorization"]
    return {
        "status" : "SUCCESS",
        "data" : req_info,
        # "token": token
    }