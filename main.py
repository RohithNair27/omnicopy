from datetime import datetime
from random import randint
from typing import Any
from fastapi import FastAPI, HTTPException,Depends
from sqlmodel import Field,Session, SQLModel, create_engine,select
from typing import Annotated
from contextlib import asynccontextmanager
from pydantic import BaseModel


class Campaign(SQLModel,table=True):
    campaign_id:int | None = Field(default=None, primary_key=True)
    name:str
    updated_date: datetime
    created_date: datetime

class CampaignCreate(SQLModel):
    name:str
    updated_date: datetime
    created_date: datetime
    


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False} #forcing py to use multiple threads
engine = create_engine(sqlite_url, connect_args=connect_args) #connect with DB


#create a session
def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

#create Database and tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app:FastAPI):
    create_db_and_tables()
    with Session(engine) as session:
        statement = select(Campaign)
        first_campaign = session.exec(statement).first()
        if not first_campaign:
            session.add_all([
                Campaign(name="summer launch",updated_date=datetime.now(),created_date=datetime.now()),
                Campaign(name="winter launch",updated_date=datetime.now(),created_date=datetime.now())
            ])
            session.commit()
   
    yield

class campaignReponse(BaseModel):
    Campaign:list[Campaign]



app = FastAPI(root_path="/api/v1",lifespan=lifespan)


@app.get("/")
def init():
    return {"data":"welcome"}

@app.get("/campaign")
def read_campaigns(session: SessionDep):
    #exec is usually used for multiple values
    data = session.exec(select(Campaign)).all()
    return {"campaigns":data}

@app.get("/campaign/{id}")
async def read_campaign(session:SessionDep,id:int):
    # get is used for single value
    data = session.get(Campaign, id)
    if not data:
        raise HTTPException(status_code=404)
    else:
        return {"campaign":data}

@app.post("/campaign",status_code=201)
async def create_campaign(body:CampaignCreate,session:SessionDep):
    db_campaign = Campaign.model_validate(body) 
    session.add(db_campaign)
    session.commit()
    session.refresh(db_campaign)
    return {"data":db_campaign}
    
@app.put("/campaign/{id}")
def update_campaign(id:int,body:CampaignCreate,session:SessionDep):
    data = session.get(Campaign, id)
    data.name = body.name
    session.commit()
    session.refresh(data)
    return {"data":data}


@app.delete("/campaign/{id}",status_code=204)
def delete_campaign(id:int,session:SessionDep):
    data = session.get(Campaign, id)
    if not data:
        raise HTTPException(status_code=404)
    else:
        session.delete(data)
        session.commit()
    return {"deleted":data}
        
