"""
Control Flow Graph (CFG) builder.
Builds execution flow graphs for functions.
"""
from typing import List, Dict, Any
from db.models import CFGNode, CFGEdge
import hashlib


class CFGBuilder:
    """Builds Control Flow Graphs for functions."""
    
    def build_cfg(self, function_id: str, function_code: str, start_line: int) -> tuple[List[CFGNode], List[CFGEdge]]:
        """
        Build CFG for a function.
        
        This is a simplified CFG builder. A production version would use
        more sophisticated analysis based on the AST.
        
        Args:
            function_id: ID of the function node
            function_code: Function source code
            start_line: Starting line number of function
            
        Returns:
            Tuple of (cfg_nodes, cfg_edges)
        """
        nodes = []
        edges = []
        
        lines = function_code.split('\n')
        
        # Create entry node
        entry_id = f"{function_id}_entry"
        nodes.append(CFGNode(
            id=entry_id,
            function_id=function_id,
            code="<entry>",
            line_number=start_line,
            type="entry"
        ))
        
        # Create exit node
        exit_id = f"{function_id}_exit"
        nodes.append(CFGNode(
            id=exit_id,
            function_id=function_id,
            code="<exit>",
            line_number=start_line + len(lines) - 1,
            type="exit"
        ))
        
        # Create nodes for each statement (simplified)
        prev_node_id = entry_id
        for i, line in enumerate(lines):
            line = line.strip()
            if not line or line.startswith('#') or line.startswith('//'):
                continue
            
            node_id = f"{function_id}_stmt_{i}"
            node_type = self._classify_statement(line)
            
            nodes.append(CFGNode(
                id=node_id,
                function_id=function_id,
                code=line,
                line_number=start_line + i,
                type=node_type
            ))
            
            # Connect to previous node
            edges.append(CFGEdge(
                source_id=prev_node_id,
                target_id=node_id
            ))
            
            # Handle control flow
            if node_type == "condition":
                # For if statements, we'd need more analysis
                # Simplified: just continue flow
                prev_node_id = node_id
            elif node_type == "loop":
                # Create back edge for loop
                prev_node_id = node_id
            elif line.startswith('return'):
                # Connect to exit
                edges.append(CFGEdge(
                    source_id=node_id,
                    target_id=exit_id
                ))
                prev_node_id = node_id
            else:
                prev_node_id = node_id
        
        # Connect last statement to exit if not already connected
        if prev_node_id != entry_id:
            edges.append(CFGEdge(
                source_id=prev_node_id,
                target_id=exit_id
            ))
        else:
            # Empty function
            edges.append(CFGEdge(
                source_id=entry_id,
                target_id=exit_id
            ))
        
        return nodes, edges
    
    def _classify_statement(self, line: str) -> str:
        """Classify statement type."""
        line_lower = line.lower()
        
        if line_lower.startswith(('if ', 'elif ', 'else:', 'switch', 'case')):
            return "condition"
        elif line_lower.startswith(('for ', 'while ', 'do ')):
            return "loop"
        elif line_lower.startswith('return'):
            return "return"
        else:
            return "statement"


# Global CFG builder instance
cfg_builder = CFGBuilder()
