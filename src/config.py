from pathlib import Path

MODEL_VERSION = '0.1.0'

BASE_DIR = Path(__file__).resolve(strict=True).parent
MODEL_PATH = BASE_DIR / f'models/model-{MODEL_VERSION}.pkl'
NUM_COLS = 10