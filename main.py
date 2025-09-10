from datetime import datetime
from random import randint
from fastapi import FastAPI, HTTPException, Response
from typing import Any

app = FastAPI(root_path="/api/v1")

@app.get("/")
async def root():
    return{'message': 'Hello World'}


data : Any = [
    {
     "campaign_id": 1, 
     "name": "Summer Lunch", 
     "due_date": "2025-09-14", 
     "created_at": datetime.now()
    },
    {
     "campaign_id": 2, 
     "name": "Summer Lunch", 
     "due_date": "2025-10-23", 
     "created_at": datetime.now()
    },
    {
     "campaign_id": 3, 
     "name": "Baby Products", 
     "due_date": "2025-12-21", 
     "created_at": datetime.now()
    }
]

"""
Campaigns
- campaign_id (int, primary key)
- name (str)
- due_date (date)
- created_at (datetime)
"""

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

