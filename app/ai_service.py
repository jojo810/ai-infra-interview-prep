import logging

from openai import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    OpenAI,
    RateLimitError,
)

from app.config import settings

logger = logging.getLogger(__name__)

client = OpenAI(
    api_key=settings.open_api_key,
    timeout=60.0,
)


class AIServiceError(Exception):
    pass

def generate_interview_scenario() -> str:
    try:
        logger.info("Generating AI infrastructure interview scenario")

        response = client.responses.create(
            model=settings.open_ai_model,
            input=(
                "Create one realistic technical interview ario for an"
                "AI infrustructure engineer. Focus on productionizaing an AI"
            " application. Return only the scenario."
            ),
        )

        logger.info("Interview scenario generated successfully")

        return response.output_text

    except APITimeoutError as exc:
        logger.error("OpenAI request timed out")
        raise AIServiceError("AI servcice timed out") from exc
    
    except RateLimitError as exc:
        logger.error("OpenAI rate limit exceeded")
        raise AIServiceError("AI service is temporarily rate limited") from exc
    
    except APIConnectionError as exc:
        logger.error("Unable to connect to OpenAI")
        raise AIServiceError("Unable to connect to AI service") from exc

    except APIStatusError as exc:
        logger.error(
            "OpenAI returned an API error: status_code=%s",
            exc.status_code,
        )
        raise AIServiceError("AI service returned an error") from exc
    

def evaluate_interview_answer(
    scenario: str,
    answer: str
) -> dict:
    try:
        logger.info("Evaluating interview answer")


        prompt = f"""
You are evaluating a technical interview answer for an AI infrastructure engineer role.

Scenario:
{scenario}

Candadite Answer:
{answer}

Evaluate the answer and return exactly these three sections:

STRENGTHS:
What the candidate did well.

GAPS:
What important infrastructure, reliability, security, scalability,
observability, deployment, or AI-specific concerns were missing.

IMPROVED_ANSWER:
Provide a stronger example answer that would perform well in a technical interview.
"""

        response = client.responses.create(
            model=settings.open_ai_model,
            input=prompt,
        )

        text = response.output_text

        logger.info("Interview answer evaluated successfully")

        return {
            "evaluation": text
        }
    
    except APITimeoutError as exc:
        logger.error("OpenAI evaluation request timed out")
        raise AIServiceError("AI service times out") from exc
    
    except RateLimitError as exc:
        logger.error("OpenAI rate limit reached during evaluation")
        raise AIServiceError("AI service is temporarily rate limited") from exc

    except APIConnectionError as exc:
        logger.error("Unable to connect to OpenAI during evaluation")
        raise AIServiceError("Unable to connect to AI Service") from exc

    except APIStatusError as exc:
        logger.error(
            "OpenAI returned an API error during evaluation: status_code=%s",
            exc.status_code
        )
        raise AIServiceError("AI service returned an error") from exc


def critique_interview_answer(
    scenario: str,
    answer: str,
) -> str:
    try:
        logger.info("Critic agent evaluating answer")

        prompt = f"""
You are a Critic Agenct for an AI Infrastructure Engineer interview.

Your job is only to analyze the candidate's answer.

Scenario:
{scenario}

Candidate Answer:
{answer}

Return two sections:

STREGTHS:
Identify important missing considerations involving areas such as:
- Infrastucture
- Security
- reliability
- scalability
- observability
- CI/CD
- containers
- secrets
- networking
- AI model reliability
- latency
- cost
- failure handling

Do not rewrite the candidate's answer
"""

        response = client.responses.create(
            model=settings.open_ai_model,
            input=prompt,
        )

        logger.info("Critic agent completed successfully")

        return response.output_text

    except APITimeoutError as exc:
        logger.error("Critic agent timed out")
        raise AIServiceError("AI service times out") from exc
    
    except RateLimitError as exc:
        logger.error("Critic agent rate limited")
        raise AIServiceError("AI service is temporarily rate limited") from exc

    except APIConnectionError as exc:
        logger.error("Critic agent connection failure")
        raise AIServiceError("Unable to connect to AI Service") from exc

    except APIStatusError as exc:
        logger.error(
            "Critic agent API failure: status_code=%s",
            exc.status_code
        )
        raise AIServiceError("AI service returned an error") from exc


def coach_interview_answer(
    scenario: str,
    answer: str,
    critique: str,
) -> str:
    try:
        logger.info("Coach agent generating improved answer")

        prompt = f"""
You are a Coach Agent for an AI Infrastructure Engineering interview.

Scenario:
{scenario}

Candidate's Original Answer:
{answer}

Critic Agent Feedback:
{critique}

Using the critic's feedback, produce a stronger version of the candidate's answer.

The answer should sound like a real engineer speaking in a technical interview. It
should be clear and structured, but not overly formal.

Do not just list technologies. Explain the reasoning behind important
infrastructure decisions.
"""
        response = client.responses.create(
            model=settings.open_ai_model,
            input=prompt,
        )

        logger.info("Coach agent completed successfully")

        return response.output_text
    
    except APITimeoutError as exc:
        logger.error("Coach agent timed out")
        raise AIServiceError("AI service times out") from exc
    
    except RateLimitError as exc:
        logger.error("Coach agent rate limited")
        raise AIServiceError("AI service is temporarily rate limited") from exc

    except APIConnectionError as exc:
        logger.error("Coach agent connection failure")
        raise AIServiceError("Unable to connect to AI Service") from exc

    except APIStatusError as exc:
        logger.error(
            "Coach agent API failure: status_code=%s",
            exc.status_code
        )
        raise AIServiceError("AI service returned an error") from exc
