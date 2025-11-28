"""
Tree-sitter parser for Python and TypeScript.
"""
from tree_sitter import Language, Parser
import tree_sitter_python as tspython
import tree_sitter_typescript as tstype
from typing import List, Dict, Any, Optional
from pathlib import Path


class TreeSitterParser:
    """Parses code using Tree-sitter."""
    
    def __init__(self):
        """Initialize parsers for Python and TypeScript."""
        # Python parser
        self.py_language = Language(tspython.language())
        self.py_parser = Parser(self.py_language)
        
        # TypeScript parser
        self.ts_language = Language(tstype.language_typescript())
        self.ts_parser = Parser(self.ts_language)
    
    def parse_file(self, file_path: str, content: str) -> Optional[Any]:
        """
        Parse a file and return AST.
        
        Args:
            file_path: Path to file
            content: File content
            
        Returns:
            Tree-sitter tree object or None if unsupported
        """
        ext = Path(file_path).suffix
        
        if ext == '.py':
            return self.py_parser.parse(bytes(content, 'utf8'))
        elif ext in ['.ts', '.tsx']:
            return self.ts_parser.parse(bytes(content, 'utf8'))
        else:
            return None
    
    def extract_functions(self, tree: Any, content: str) -> List[Dict[str, Any]]:
        """
        Extract function definitions from AST.
        
        Args:
            tree: Tree-sitter tree
            content: Source code
            
        Returns:
            List of function information dictionaries
        """
        functions = []
        
        def traverse(node):
            # Python function
            if node.type == 'function_definition':
                name_node = node.child_by_field_name('name')
                if name_node:
                    functions.append({
                        'name': name_node.text.decode('utf8'),
                        'start_line': node.start_point[0] + 1,
                        'end_line': node.end_point[0] + 1,
                        'start_byte': node.start_byte,
                        'end_byte': node.end_byte,
                        'type': 'function'
                    })
            
            # TypeScript function
            elif node.type in ['function_declaration', 'method_definition', 'arrow_function']:
                name_node = node.child_by_field_name('name')
                if name_node:
                    functions.append({
                        'name': name_node.text.decode('utf8'),
                        'start_line': node.start_point[0] + 1,
                        'end_line': node.end_point[0] + 1,
                        'start_byte': node.start_byte,
                        'end_byte': node.end_byte,
                        'type': 'function'
                    })
            
            for child in node.children:
                traverse(child)
        
        traverse(tree.root_node)
        return functions
    
    def extract_classes(self, tree: Any, content: str) -> List[Dict[str, Any]]:
        """Extract class definitions from AST."""
        classes = []
        
        def traverse(node):
            if node.type in ['class_definition', 'class_declaration']:
                name_node = node.child_by_field_name('name')
                if name_node:
                    classes.append({
                        'name': name_node.text.decode('utf8'),
                        'start_line': node.start_point[0] + 1,
                        'end_line': node.end_point[0] + 1,
                        'start_byte': node.start_byte,
                        'end_byte': node.end_byte,
                        'type': 'class'
                    })
            
            for child in node.children:
                traverse(child)
        
        traverse(tree.root_node)
        return classes
    
    def extract_imports(self, tree: Any, content: str) -> List[Dict[str, Any]]:
        """Extract import statements from AST."""
        imports = []
        
        def traverse(node):
            if node.type in ['import_statement', 'import_from_statement', 'import_declaration']:
                imports.append({
                    'text': node.text.decode('utf8'),
                    'start_line': node.start_point[0] + 1,
                    'end_line': node.end_point[0] + 1,
                    'type': 'import'
                })
            
            for child in node.children:
                traverse(child)
        
        traverse(tree.root_node)
        return imports
    
    def extract_calls(self, tree: Any, content: str) -> List[Dict[str, Any]]:
        """Extract function calls from AST."""
        calls = []
        
        def traverse(node):
            if node.type == 'call':
                # Get function being called
                function_node = node.child_by_field_name('function')
                if function_node:
                    calls.append({
                        'function': function_node.text.decode('utf8'),
                        'line': node.start_point[0] + 1,
                        'type': 'call'
                    })
            
            for child in node.children:
                traverse(child)
        
        traverse(tree.root_node)
        return calls


# Global parser instance
parser = TreeSitterParser()
