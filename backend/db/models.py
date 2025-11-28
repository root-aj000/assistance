"""
Data models for storing code analysis results.
"""
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum


class NodeType(str, Enum):
    """Types of nodes in the ASG."""
    FUNCTION = "function"
    CLASS = "class"
    METHOD = "method"
    IMPORT = "import"
    VARIABLE = "variable"
    CALL = "call"


@dataclass
class CodeNode:
    """Represents a node in the Abstract Semantic Graph."""
    id: str
    type: NodeType
    name: str
    file_path: str
    start_line: int
    end_line: int
    code: str
    metadata: Dict[str, Any]


@dataclass
class CodeEdge:
    """Represents an edge in the ASG (relationships between nodes)."""
    source_id: str
    target_id: str
    relationship: str  # e.g., "calls", "imports", "defines", "inherits"
    metadata: Dict[str, Any]


@dataclass
class CFGNode:
    """Represents a node in the Control Flow Graph."""
    id: str
    function_id: str
    code: str
    line_number: int
    type: str  # e.g., "entry", "exit", "statement", "condition", "loop"


@dataclass
class CFGEdge:
    """Represents an edge in the CFG (control flow)."""
    source_id: str
    target_id: str
    condition: Optional[str] = None  # For conditional branches


@dataclass
class CodeChunk:
    """Represents a chunk of code for embedding."""
    id: str
    file_path: str
    start_line: int
    end_line: int
    code: str
    tokens: int
    embedding: Optional[List[float]] = None
    metadata: Dict[str, Any] = None


@dataclass
class FileMetadata:
    """Metadata about an indexed file."""
    path: str
    language: str  # "python" or "typescript"
    lines: int
    tokens: int
    chunks: int
    asg_nodes: int
    cfg_nodes: int
    indexed_at: str
    hash: str  # File hash for change detection
