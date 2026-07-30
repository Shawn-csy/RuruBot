from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from services.use_cases.astro import get_astro_result
from services.use_cases.answers_book import get_answers_book_result
from services.use_cases.podcast import get_podcast_result
from services.use_cases.radar import get_radar_result
from services.use_cases.ticket import get_ticket_result
from services.constants import astro as astro_dict
from services.features.help import get_help_message

router = APIRouter(prefix="/api")


class TicketRequest(BaseModel):
    question: str = ""


class AnswersBookRequest(BaseModel):
    question: str = ""


@router.get("/astro")
def get_astro(
    sign: str = Query(..., description="星座名，如 金牛座"),
    type: str = Query("daily", description="daily 或 weekly"),
):
    if sign not in astro_dict:
        raise HTTPException(status_code=400, detail=f"未知星座: {sign}")
    if type not in ("daily", "weekly"):
        raise HTTPException(status_code=400, detail="type 必須是 daily 或 weekly")

    result = get_astro_result(sign, type)

    if result.get("error"):
        raise HTTPException(status_code=503, detail=result["error"])

    return result


@router.get("/radar")
def get_radar():
    result = get_radar_result()
    if result.get("error"):
        raise HTTPException(status_code=503, detail=result["error"])
    return result


@router.post("/ticket")
def post_ticket(payload: TicketRequest):
    result = get_ticket_result(payload.question, with_ai=False)
    if result.get("error"):
        raise HTTPException(status_code=503, detail=result["error"])
    return result


@router.get("/podcast")
def get_podcast():
    result = get_podcast_result()
    if result.get("error"):
        raise HTTPException(status_code=503, detail=result["error"])
    return result


@router.post("/answers-book")
def post_answers_book(payload: AnswersBookRequest):
    result = get_answers_book_result(payload.question)
    if result.get("error"):
        raise HTTPException(status_code=503, detail=result["error"])
    return result


@router.get("/help")
def get_help():
    return get_help_message()
