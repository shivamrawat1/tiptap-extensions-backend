import subprocess
import tempfile
import os
import platform
import sys
from typing import Dict, Union
import resource
import ast
import io
from contextlib import redirect_stdout, redirect_stderr

FORBIDDEN_MODULES = {
    'os', 'sys', 'subprocess', 'socket', 'requests', 
    'urllib', 'http', 'ftplib', 'telnetlib'
}

def check_code_safety(code: str) -> tuple[bool, str]:
    """Check if code contains forbidden imports or operations"""
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return False, "Invalid Python syntax"
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for name in node.names:
                if name.name.split('.')[0] in FORBIDDEN_MODULES:
                    return False, f"Use of forbidden module: {name.name}"
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.module.split('.')[0] in FORBIDDEN_MODULES:
                return False, f"Use of forbidden module: {node.module}"
    
    return True, ""

def set_resource_limits():
    """Set resource limits for the subprocess"""
    if platform.system() != 'Windows':  # Resource limits only work on Unix-like systems
        try:
            # 50MB memory limit
            memory_limit = 50 * 1024 * 1024
            resource.setrlimit(resource.RLIMIT_AS, (memory_limit, memory_limit))
            
            # CPU time limit (2 seconds)
            resource.setrlimit(resource.RLIMIT_CPU, (2, 2))
            
            # Restrict file size creation to 1MB
            resource.setrlimit(resource.RLIMIT_FSIZE, (1024 * 1024, 1024 * 1024))
        except Exception as e:
            print(f"Warning: Failed to set resource limits: {e}")

def create_safe_globals():
    """Create a restricted globals dictionary for code execution"""
    safe_modules = {
        'math': __import__('math'),
        'random': __import__('random'),
        'datetime': __import__('datetime'),
        'json': __import__('json'),
        're': __import__('re'),
    }
    
    return {
        '__builtins__': {
            'abs': abs,
            'all': all,
            'any': any,
            'bin': bin,
            'bool': bool,
            'chr': chr,
            'dict': dict,
            'dir': dir,
            'divmod': divmod,
            'enumerate': enumerate,
            'filter': filter,
            'float': float,
            'format': format,
            'frozenset': frozenset,
            'hex': hex,
            'int': int,
            'isinstance': isinstance,
            'issubclass': issubclass,
            'len': len,
            'list': list,
            'map': map,
            'max': max,
            'min': min,
            'oct': oct,
            'ord': ord,
            'pow': pow,
            'print': print,
            'range': range,
            'repr': repr,
            'reversed': reversed,
            'round': round,
            'set': set,
            'slice': slice,
            'sorted': sorted,
            'str': str,
            'sum': sum,
            'tuple': tuple,
            'type': type,
            'zip': zip,
        },
        **safe_modules
    }

def execute_code(code: str) -> Dict[str, Union[bool, str]]:
    """Execute Python code in a restricted environment"""
    # Capture stdout and stderr
    stdout = io.StringIO()
    stderr = io.StringIO()
    
    try:
        # Create restricted environment
        restricted_globals = create_safe_globals()
        restricted_locals = {}

        # Compile the code first to catch syntax errors
        compiled_code = compile(code, '<string>', 'exec')
        
        # Execute the code with restricted globals and locals
        with redirect_stdout(stdout), redirect_stderr(stderr):
            exec(compiled_code, restricted_globals, restricted_locals)
        
        # Get output
        output = stdout.getvalue()
        error = stderr.getvalue()
        
        if error:
            return {
                'success': False,
                'error': error.strip()
            }
        
        return {
            'success': True,
            'output': output.strip() or 'Code executed successfully with no output'
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }
    finally:
        stdout.close()
        stderr.close()