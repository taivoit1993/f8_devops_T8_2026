from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from mangum import Mangum
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text

from database import get_db
import models
import schemas

app = FastAPI(
    title="F8 DevOps Assignment 0506 - Backend API",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {
        "status": "success",
        "message": "Welcome to Backend API! Access /docs for Swagger UI documentation."
    }

@app.get("/health/db", status_code=status.HTTP_200_OK)
async def check_db_connection(db: AsyncSession = Depends(get_db)):
    """Check if connection to the database is working properly."""
    try:
        result = await db.execute(text("SELECT 1 AS check, current_database() AS db_name, version() AS version"))
        row = result.mappings().one()
        return {
            "status": "success",
            "database": "connected",
            "current_database": row["db_name"],
            "db_version": row["version"],
            "message": "Database connection is healthy!"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "status": "error",
                "database": "disconnected",
                "message": f"Could not connect to database: {str(e)}"
            }
        )

@app.get("/posts", response_model=List[schemas.PostResponse], status_code=status.HTTP_200_OK)
async def get_all_posts(db: AsyncSession = Depends(get_db)):
    """Fetch all posts from the database ordered by id."""
    result = await db.execute(select(models.Post).order_by(models.Post.id.asc()))
    posts = result.scalars().all()
    return posts

@app.post("/posts", response_model=schemas.PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(post_in: schemas.PostCreate, db: AsyncSession = Depends(get_db)):
    """Create a new post."""
    post = models.Post(**post_in.model_dump())
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post

@app.get("/posts/{post_id}", response_model=schemas.PostResponse)
async def get_post_by_id(post_id: int, db: AsyncSession = Depends(get_db)):
    """Get single post by ID."""
    result = await db.execute(select(models.Post).where(models.Post.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found"
        )
    return post

FAKE_USERS = [
    {
        "id": 1,
        "name": "Nguyễn Văn A",
        "email": "nguyenvana@example.com",
        "role": "admin",
        "is_active": True,
    },
    {
        "id": 2,
        "name": "Trần Thị B",
        "email": "tranthib@example.com",
        "role": "user",
        "is_active": True,
    },
    {
        "id": 3,
        "name": "Lê Văn C",
        "email": "levanc@example.com",
        "role": "user",
        "is_active": False,
    },
    {
        "id": 4,
        "name": "Phạm Minh D",
        "email": "phamminhd@example.com",
        "role": "editor",
        "is_active": True,
    },
]

@app.get("/users", response_model=List[schemas.UserResponse], status_code=status.HTTP_200_OK)
def get_users():
    """Fetch fake list of users."""
    return FAKE_USERS

# AWS Lambda handler
handler = Mangum(app)


