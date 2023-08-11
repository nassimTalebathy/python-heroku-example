import time
from fastapi import FastAPI
import joblib
from src.data_types import DataInput, DataOutput
try:
    import src.config as config
except:
    import config

# Global variable to store model after loading it
model = None 

# FastAPI app
app = FastAPI()

@app.on_event("startup")
def load_model():
    global model
    model = joblib.load(config.MODEL_PATH)
    return


@app.get("/health")
def predict() -> dict:
    return {'status':'OK', 'status_code': 200, 'model_version': config.MODEL_VERSION}


@app.post("/predict", response_model=DataOutput)
def predict(input_data: DataInput) -> dict:
    start_time = time.time()
    np_array = input_data.to_np_array()
    predictions = model.predict_proba(np_array)[:, 1]
    return {
        "predictions": predictions.tolist(),
        "start_time": start_time,
        "time_taken": time.time() - start_time,
    } 
