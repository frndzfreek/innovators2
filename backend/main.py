from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
import pandas as pd

app = FastAPI()

# Load and preprocess the dataset
DATA_PATH = "./data/incidents.csv"
data = pd.read_csv(DATA_PATH)

# AI model for ticket classification
model = pipeline("zero-shot-classification")
categories = ["Incident ID","Incident Type","Security","Description","Status","Time Reported","Time Resolved","Solution","Category","Root Cause"]

# API models
class Incident(BaseModel):
    description: str

@app.get("/")
def home():
    return {"message": "Welcome to the SIMS Backend!"}

@app.get("/incidents")
def get_incidents():
    return data.to_dict(orient="records")

@app.post("/classify")
def classify_incident(incident: Incident):
    result = model(incident.description, candidate_labels=categories)
    return {"category": result["labels"][0], "confidence": result["scores"][0]}

@app.get("/summary")
def get_summary():
    summary = data.groupby("severity").size().reset_index(name="count")
    return summary.to_dict(orient="records")
