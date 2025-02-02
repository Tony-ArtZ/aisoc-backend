from fastapi import FastAPI
from model import Code
import subprocess
import os
from contextlib import contextmanager
import tempfile

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@contextmanager
def safe_file_handling(content):
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".pyowo", delete=False
    ) as temp_file:
        try:
            temp_file.write(content)
            temp_file.flush()
            yield temp_file.name
        finally:
            try:
                os.unlink(temp_file.name)
            except Exception:
                pass


@app.get("/")
async def root():
    print("Hello")


@app.post("/run")
async def run(code: Code):
    try:
        code.code = code.code.replace("\r\n", "\n")
        code.code = code.code.replace("\r", "\n")
        code.code = code.code.replace("pythOwO", "")
        with safe_file_handling(code.code) as file_path:
            result = subprocess.run(
                ["python3", "pythowo.py", file_path],
                capture_output=True,
                text=True,
                timeout=30,
            )

        return {
            "output": result.stdout,
            "error": result.stderr,
            "status_code": result.returncode,
        }

    except subprocess.TimeoutExpired:
        return {"output": "", "error": "Execution timed out", "status_code": 124}
    except Exception as e:
        return {"output": "", "error": f"Execution failed: {str(e)}", "status_code": 1}
