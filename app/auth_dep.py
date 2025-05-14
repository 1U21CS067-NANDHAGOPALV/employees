from fastapi import Depends, HTTPException
from app.oauth import verify_token
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/employee/login")

def get_current_employee(token: str = Depends(oauth2_scheme)) -> int:
    employee_id = verify_token(token)
    if employee_id is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return employee_id

