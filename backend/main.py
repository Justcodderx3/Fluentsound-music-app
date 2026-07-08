from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from pathlib import Path
from sqlalchemy.orm import Session
from database import TrackDB, get_db, Base, engine, UserDB
from random import randint
from sqlalchemy import and_
from passlib.context import CryptContext
from auth import create_access_token, get_current_user
from fastapi.security import OAuth2PasswordRequestForm

pwd_context = CryptContext(schemes=['bcrypt'])
app = FastAPI(
    title="FluentSound",
    version="0.0.0",
    description="Offline music player for android",
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
            raise ValueError(f"Unsupported file format:{v.suffix}")
        return v


class UserCreate(BaseModel):
    username: str = Field(..., min_length=4, max_length=25)
    password: str = Field(..., min_length=8, max_length=100)


class User(BaseModel):
    username: Optional[str] = Field(f'user{randint(999999, 10000000)}', min_length=4, max_length=25)
    description: Optional[str] = Field(None, min_length=1, max_length=350)
    add_date: datetime = Field(default_factory=datetime.now)


class TrackResponse(BaseModel):
    id: int
    track_name: str
    artist_name: Optional[str] = None


class TrackCreate(BaseModel):
    track_name: str
    artist_name: Optional[str] = None
    file_path: Path

    @field_validator("file_path")
    def validate_track_path(cls, v: Path):
        track_extensions = {".mp3", ".m4a", ".ogg", ".flac"}
        if v.suffix.lower() not in track_extensions:
            raise ValueError(f"Unsupported file format:{v.suffix}")
        return v


@app.get("/tracks", response_model=list[TrackResponse])
def all_added_tracks_return(db: Session = Depends(get_db)):
    tracks = db.query(TrackDB).all()
    return tracks


@app.post('/users')
async def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    if db.query(UserDB).filter(UserDB.username == user_data.username).first():
        raise HTTPException(status_code=400, detail=f'Username already taken')
    hashed_password = pwd_context.hash(user_data.password)
    db_users = UserDB(
        username=user_data.username,
        password=hashed_password
    )
    db.add(db_users)
    db.commit()
    db.refresh(db_users)
    return {'message': f'User created successfully'}


@app.post('/users/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code=401, detail=f'User not found')
    verify_password = pwd_context.verify(form_data.password, user.password)
    if not verify_password:
        raise HTTPException(status_code=401, detail=f'Uncorrect password')
    token = create_access_token({'user_id': user.id, 'username': user.username})
    return {'access_token': token, 'token_type': 'bearer'}


@app.get("/profile")
async def read_profile(current_user: dict = Depends(get_current_user)):
    return current_user


@app.get("/tracks/{track_id}")
async def get_current_track(track_id: int, db: Session = Depends(get_db),
                            current_user: dict = Depends(get_current_user)):
    user_id = current_user['user_id']
    track_data = db.query(TrackDB).filter(and_(TrackDB.id == track_id, TrackDB.user_id == user_id)).first()
    if not track_data:
        raise HTTPException(status_code=404, detail='Track not found')
    return {"id": track_data.id, "track_name": track_data.track_name, "artist_name": track_data.artist_name}


@app.post('/tracks', response_model=TrackResponse)
async def create_track(track_data: TrackCreate, db: Session = Depends(get_db),
                       current_user: dict = Depends(get_current_user)):
    db_track = TrackDB(
        track_name=track_data.track_name,
        artist_name=track_data.artist_name,
        file_path=str(track_data.file_path),
        file_format=track_data.file_path.suffix[1:],
        user_id=current_user['user_id']
    )
    db.add(db_track)
    db.commit()
    db.refresh(db_track)

    return {'id': db_track.id,
            'track_name': db_track.track_name,
            'artist_name': db_track.artist_name
            }


@app.put('/tracks/{track_id}', response_model=TrackUpdate)
async def track_update(track_id: int, update_data: TrackUpdate, db: Session = Depends(get_db),
                       current_user: dict = Depends(get_current_user)):
    track = db.query(TrackDB).filter(and_(TrackDB.id == track_id, TrackDB.user_id == current_user['user_id'])).first()
    if not track:
        raise HTTPException(status_code=404, detail='Track not found')
    update_dict = update_data.dict(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(track, field, value)

    db.commit()
    db.refresh(track)
    return {'id': track.id, 'track_name': track.track_name, 'artist_name': track.artist_name}


@app.delete('/tracks/{track_id}')
async def delete_track(track_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    track = db.query(TrackDB).filter(and_(TrackDB.id == track_id, TrackDB.user_id == current_user['user_id'])).first()
    if not track:
        raise HTTPException(status_code=404, detail='Track not found')

    deleted_track_id = track.id
    deleted_track_name = track.track_name

    db.delete(track)
    db.commit()
    return {'message': 'Track successfuly deleted', 'id': deleted_track_id, 'track_name': deleted_track_name}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='127.0.0.1', port=8000, )
