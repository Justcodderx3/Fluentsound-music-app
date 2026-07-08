# Fluentsound-music-app (WIP)
## Description <br>
<u>Fluentsound</u> - A backend REST API for uploading, streaming, and downloading music tracks.<br>

A personal project built to <u>explore</u> FastAPI and <u>practice</u> Backend development. <br>

## Features
- JWT authentication (registration, login, password hashing with bcrypt)
- Track upload with file storage
- Streaming with HTTP Range support
- Track download
- Full CRUD for tracks, with ownership protection

## Technology stack
**Python**: 3.9 <br>
**Framework**: FastAPI <br>
**Database**: SQLlite with **ORM** SQLAlchemy <br>
**Auth**: JWT (python-jose) + passlib/bcrypt <br>
**Frontend**: KivyMD

## API Endpoints

| Method | Endpoint | Description | Auth required |
|--------|----------|--------------|----------------|
| POST | `/users` | Register a new user | No |
| POST | `/users/login` | Login, returns JWT token | No |
| GET | `/profile` | Get current user info | Yes |
| GET | `/tracks` | List all tracks | No |
| POST | `/tracks/upload` | Upload a track file | Yes |
| GET | `/tracks/{id}` | Get a specific track | Yes |
| PUT | `/tracks/{id}` | Update a track | Yes (owner only) |
| DELETE | `/tracks/{id}` | Delete a track | Yes (owner only) |
| GET | `/tracks/{id}/download` | Download a track | No |
| GET | `/tracks/{id}/stream` | Stream a track | No |

## Getting Started

### Prerequisites
- Python 3.9+

### Installation
```bash
git clone https://github.com/Justcodderx3/Fluentsound-music-app.git
cd Fluentsound-music-app/backend
pip install -r requirements.txt
```

### Environment setup
Create a `.env` file in the `backend` folder:
```
SECRET_KEY=your_secret_key_here
```

Generate one with:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Run
```bash
python main.py
```

API docs available at `http://127.0.0.1:8000/docs`