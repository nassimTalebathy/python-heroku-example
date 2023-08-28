import time
from fastapi import FastAPI
import joblib
from src.data_types import DataInput, DataOutput
import src.config as config
from src.log import logger


# Global variable to store model after loading it
model = None

# FastAPI app
app = FastAPI()


@app.on_event("startup")
def load_model():
    global model
    model = joblib.load(config.MODEL_PATH)
    logger.info("Model loaded!")
    return


@app.get("/health")
def predict() -> dict:
    return {"status": "OK", "status_code": 200, "model_version": config.MODEL_VERSION}


@app.post("/predict", response_model=DataOutput)
def predict(input_data: DataInput) -> dict:
    if input_data.verbose:
        logger.info(f"Incoming request with data type {type(input_data)}")
        logger.info(f"input_data:\n{input_data[:2]}")
    start_time = time.time()
    np_array = input_data.to_np_array()
    predictions = model.predict_proba(np_array)[:, 1]
    end_time = time.time()
    if input_data.verbose:
        logger.info(f"Predictions took {end_time - start_time:.1f} seconds")
        logger.info(f"{predictions}")
    return {
        "predictions": predictions.tolist(),
        "start_time": start_time,
        "time_taken": end_time - start_time,
    }
