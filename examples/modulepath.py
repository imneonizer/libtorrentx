import os, sys
from pathlib import Path

# Used to add the parent directory to the path
sys.path.append(Path(os.path.realpath(__file__)).parent.parent.as_posix())
