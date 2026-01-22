from fastapi import Header, HTTPException, Depends
from app.config import APP_PIN

def verify_pin(x_pin: str = Header(...)):
    if x_pin != APP_PIN:
        raise HTTPException(
            status_code=401,
            detail="Invalid PIN"
        )
