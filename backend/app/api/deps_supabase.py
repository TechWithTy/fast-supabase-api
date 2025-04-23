from fastapi import Depends, HTTPException, status, Request
from app.supabase_home.client import SupabaseClient
import logging

async def get_current_supabase_superuser(request: Request):
    auth_header = request.headers.get("authorization")
    logging.debug(f"[get_current_supabase_superuser] Authorization header: {auth_header}")
    if not auth_header or not auth_header.lower().startswith("bearer "):
        logging.warning("[get_current_supabase_superuser] Missing credentials")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Missing credentials")
    token = auth_header[7:]
    try:
        auth_service = SupabaseClient().get_auth_service()
        user_info = await auth_service.get_user_by_token(token)
        user = user_info.get("user", user_info)
        meta = user.get("user_metadata", {})
        app_meta = user.get("app_metadata", {})
        logging.debug(f"[get_current_supabase_superuser] user_metadata: {meta}, app_metadata: {app_meta}")
        if not (meta.get("is_superuser") or app_meta.get("is_superuser")):
            logging.warning(f"[get_current_supabase_superuser] Not a superuser. meta: {meta}, app_meta: {app_meta}")
            raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")
        logging.info(f"[get_current_supabase_superuser] Superuser access granted for user: {user.get('email')}")
        return user
    except Exception as e:
        logging.error(f"[get_current_supabase_superuser] Exception: {e}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials")
