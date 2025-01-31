import os
from pathlib import Path

from agents.search import Search
from fastapi import APIRouter

from .models import QueryRequest, QueryResponse

router = APIRouter()
search = Search(config_path=Path(os.getenv("CONFIG_PATH")))


@router.post("/request", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    # Получение контекста через RAG
    result = await search.get_answer(request.query)

    return QueryResponse(id=request.id, **result)
