import os
import site
from importlib.util import find_spec

spec = find_spec("notebook")
if spec is not None:
    print(f"Jupyter Notebook находится по следующему пути: {os.path.dirname(spec.origin)}")
else:
    print("Модуль Jupyter Notebook не обнаружен.")
	