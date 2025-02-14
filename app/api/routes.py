import os
from pathlib import Path

from agents.search import Search
from fastapi import APIRouter
from metagpt.const import METAGPT_ROOT
from .models import QueryRequest, QueryResponse

router = APIRouter()
search = Search(config_path=METAGPT_ROOT / "config/config2.yaml")


@router.post("/request", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    # Получение контекста через RAG
    result = await search.get_answer(request.query)

    return QueryResponse(id=request.id, **result)
