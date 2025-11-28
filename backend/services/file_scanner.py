"""
File scanner for discovering code files in a repository.
"""
from pathlib import Path
from typing import List
import logging

logger = logging.getLogger(__name__)


class FileScanner:
    """Scans repository for code files."""
    
    def __init__(self, supported_extensions: List[str] = None):
        """
        Initialize file scanner.
        
        Args:
            supported_extensions: List of file extensions to scan (e.g., ['.py', '.ts'])
        """
        self.supported_extensions = supported_extensions or ['.py', '.ts', '.tsx', '.js', '.jsx']
    
    def scan_directory(self, directory: str, exclude_patterns: List[str] = None) -> List[str]:
        """
        Scan directory for code files.
        
        Args:
            directory: Root directory to scan
            exclude_patterns: Patterns to exclude (e.g., ['node_modules', '__pycache__'])
            
        Returns:
            List of file paths
        """
        exclude_patterns = exclude_patterns or [
            'node_modules', '__pycache__', '.git', 'venv', 'env',
            'dist', 'build', '.next', 'coverage'
        ]
        
        directory_path = Path(directory)
        if not directory_path.exists():
            logger.error(f"Directory does not exist: {directory}")
            return []
        
        files = []
        
        for file_path in directory_path.rglob('*'):
            # Skip directories
            if not file_path.is_file():
                continue
            
            # Skip excluded patterns
            if any(pattern in str(file_path) for pattern in exclude_patterns):
                continue
            
            # Check if file has supported extension
            if file_path.suffix in self.supported_extensions:
                files.append(str(file_path))
        
        logger.info(f"Found {len(files)} code files in {directory}")
        return files
    
    def get_file_info(self, file_path: str) -> dict:
        """Get basic information about a file."""
        path = Path(file_path)
        return {
            'path': str(path),
            'name': path.name,
            'extension': path.suffix,
            'size': path.stat().st_size if path.exists() else 0
        }


# Global file scanner instance
file_scanner = FileScanner()
