from contextlib import asynccontextmanager
from datetime import datetime, timezone
from random import randint
from fastapi import Depends, FastAPI, HTTPException, Response
from typing import Annotated, Any

from pydantic import BaseModel
from sqlmodel import Field, SQLModel, Session, create_engine, select

class Campaign(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    due_date: datetime | None = Field(default=None, index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=True, index=True)

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    
def get_session():
    with Session(engine) as session:
        yield session
        
SessionDep = Annotated[Session, Depends(get_session)]

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    with Session(engine) as session:
        if not session.exec(select(Campaign)).first():
            session.add_all([
                Campaign(name="Summer Lunch", due_date=datetime(2025, 9, 14)),
                Campaign(name="Summer Lunch", due_date=datetime(2025, 10, 23)),
                Campaign(name="Baby Products", due_date=datetime(2025, 12, 21))
            ])
            session.commit()     
    yield

app = FastAPI(root_path="/api/v1", lifespan=lifespan)

@app.get("/")
async def root():
    return{'message': 'Hello World'}

"""
Campaigns
- campaign_id (int, primary key)
- name (str)
- due_date (date)
- created_at (datetime)
"""

class CampaignsResponse(BaseModel):
    campaigns: list[Campaign]

@app.get("/campaigns", response_model=CampaignsResponse)
async def read_campaigns(session: SessionDep):
    data = session.exec(select(Campaign)).all()
    return {"campaigns": data}

'''
@app.get("/campaigns")
async def read_campaigns():
    return {"campaigns": data}

@app.get("/campaigns/{id}")
async def read_campaign(id: int):
    for campaign in data:
        if campaign.get("campaign_id") == id:
            return {"campaign": campaign}
    raise HTTPException(status_code=404, detail="Campaign not found")

@app.post("/campaigns", status_code=201)
async def create_campaign(body: dict[str, Any]):
    
    new : Any = {
        "campaign_id": randint(100, 1000),
        "name": body.get("name"),
        "due_date": body.get("due_date"),
        "created_at": datetime.now()  
    }
    
    data.append(new)
    return {"campaign": new}

@app.put("/campaigns/{id}")
async def update_campaign(id: int, body: dict[str, Any]):
    for index, campaign in enumerate(data):
        if campaign.get("campaign_id") == id:
            
            updated : Any = {
                "campaign_id": id,
                "name": body.get("name"),
                "due_date": body.get("due_date"),
                "created_at": campaign.get("created_at")  
            }
            
            data[index] = updated
            return {"campaign": updated}
    raise HTTPException(status_code=404, detail="Campaign not found")

@app.delete("/campaigns/{id}")
async def delete_campaign(id: int):
    
    for index, campaign in enumerate(data):
        if campaign.get("campaign_id") == id:
            
            data.pop(index)
            return Response(status_code=204)
    raise HTTPException(status_code=404, detail="Campaign not found")
'''

# data : Any = [
#     {
#      "campaign_id": 1, 
#      "name": "Summer Lunch", 
#      "due_date": "2025-09-14", 
#      "created_at": datetime.now()
#     },
#     {
#      "campaign_id": 2, 
#      "name": "Summer Lunch", 
#      "due_date": "2025-10-23", 
#      "created_at": datetime.now()
#     },
#     {
#      "campaign_id": 3, 
#      "name": "Baby Products", 
#      "due_date": "2025-12-21", 
#      "created_at": datetime.now()
#     }
# ]