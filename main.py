from datetime import datetime
from random import randint
from typing import Any
from fastapi import FastAPI, HTTPException

app = FastAPI(root_path="/api/v1")

data = [
    {"campaign_id":1,
     "name":"summer sale",
     "Updated_date":datetime.now(),
     "created_date":datetime.now()
     },
    {"campaign_id":2,
     "name":"Black Friday",
     "Updated_date":datetime.now(),
     "created_date":datetime.now()
     }
]

@app.get("/")
def init():
    return {"data":"welcome"}

@app.get("/campaign")
def read_campaigns():
    return {"data":data}

@app.get("/campaign/{id}")
def read_campaign(id:int):
    for campaign in data:
        print(campaign.get("campaign_id")==id)
        if(campaign.get("campaign_id") == id):
            return {"data":campaign}
    raise HTTPException(status_code=404)

@app.post("/campaign")
async def create_campaign(body:dict[str,Any]):

    new = {
    "campaign_id":randint(0,100),
     "name":body.get("name"),
     "Updated_date":datetime.now(),
     "created_date":body.get("updated_date")
    }
    data.append(new)
    return {"new":new}

@app.put("/campaign/{id}")
def udpate_campaign(id:int,body:dict[str,Any]):
    # id = body.get("campaign_id")
    for index,campaign in enumerate(data):
        print(campaign.get("campaign_id")==id)
        if(campaign.get("campaign_id") == id):
            campaign["name"] = body.get("name")
            campaign["Updated_date"] = datetime.now()
            data[index] = campaign
            return campaign
    raise HTTPException(status_code=404)

@app.delete("/campaign/{id}",status_code=204)
def delete_campaign(id:int):
    # id = body.get("campaign_id")
    for index,campaign in enumerate(data):
        if(campaign.get("campaign_id") == id):
            data.pop(index)
            return {'Sucess'}
    raise HTTPException(status_code=404)