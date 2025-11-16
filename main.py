import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from database import db, create_document, get_documents
from schemas import Creative, Experiment, Feedback

app = FastAPI(title="Meta Creatives Testing Tools API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Meta Creatives Testing Tools API is running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = os.getenv("DATABASE_NAME") or "❌ Not Set"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
                response["connection_status"] = "Connected"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    return response

# Simple DTOs for requests where only IDs are passed from frontend as strings
class CreateCreativeRequest(Creative):
    pass

class CreateExperimentRequest(BaseModel):
    name: str
    description: Optional[str] = None
    creative_ids: List[str]
    status: Optional[str] = "draft"
    hypothesis: Optional[str] = None

class CreateFeedbackRequest(BaseModel):
    experiment_id: str
    creative_id: str
    score: int
    note: Optional[str] = None
    user: Optional[str] = None

@app.post("/api/creatives")
def create_creative(req: CreateCreativeRequest):
    try:
        _id = create_document("creative", req)
        return {"id": _id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/creatives")
def list_creatives():
    try:
        docs = get_documents("creative", {})
        # Convert ObjectId to string for frontend
        for d in docs:
            d["_id"] = str(d.get("_id"))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/experiments")
def create_experiment(req: CreateExperimentRequest):
    try:
        _id = create_document("experiment", req.model_dump())
        return {"id": _id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/experiments")
def list_experiments():
    try:
        docs = get_documents("experiment", {})
        for d in docs:
            d["_id"] = str(d.get("_id"))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/feedback")
def submit_feedback(req: CreateFeedbackRequest):
    try:
        _id = create_document("feedback", req.model_dump())
        return {"id": _id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/feedback")
def list_feedback(experiment_id: Optional[str] = None, creative_id: Optional[str] = None):
    try:
        filter_q = {}
        if experiment_id:
            filter_q["experiment_id"] = experiment_id
        if creative_id:
            filter_q["creative_id"] = creative_id
        docs = get_documents("feedback", filter_q)
        for d in docs:
            d["_id"] = str(d.get("_id"))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
