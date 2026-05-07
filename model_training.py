"""
Calorie Burnt Prediction - Model Training Pipeline
Trains and compares Linear Regression, Random Forest, and XGBoost
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import xgboost as xgb
import joblib
import json
import os

# ─── 1. Load & Merge Dataset ───────────────────────────────────────────────────
print("📦 Loading dataset...")
df_exercise = pd.read_csv("dataset/exercise.csv")
df_calories = pd.read_csv("dataset/calories.csv")
df = pd.merge(df_exercise, df_calories, on="User_ID")

print(f"   Total records: {len(df)}")
print(f"   Features: {df.columns.tolist()}")
print(f"   Missing values: {df.isnull().sum().sum()}")

# ─── 2. Feature Engineering ────────────────────────────────────────────────────
print("\n🔧 Engineering features...")
df["Gender"] = df["Gender"].map({"male": 0, "female": 1})

# BMI as a derived feature
df["BMI"] = df["Weight"] / ((df["Height"] / 100) ** 2)

# Effort index: heart rate × duration
df["Effort_Index"] = df["Heart_Rate"] * df["Duration"]

FEATURES = [
    "Gender", "Age", "Height", "Weight",
    "Duration", "Heart_Rate", "Body_Temp",
    "BMI", "Effort_Index"
]
TARGET = "Calories"

X = df[FEATURES]
y = df[TARGET]

# ─── 3. Train/Test Split ───────────────────────────────────────────────────────
print("\n✂️  Splitting data (80/20)...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ─── 4. Scale Features ─────────────────────────────────────────────────────────
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

# ─── 5. Train Models ───────────────────────────────────────────────────────────
print("\n🤖 Training models...")

models = {
    "Linear Regression": LinearRegression(),
    "Random Forest":     RandomForestRegressor(
                             n_estimators=150, max_depth=12,
                             random_state=42, n_jobs=-1),
    "XGBoost":           xgb.XGBRegressor(
                             n_estimators=200, learning_rate=0.08,
                             max_depth=6, subsample=0.8,
                             colsample_bytree=0.8, random_state=42,
                             verbosity=0)
}

results = {}

for name, model in models.items():
    print(f"   ▶ Training {name}...")
    model.fit(X_train_scaled, y_train)
    preds = model.predict(X_test_scaled)

    mae  = mean_absolute_error(y_test, preds)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    r2   = r2_score(y_test, preds)

    results[name] = {
        "MAE":  round(mae,  4),
        "RMSE": round(rmse, 4),
        "R2":   round(r2,   6)
    }
    print(f"      MAE={mae:.2f}  RMSE={rmse:.2f}  R²={r2:.4f}")

# ─── 6. Select Best Model ──────────────────────────────────────────────────────
best_name = max(results, key=lambda k: results[k]["R2"])
best_model = models[best_name]
print(f"\n🏆 Best model: {best_name} (R²={results[best_name]['R2']})")

# Feature importance (XGBoost / RF)
feature_importance = {}
if hasattr(best_model, "feature_importances_"):
    for feat, imp in zip(FEATURES, best_model.feature_importances_):
        feature_importance[feat] = round(float(imp), 6)

# ─── 7. Save Artifacts ─────────────────────────────────────────────────────────
print("\n💾 Saving model artifacts...")
joblib.dump(best_model, "model.pkl")
joblib.dump(scaler,     "scaler.pkl")

meta = {
    "best_model":         best_name,
    "features":           FEATURES,
    "model_results":      results,
    "feature_importance": feature_importance,
    "train_size":         len(X_train),
    "test_size":          len(X_test)
}
with open("model_meta.json", "w") as f:
    json.dump(meta, f, indent=2)

print("✅ Done! Saved: model.pkl | scaler.pkl | model_meta.json")
print("\n📊 Final Comparison:")
print(f"{'Model':<22} {'MAE':>8} {'RMSE':>8} {'R²':>8}")
print("-" * 50)
for name, m in results.items():
    star = " ⭐" if name == best_name else ""
    print(f"{name:<22} {m['MAE']:>8.2f} {m['RMSE']:>8.2f} {m['R2']:>8.4f}{star}")
