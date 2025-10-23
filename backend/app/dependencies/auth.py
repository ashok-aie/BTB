# app/dependencies/auth.py
from fastapi.responses import RedirectResponse
from fastapi import Request, HTTPException, status

def require_login(request: Request):
    user = request.session.get("user")
    if not user:
        # Redirect to login page if user is not logged in
        return RedirectResponse(url="/login", status_code=303)
    return user


def get_current_user(request: Request):
    user_id = request.session.get("user_id")  # Assuming you use cookie/session
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user_id
