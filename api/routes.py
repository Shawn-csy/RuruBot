from fastapi import APIRouter, HTTPException, Query
from services.use_cases.astro import get_astro_result
from services.constants import astro as astro_dict

router = APIRouter(prefix="/api")


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
