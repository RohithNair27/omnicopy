from datetime import datetime
from random import randint
from typing import Any
from fastapi import FastAPI, HTTPException,Depends
from sqlmodel import Field,Session, SQLModel, create_engine,select
from typing import Annotated
from contextlib import asynccontextmanager
from pydantic import BaseModel

from database import create_db_and_tables,engine
from model import Campaign
from routers import campaigns


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


app = FastAPI(root_path="/api/v1",lifespan=lifespan)

app.include_router(campaigns.router)


