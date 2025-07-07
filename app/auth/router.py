from fastapi import Depends, HTTPExceptionfrom 
from fastapi.security import HTTPBasic, HTTPBasicCredentialsapp 


secret_user: str = "newphone"
secret_password: str = "whodis?"
basic: HTTPBasicCredentials = HTTPBasic()

@app.get("/who")
def get_user(creds: HTTPBasicCredentials = Depends(basic)) -> dict:    
    if (creds.username == secret_user and        creds.password == secret_password):        
        return {"username": creds.username,            "password": creds.password}    
    raise HTTPException(status_code=401, detail="Hey!")