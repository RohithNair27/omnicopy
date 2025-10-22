from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List,Annotated
from model import Campaign, CampaignCreate, CampaignResponse

from database import get_session 


router = APIRouter(
    prefix="/campaign"
)

SessionDep = Annotated[Session, Depends(get_session)]


@router.get("/")
def read_campaigns(session: SessionDep):
    #exec is usually used for multiple values
    data = session.exec(select(Campaign)).all()
    return {"campaigns":data}

@router.get("/{id}")
async def read_campaign(session:SessionDep,id:int):
    # get is used for single value
    data = session.get(Campaign, id)
    if not data:
        raise HTTPException(status_code=404)
    else:
        return {"campaign":data}

@router.post("/",status_code=201)
async def create_campaign(body:CampaignCreate,session:SessionDep):
    db_campaign = Campaign.model_validate(body) 
    session.add(db_campaign)
    session.commit()
    session.refresh(db_campaign)
    return {"data":db_campaign}
    
@router.put("/{id}")
def update_campaign(id:int,body:CampaignCreate,session:SessionDep):
    data = session.get(Campaign, id)
    data.name = body.name
    session.commit()
    session.refresh(data)
    return {"data":data}


@router.delete("/{id}",status_code=204)
def delete_campaign(id:int,session:SessionDep):
    data = session.get(Campaign, id)
    if not data:
        raise HTTPException(status_code=404)
    else:
        session.delete(data)
        session.commit()
    return {"deleted":data}