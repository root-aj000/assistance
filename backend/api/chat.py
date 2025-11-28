"""
Chat API endpoints for codebase interaction.
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
import logging

from retrieval.vector_search import vector_search
from retrieval.graph_search import graph_search
from retrieval.ranker import ranker
from retrieval.context_packer import context_packer
from llm.gemini_client import gemini_client
from llm.prompts import build_chat_prompt

logger = logging.getLogger(__name__)

router = APIRouter()


class ChatRequest(BaseModel):
    """Chat request model."""
    question: str
    stream: bool = False


class ChatResponse(BaseModel):
    """Chat response model."""
    answer: str
    context_stats: dict


@router.post("/chat")
async def chat_with_codebase(request: ChatRequest):
    """
    Chat with the entire codebase.
    
    Retrieves relevant code using hybrid search and generates response.
    """
    try:
        # 1. Vector search
        vector_results = await vector_search.search(request.question, k=20)
        
        # 2. Graph expansion (get nodes from top results)
        # For simplicity, we'll use vector results directly
        graph_nodes = []
        
        # 3. Rank results
        ranked_chunks = ranker.rank(vector_results, graph_nodes)
        ranked_chunks = ranker.deduplicate(ranked_chunks)
        
        # 4. Pack context
        system_prompt = "You are a helpful code assistant."
        user_prompt = build_chat_prompt("", request.question)
        context, stats = context_packer.pack_context(ranked_chunks, user_prompt)
        
        # 5. Build final prompt
        final_prompt = build_chat_prompt(context, request.question)
        
        # 6. Generate response
        if request.stream:
            async def generate():
                async for chunk in gemini_client.generate_response_stream(final_prompt):
                    yield chunk
            
            return StreamingResponse(generate(), media_type="text/plain")
        else:
            answer = await gemini_client.generate_response(final_prompt)
            return ChatResponse(answer=answer, context_stats=stats)
    
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/codebase/chat")
async def chat_with_file(request: ChatRequest, file_path: Optional[str] = None):
    """
    Chat with a specific file or subset of the codebase.
    """
    # Similar to chat_with_codebase but can filter by file_path
    # For simplicity, using same implementation
    return await chat_with_codebase(request)
