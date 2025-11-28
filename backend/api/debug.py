"""
Debug API endpoint.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import logging

from retrieval.vector_search import vector_search
from retrieval.context_packer import context_packer
from llm.gemini_client import gemini_client
from llm.prompts import build_debug_prompt

logger = logging.getLogger(__name__)

router = APIRouter()


class DebugRequest(BaseModel):
    """Debug request model."""
    file_path: str
    error_message: str
    context: Optional[str] = None


class DebugResponse(BaseModel):
    """Debug response model."""
    analysis: str
    suggested_fix: str
    context_stats: dict


@router.post("/debug")
async def debug_code(request: DebugRequest):
    """
    Debug a code issue.
    
    Analyzes the error and provides a fix.
    """
    try:
        # Build search query from error and file
        search_query = f"{request.file_path} {request.error_message}"
        
        # 1. Search for relevant code
        vector_results = await vector_search.search(search_query, k=15)
        
        # 2. Pack context
        system_prompt = "Debug assistant"
        context, stats = context_packer.pack_context(
            vector_results,
            system_prompt
        )
        
        # 3. Build debug prompt
        debug_prompt = build_debug_prompt(
            context,
            request.error_message,
            request.file_path
        )
        
        # 4. Generate response
        response = await gemini_client.generate_response(debug_prompt)
        
        # Parse response (simplified - in production, use structured output)
        return DebugResponse(
            analysis=response,
            suggested_fix=response,
            context_stats=stats
        )
    
    except Exception as e:
        logger.error(f"Error in debug endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))
