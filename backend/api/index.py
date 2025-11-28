"""
Index statistics and management API.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import logging

from services.indexer import indexer

logger = logging.getLogger(__name__)

router = APIRouter()


class IndexStatsResponse(BaseModel):
    """Index statistics response."""
    metrics: dict
    vector_store: dict
    graph_store: dict


class IndexRequest(BaseModel):
    """Index request model."""
    repository_path: str


@router.get("/stats")
async def get_index_stats():
    """
    Get indexing statistics and coverage metrics.
    """
    try:
        stats = indexer.get_stats()
        return IndexStatsResponse(**stats)
    
    except Exception as e:
        logger.error(f"Error getting index stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/index")
async def index_repository(request: IndexRequest):
    """
    Index a repository.
    
    Args:
        repository_path: Path to repository root
    """
    try:
        stats = await indexer.index_repository(request.repository_path)
        return {"status": "success", "stats": stats}
    
    except Exception as e:
        logger.error(f"Error indexing repository: {e}")
        raise HTTPException(status_code=500, detail=str(e))
