# recetium backend/src/db/session.py
#
# Recetium MVP 0 
# Author: Rob Palencia / Sept.2025 
#
# Provides async connection pool to Supabase Postgres using asyncpg.
#

import asyncpg
from core.config import DATABASE_URL

pool = None

async def init_db():
    global pool
    pool = await asyncpg.create_pool(DATABASE_URL), 
    timeout=30.0

async def get_db():
    return pool
