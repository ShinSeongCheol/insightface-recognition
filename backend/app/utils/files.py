import numpy as np
from uuid import uuid4
from pathlib import Path
from datetime import datetime

def capture_image(buffer: np.ndarray):
    today_date = datetime.now().strftime("%Y-%m-%d")
    save_dir = Path(f"static/captures/{today_date}")
    save_dir.mkdir(parents=True, exist_ok=True)
    file_name = uuid4()
    file_path = save_dir / f"{file_name}.jpg"

    with open(file_path, "wb") as f:
        f.write(buffer.tobytes())