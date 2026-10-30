import asyncio
from sqlalchemy import select
from database import AsyncSessionLocal
from models import Post

SAMPLE_POSTS = [
    {
        "title": "Getting Started with FastAPI and Docker",
        "content": "FastAPI is a modern, fast web framework for building APIs with Python based on standard Python type hints.",
        "published": True,
    },
    {
        "title": "Database Migrations with Alembic",
        "content": "Alembic is a lightweight database migration tool for usage with the SQLAlchemy Database Toolkit for Python.",
        "published": True,
    },
    {
        "title": "Containerizing DevOps Applications",
        "content": "Docker containers wrap up software and its dependencies into a standardized unit for software development.",
        "published": True,
    },
    {
        "title": "CI/CD Pipeline Best Practices",
        "content": "Automating testing, linting, building, and deployment ensures fast and reliable software delivery.",
        "published": True,
    },
]

async def seed_data():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Post))
        existing_posts = result.scalars().all()
        
        if existing_posts:
            print(f"Database already contains {len(existing_posts)} post(s). Skipping seed.")
            return

        print("Seeding sample posts into the database...")
        for item in SAMPLE_POSTS:
            post = Post(**item)
            session.add(post)
        
        await session.commit()
        print(f"Successfully seeded {len(SAMPLE_POSTS)} posts!")

if __name__ == "__main__":
    asyncio.run(seed_data())
