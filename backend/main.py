from fastapi import FastAPI, Depends, Header, HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
# import os
from pathlib import Path
from sqlalchemy.orm import Session
from database import TrackDB, get_db, Base, engine, fake_users_db
from random import randint
from sqlalchemy import and_

app = FastAPI(
    title="FluentSound",
    version="0.0.0",
    description="Оффлайн музыкальный плеер для андроид",
    docs_url="/docs",
    redoc_url="/redoc"
)


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


class TrackInfo(BaseModel):
    id: int = Field()
    add_date: datetime = Field(default_factory=datetime.now)


class TrackUpdate(BaseModel):
    artist_name: Optional[str] = Field(None, min_length=1, max_length=200)
    track_name: Optional[str] = Field(None, min_length=1, max_length=200)
    file_path: Path = Field(...)

    @field_validator("file_path")
    def validate_track_path(cls, v: Path):
        track_extensions = {".mp3", ".m4a", ".ogg", ".flac"}
        if v.suffix.lower() not in track_extensions:
            raise ValueError(f"Неподдерживаемый формат файла:{v.suffix}")
        return v


class User(BaseModel):
    username: Optional[str] = Field(f'user{randint(999999, 10000000)}', min_length=4, max_length=25)
    description: Optional[str] = Field(None, min_length=1, max_length=350)
    add_date: datetime = Field(default_factory=datetime.now)


class TrackResponse(BaseModel):
    id: int
    track_name: str
    artist_name: Optional[str] = None


@app.get("/tracks", response_model=list[TrackResponse])
def all_added_tracks_return(db: Session = Depends(get_db)):
    tracks = db.query(TrackDB).all()
    return tracks


async def get_current_user(x_api_key: str = Header(..., alias="X-API-Key")):
    user_data = fake_users_db.get(x_api_key)
    if not user_data:
        raise HTTPException(status_code=401, detail=f"User not found")
    return user_data


@app.get("/profile")
async def read_profile(curent_user: dict = Depends(get_current_user)):
    return curent_user


@app.get("/tracks/{track_id}")
async def get_current_track(track_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    user_id = current_user.get('user_id')
    if not user_id:
        raise HTTPException(status_code=401, detail='User ID not found in token')
    track_data = db.query(TrackDB).filter(and_(TrackDB.id == track_id, TrackDB.user_id == user_id)).first()
    if not track_data:
        raise HTTPException(status_code=404, detail='Track not found')
    return {"id": track_data.id, "track_name": track_data.track_name, "artist_name": track_data.artist_name}


# @app.post("/tracks/")
# async def create_track():


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='127.0.0.1', port=8000, )
