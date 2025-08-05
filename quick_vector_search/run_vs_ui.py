import subprocess
import sys
from pathlib import Path

def main():
    # Adjust path to find vector_search.py
    package_dir = Path(__file__).parent
    script_path = package_dir / "vector_search.py"
    subprocess.run([sys.executable, "-m", "marimo", "run", str(script_path)] + sys.argv[1:])

if __name__ == "__main__":
    main()
