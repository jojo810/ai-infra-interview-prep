from pydantic import BaseModel

class InterviewAnswerRequest(BaseModel):
    scenario: str
    answer: str

class InterviewEvaluationResponse(BaseModel):
    strengths: str
    gaps: str
    improved_answer: str

