#!/usr/bin/env python3
"""
Script to create an admin user for Sumātosensā in Docker environment.
Run this script inside the Docker container to create the initial admin user.
"""

import asyncio
import sys
import os
from getpass import getpass

# Add the app directory to the Python path
sys.path.insert(0, '/app')

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import AsyncSessionLocal
from app.models import User
from app.auth import get_password_hash

async def create_admin_user():
    """Create an admin user interactively."""
    print("=== Sumātosensā Admin User Creation (Docker) ===")
    
    # Use environment variables or prompt for input
    username = os.getenv('ADMIN_USERNAME') or input("Enter admin username: ").strip()
    if not username:
        print("Username cannot be empty.")
        return False
    
    email = os.getenv('ADMIN_EMAIL') or input("Enter admin email: ").strip()
    if not email:
        print("Email cannot be empty.")
        return False
    
    password = os.getenv('ADMIN_PASSWORD')
    if not password:
        password = getpass("Enter admin password: ")
        if not password:
            print("Password cannot be empty.")
            return False
        
        confirm_password = getpass("Confirm admin password: ")
        if password != confirm_password:
            print("Passwords do not match.")
            return False
    
    try:
        async with AsyncSessionLocal() as db:
            # Check if user already exists
            result = await db.execute(select(User).where(User.username == username))
            if result.scalar_one_or_none():
                print(f"User '{username}' already exists.")
                return False
            
            # Check if email already exists
            result = await db.execute(select(User).where(User.email == email))
            if result.scalar_one_or_none():
                print(f"Email '{email}' already exists.")
                return False
            
            # Create admin user
            hashed_password = get_password_hash(password)
            admin_user = User(
                username=username,
                email=email,
                password_hash=hashed_password,
                role="admin",
                is_active=True
            )
            
            db.add(admin_user)
            await db.commit()
            
            print(f"Admin user '{username}' created successfully!")
            return True
            
    except Exception as e:
        print(f"Error creating admin user: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(create_admin_user())
    sys.exit(0 if success else 1)