import asyncio
from passlib.context import CryptContext
from models.database import engine, AsyncSessionLocal
from models.orm_models import User

# This tool hashes the password so it's not stored as plain text
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def seed_admin():
    async with AsyncSessionLocal() as session:
        # 1. Hash the password 'admin123'
        hashed_pw = pwd_context.hash("admin123")
        
        # 2. Prepare the user object
        new_user = User(
            name="Test Admin",
            email="admin@example.com",
            hashed_password=hashed_pw,
            role="executive"
        )
        
        # 3. Save to PostgreSQL
        session.add(new_user)
        await session.commit()
    print("✅ Success! You can now login with:")
    print("Email: admin@example.com")
    print("Password: admin123")

if __name__ == "__main__":
    asyncio.run(seed_admin())