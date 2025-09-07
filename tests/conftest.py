import sys
from pathlib import Path

# Ensure project root is importable so `src` package can be imported
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
