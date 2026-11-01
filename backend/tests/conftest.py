import os
import sys
from pathlib import Path

# Enforce testing environment for predictable, deterministic regression execution
os.environ["APP_ENV"] = "testing"
os.environ["AI_ENABLE_GEMINI"] = "false"
os.environ["AI_ENABLE_QWEN"] = "false"
os.environ["AI_ENABLE_GEMMA"] = "false"

# Ensure backend root is always on sys.path regardless of execution directory
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))
