#!/bin/bash
# Startup script for Render deployment

# Create database tables
python3 -c "
from database import create_tables
from models.user import User, UserRole, UserStatus
from auth import get_password_hash
from database import SessionLocal

print('Creating database tables...')
create_tables()

print('Creating admin user...')
db = SessionLocal()
try:
    admin = db.query(User).filter(User.email == 'admin@juridence.com').first()
    if not admin:
        hashed_password = get_password_hash('admin123')
        admin_user = User(
            email='admin@juridence.com',
            first_name='Admin',
            last_name='User',
            hashed_password=hashed_password,
            role=UserRole.ADMIN,
            status=UserStatus.ACTIVE,
            is_admin=True,
            is_verified=True
        )
        db.add(admin_user)
        db.commit()
        print('Admin user created successfully!')
    else:
        print('Admin user already exists')
except Exception as e:
    print(f'Error creating admin user: {e}')
finally:
    db.close()

print('Starting server...')
"

# Start the FastAPI server
exec uvicorn main:app --host 0.0.0.0 --port $PORT
