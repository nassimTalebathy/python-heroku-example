from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler
import joblib

try:
    import src.config as config
except:
    import config

# Generate fake training data
X, y = make_classification(n_samples=10000, n_features=config.NUM_COLS, n_informative=2, n_redundant=2, random_state=42)
print(X.shape, y.shape)

# Train random forest model
pipe = Pipeline([
    ('scaler', RobustScaler()),
    ('rf', RandomForestClassifier(n_jobs=-1)),
])
pipe.fit(X, y)
print('Fitted pipe', pipe, sep='\n')

# Save
joblib.dump(pipe, config.MODEL_PATH)