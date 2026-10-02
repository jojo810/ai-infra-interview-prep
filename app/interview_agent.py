from app.ai_service import (
    coach_interview_answer,
    critique_interview_answer,
)


def run_interview_evaluation(
    scenario: str,
    answer: str,
) -> dict:
    critique = critique_interview_answer(
        scenario=scenario,
        answer=answer,
    )

    improved_answer = coach_interview_answer(
        scenario=scenario,
        answer=answer,
        critique=critique,
    )

    return {
        "critique": critique,
        "improved_answer": improved_answer,
    }