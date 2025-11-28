"""
Planning API endpoint.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import logging

from retrieval.vector_search import vector_search
from retrieval.context_packer import context_packer
from llm.gemini_client import gemini_client
from llm.prompts import build_plan_prompt

logger = logging.getLogger(__name__)

router = APIRouter()


class PlanRequest(BaseModel):
    """Plan request model."""
    goal: str
    scope: Optional[str] = None


class PlanResponse(BaseModel):
    """Plan response model."""
    plan: str
    context_stats: dict


@router.post("/plan")
async def create_plan(request: PlanRequest):
    """
    Create an implementation plan for a goal.
    
    Analyzes the codebase and creates a structured plan.
    """
    try:
        # 1. Search for relevant code
        search_query = request.goal
        if request.scope:
            search_query = f"{request.scope} {request.goal}"
        
        vector_results = await vector_search.search(search_query, k=20)
        
        # 2. Pack context
        system_prompt = "Planning assistant"
        context, stats = context_packer.pack_context(
            vector_results,
            system_prompt
        )
        
        # 3. Build plan prompt
        plan_prompt = build_plan_prompt(context, request.goal)
        
        # 4. Generate plan
        plan = await gemini_client.generate_response(plan_prompt)
        
        return PlanResponse(plan=plan, context_stats=stats)
    
    except Exception as e:
        logger.error(f"Error in plan endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))
