# code_interpreter_tool.py

import subprocess
import resource
import os
import tempfile

class CodeInterpreterTool:
    def __init__(self):
        self.description = "Executes code in a sandboxed environment"

    def run(self, code: str):
        try:
            resource.setrlimit(resource.RLIMIT_CPU, (1, 1))
            resource.setrlimit(resource.RLIMIT_AS, (100 * 1024 * 1024, 100 * 1024 * 1024))
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmpfile:
                tmpfile.write(code.encode())
                tmpfile_path = tmpfile.name
            
            result = subprocess.run(
                ['docker', 'run', '--rm', '-v', f'{tmpfile_path}:/code.py', 'python:3.9', 'python', '/code.py'],
                capture_output=True,
                timeout=5
            )
            
            os.remove(tmpfile_path)

            if result.returncode != 0:
                raise Exception(f"Code execution error: {result.stderr.decode()}")

            return result.stdout.decode()
        
        except Exception as e:
            return str(e)
