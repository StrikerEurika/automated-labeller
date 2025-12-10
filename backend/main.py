# main.py
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import asyncio
import logging

app = FastAPI(title="AutoAnnotate API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class AnnotationRequest(BaseModel):
    image_id: str
    prompt: str
    confidence_threshold: float = 0.3
    iou_threshold: float = 0.5

class BatchAnnotationRequest(BaseModel):
    image_ids: List[str]
    prompt: str
    batch_size: int = 8

class AnnotationResult(BaseModel):
    image_id: str
    detections: List[Dict]
    masks: List[Dict]
    processing_time: float