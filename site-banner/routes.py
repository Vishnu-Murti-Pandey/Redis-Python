import json
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, Field, SQLModel, select
from typing import Optional
from pydantic import BaseModel
from uuid import uuid4, UUID
from datetime import datetime, timezone

from config_redis import redis_client
from config_db import get_session
from config import REDIS_BANNER_KEY


def _uuid() -> str:
    return str(uuid4())

def _now() -> datetime:
    return datetime.now(timezone.utc)


# Banner Model
class Banner(SQLModel, table=True): 
    __tablename__ = "banner"
    
    id: UUID = Field(default_factory=_uuid, primary_key=True)
    banner_title: Optional[str] = Field(default="Welcome to site-banner app!")
    created_at: datetime = Field(default_factory=_now, nullable=False)
    
    
# Request Schema
class POSTBannerRequest(BaseModel):
    banner_title: str

# Response Schema
class POSTBannerResponse(BaseModel):
    message: str
    
class GETBannerResponse(BaseModel):
    served_from: str
    banner_title: str
    
    

banner_router = APIRouter(prefix='/api', tags=["Banner"])

@banner_router.post('/banner', response_model=POSTBannerResponse)
def bannerMessage(request: POSTBannerRequest, session: Session = Depends(get_session)):
    banner_title = request.banner_title
    
    banner = Banner(banner_title=banner_title)
    
    session.add(banner)
    session.commit()
    session.refresh(banner)
    
    return POSTBannerResponse(message="Banner Created!")
    
@banner_router.get('/banner', response_model=GETBannerResponse)
def bannerMessage(id: str, session: Session = Depends(get_session)):
    
    banner_from_cache = redis_client.get(f"{REDIS_BANNER_KEY}:{id}")
    if banner_from_cache:
        banner_data = json.loads(banner_from_cache)
        return GETBannerResponse(banner_title=banner_data["banner_title"], served_from="redis")
        
    banner = session.get(Banner, id)
    
    if not banner:  
        raise HTTPException(status_code=404, detail=f"Banner not found!")
    
    banner_dump = {
        "id": str(banner.id),
        "banner_title": banner.banner_title,
        "created_at": banner.created_at.isoformat()
    }
    
    redis_client.set(f"{REDIS_BANNER_KEY}:{id}", json.dumps(banner_dump), ex=120)
        
    return GETBannerResponse(banner_title=banner.banner_title, served_from="database")
        