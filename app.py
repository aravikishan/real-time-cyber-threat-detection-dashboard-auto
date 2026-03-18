
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
import uvicorn

app = FastAPI()

# Database setup
DATABASE_URL = "sqlite:///./cyber_threats.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class Threat(Base):
    __tablename__ = "threats"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    severity = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(String)

class AnalyticsData(Base):
    __tablename__ = "analytics"
    id = Column(Integer, primary_key=True, index=True)
    metric = Column(String)
    value = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)

# Seed data
def seed_data(db: Session):
    if not db.query(Threat).first():
        db.add(Threat(description="SQL Injection Attempt", severity="High"))
        db.add(Threat(description="DDoS Attack", severity="Critical"))
        db.commit()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Routes
@app.get("/", response_class=HTMLResponse)
async def read_dashboard():
    with open("templates/index.html") as f:
        return HTMLResponse(content=f.read())

@app.get("/threats", response_class=HTMLResponse)
async def read_threats():
    with open("templates/threats.html") as f:
        return HTMLResponse(content=f.read())

@app.get("/analytics", response_class=HTMLResponse)
async def read_analytics():
    with open("templates/analytics.html") as f:
        return HTMLResponse(content=f.read())

@app.get("/settings", response_class=HTMLResponse)
async def read_settings():
    with open("templates/settings.html") as f:
        return HTMLResponse(content=f.read())

@app.get("/api/threats")
async def get_threats(db: Session = Depends(get_db)):
    threats = db.query(Threat).all()
    return threats

@app.post("/api/threats")
async def create_threat(description: str, severity: str, db: Session = Depends(get_db)):
    threat = Threat(description=description, severity=severity)
    db.add(threat)
    db.commit()
    db.refresh(threat)
    return threat

@app.get("/api/analytics")
async def get_analytics(db: Session = Depends(get_db)):
    analytics_data = db.query(AnalyticsData).all()
    return analytics_data

@app.get("/api/user/settings")
async def get_user_settings():
    return {"settings": "User settings data"}

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
