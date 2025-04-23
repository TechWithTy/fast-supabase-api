import os

from app.tests.utils.env_loader import load_env

load_env()


def get_db_client():

    
    # Use SUPABASE_ANON_KEY instead of SUPABASE_KEY
    if (os.getenv("SUPABASE_URL") or "").strip() and (os.getenv("SUPABASE_ANON_KEY") or "").strip():
        from app.supabase_home.client import supabase
        return supabase
    elif (os.getenv("POSTGRES_SERVER") or "").strip() and (os.getenv("POSTGRES_USER") or "").strip():
        from sqlmodel import Session
        from app.core.db import engine
        return Session(engine)
    else:
        raise RuntimeError(
            "No database configuration found. Set SUPABASE_URL/SUPABASE_ANON_KEY or POSTGRES_SERVER/POSTGRES_USER."
        )
