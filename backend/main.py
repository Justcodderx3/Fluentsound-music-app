from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
#import os
from pathlib import Path
from sqlalchemy.orm import Session
from database import TrackDB, get_db, Base, engine

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


class TrackResponse(BaseModel):
    id: int
    track_name: str
    artist_name: Optional[str] = None


@app.get("/tracks", response_model=list[TrackResponse])
def all_added_tracks_return(db: Session = Depends(get_db)):
    tracks = db.query(TrackDB).all()
    return tracks


# @app.post("/tracks/")
# async def create_track():
#     pass


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='127.0.0.1', port=8000, )
