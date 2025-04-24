from fastapi import Request, HTTPException, status, Depends

def require_scope(required_scope: str):
    def checker(request: Request):
        token_scopes = getattr(request.state, "token_scopes", [])
        if required_scope not in token_scopes:
            raise HTTPException(status_code=403, detail="Insufficient OAuth scope")
    return Depends(checker)
