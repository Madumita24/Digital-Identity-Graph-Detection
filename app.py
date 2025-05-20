from fastapi import FastAPI
from pydantic import BaseModel
from trust_core import compute_trust_score

app = FastAPI()

class UserRequest(BaseModel):
    user_id: str

@app.post("/check_trust")
def check_trust(request: UserRequest):
    score = compute_trust_score(request.user_id)
    return {"user_id": request.user_id, "trust_score": score}
