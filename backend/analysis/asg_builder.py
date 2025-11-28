"""
Abstract Semantic Graph (ASG) builder.
Builds code relationships and semantic structure.
"""
from typing import List, Dict, Any
from db.models import CodeNode, CodeEdge, NodeType
from analysis.tree_sitter_parser import parser
import hashlib


class ASGBuilder:
    """Builds Abstract Semantic Graph from code."""
    
    def build_asg(self, file_path: str, content: str) -> tuple[List[CodeNode], List[CodeEdge]]:
        """
        Build ASG for a file.
        
        Args:
            file_path: Path to the file
            content: File content
            
        Returns:
            Tuple of (nodes, edges)
        """
        nodes = []
        edges = []
        
        # Parse file
        tree = parser.parse_file(file_path, content)
        if not tree:
            return nodes, edges
        
        # Extract functions
        functions = parser.extract_functions(tree, content)
        for func in functions:
            node_id = self._generate_node_id(file_path, func['name'], func['start_line'])
            code = content.encode('utf8')[func['start_byte']:func['end_byte']].decode('utf8')
            
            nodes.append(CodeNode(
                id=node_id,
                type=NodeType.FUNCTION,
                name=func['name'],
                file_path=file_path,
                start_line=func['start_line'],
                end_line=func['end_line'],
                code=code,
                metadata={'signature': func.get('signature', '')}
            ))
        
        # Extract classes
        classes = parser.extract_classes(tree, content)
        for cls in classes:
            node_id = self._generate_node_id(file_path, cls['name'], cls['start_line'])
            code = content.encode('utf8')[cls['start_byte']:cls['end_byte']].decode('utf8')
            
            nodes.append(CodeNode(
                id=node_id,
                type=NodeType.CLASS,
                name=cls['name'],
                file_path=file_path,
                start_line=cls['start_line'],
                end_line=cls['end_line'],
                code=code,
                metadata={}
            ))
        
        # Extract imports
        imports = parser.extract_imports(tree, content)
        for imp in imports:
            node_id = self._generate_node_id(file_path, imp['text'], imp['start_line'])
            
            nodes.append(CodeNode(
                id=node_id,
                type=NodeType.IMPORT,
                name=imp['text'],
                file_path=file_path,
                start_line=imp['start_line'],
                end_line=imp['end_line'],
                code=imp['text'],
                metadata={}
            ))
        
        # Extract function calls and create edges
        calls = parser.extract_calls(tree, content)
        for call in calls:
            # Find which function this call belongs to
            calling_func = self._find_containing_function(call['line'], functions)
            if calling_func:
                source_id = self._generate_node_id(file_path, calling_func['name'], calling_func['start_line'])
                
                # Try to find the called function in the same file
                called_func = next((f for f in functions if f['name'] == call['function']), None)
                if called_func:
                    target_id = self._generate_node_id(file_path, called_func['name'], called_func['start_line'])
                    
                    edges.append(CodeEdge(
                        source_id=source_id,
                        target_id=target_id,
                        relationship="calls",
                        metadata={'line': call['line']}
                    ))
        
        return nodes, edges
    
    def _generate_node_id(self, file_path: str, name: str, line: int) -> str:
        """Generate unique node ID."""
        content = f"{file_path}::{name}::{line}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _find_containing_function(self, line: int, functions: List[Dict]) -> Dict:
        """Find which function contains a given line."""
        for func in functions:
            if func['start_line'] <= line <= func['end_line']:
                return func
        return None


# Global ASG builder instance
asg_builder = ASGBuilder()
