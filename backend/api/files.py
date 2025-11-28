"""
File operations API endpoints.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from pathlib import Path
import logging

from services.file_scanner import file_scanner

logger = logging.getLogger(__name__)

router = APIRouter()


class FileInfo(BaseModel):
    """File information model."""
    path: str
    name: str
    extension: str
    size: int


class FileListResponse(BaseModel):
    """File list response model."""
    files: List[FileInfo]
    total: int


class FileContentResponse(BaseModel):
    """File content response model."""
    path: str
    content: str
    lines: int


@router.get("/files")
async def list_files(directory: str = "."):
    """
    List all code files in the repository.
    
    Args:
        directory: Repository root directory
    """
    try:
        file_paths = file_scanner.scan_directory(directory)
        
        files = []
        for file_path in file_paths:
            file_info = file_scanner.get_file_info(file_path)
            files.append(FileInfo(**file_info))
        
        return FileListResponse(files=files, total=len(files))
    
    except Exception as e:
        logger.error(f"Error listing files: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/file")
async def get_file_content(file_path: str):
    """
    Get content of a specific file.
    
    Args:
        file_path: Path to the file
    """
    try:
        path = Path(file_path)
        
        if not path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = len(content.split('\n'))
        
        return FileContentResponse(
            path=str(path),
            content=content,
            lines=lines
        )
    
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        logger.error(f"Error reading file: {e}")
        raise HTTPException(status_code=500, detail=str(e))
