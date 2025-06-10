# backend/app/api/v1/api.py
from fastapi import APIRouter
from .endpoints import health # Example: import your endpoint routers
# Import other endpoint routers here as they are created
# from .endpoints import items
# from .endpoints import users

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
# api_router.include_router(items.router, prefix="/items", tags=["items"])
# api_router.include_router(users.router, prefix="/users", tags=["users"])
# Add other routers here
