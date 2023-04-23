from fastapi import FastAPI, Form

app = FastAPI()

data = {
    "status": "logout",
    "timestamp": "",
    "ipv4": "",
    "ipv6": "",
}


@app.get("/info")
async def root():
    return data


@app.get("/")
async def heartbeat(status: str = Form(), timestamp: str = Form(), ipv4: str = Form(), ipv6: str = Form()):
    print(status, timestamp, ipv4, ipv6)
    data["status"] = status
    data["timestamp"] = timestamp
    data["ipv4"] = ipv4
    data["ipv6"] = ipv6
    return {"message": "ok"}
