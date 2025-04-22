import os


def get_db_client():
    if os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_KEY"):
        from app.supabase_home.client import supabase

        return supabase
    elif os.getenv("POSTGRES_SERVER") and os.getenv("POSTGRES_USER"):
        from sqlmodel import Session

        from app.core.db import engine

        return Session(engine)
    else:
        raise RuntimeError(
            "No database configuration found. Set SUPABASE_URL/SUPABASE_KEY or POSTGRES_SERVER/POSTGRES_USER."
        )
