from fastapi import FastAPI, Form
from pydantic import BaseModel
app = FastAPI()


class Data(BaseModel):
    status: str
    timestamp: str
    ipv4: str
    ipv6: str


data = Data()
data.status = "logout"
data.timestamp = ""
data.ipv4 = ""
data.ipv6 = ""


@app.get("/info")
async def root():
    if data.status == "":
        data.status = "logout"
    return data


# 接受body为json格式的数据
@app.post("/")
async def post_heartbeat(param: Data):
    data.status = param.status
    data.timestamp = param.timestamp
    data.ipv4 = param.ipv4
    data.ipv6 = param.ipv6
    print(data)
    return {"status": "success"}
