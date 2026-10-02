import logging

from fastapi import FastAPI, HTTPException

from app.ai_service import (
    AIServiceError,
    generate_interview_scenario,
)

from app.interview_agent import run_interview_evaluation

from app.models import InterviewAnswerRequest

from app.config import settings


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

app = FastAPI(title="AI Infrastructure Interview Prep")

@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/config-check")
def config_check():
    return {
        "openai_configured": bool(settings.open_api_key),
        "model": settings.open_ai_model,
    }


@app.get("/scenario")
def scenario():
    try:
        return {
            "scenario": generate_interview_scenario()
        }
    except AIServiceError as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc),
        ) from exc

@app.post("/evaluate")
def evaluate(request: InterviewAnswerRequest):
    try:
        return run_interview_evaluation(
            scenario=request.scenario,
            answer=request.answer,
        )
    
    except AIServiceError as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc),
        ) from exc