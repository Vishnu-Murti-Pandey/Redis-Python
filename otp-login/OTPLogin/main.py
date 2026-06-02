from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from config import REDIS_OTP_KEY
from config_redis import redis_client
from utils import generate_otp

app = FastAPI(title="OTP APP")

# Request Schema
class OTPRequest(BaseModel):
    phone: str
    
class OTPVerifyRequest(BaseModel):
    phone: str
    otp: str

# Response Schema
class OTPResponse(BaseModel):
    otp: str
    message: str

class TTLResponse(BaseModel):
    ttl: int

class OTPVerifyResponse(BaseModel):
    message: str
    

@app.post('/api/otp', response_model=OTPResponse)
def generateOtp(request: OTPRequest):
    phone = request.phone
    
    otp = generate_otp(6)
    
    redis_client.set(f"{REDIS_OTP_KEY}{phone}", otp, ex=120)
    
    return { "otp": otp, "message": "OTP send successfully."}


@app.post('/api/otp/verify', response_model=OTPVerifyResponse)
def verifyOtp(request: OTPVerifyRequest):
    phone = request.phone
    otp = request.otp
    
    otp_cached = redis_client.get(f"{REDIS_OTP_KEY}{phone}")
    
    if not otp_cached:
        return {"message": "OTP expired"}
    
    if(otp != otp_cached):
        raise HTTPException(status_code=404, detail="Invalid OTP")
    
    redis_client.delete(f"{REDIS_OTP_KEY}{phone}")
    
    return {"message": "OTP verified successfully."}


@app.get('/api/ttl', response_model=TTLResponse)
def getTTL(phone: str):
    ttl = redis_client.ttl(f"{REDIS_OTP_KEY}{phone}")
    
    return {"ttl": ttl}
