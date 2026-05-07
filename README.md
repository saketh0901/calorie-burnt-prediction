# 🔥 Calorie Burnt Prediction — Final Year Major Project

> **ML-powered web application** that predicts calories burnt during exercise  
> using XGBoost with **R² = 0.9977** accuracy, deployed via Streamlit.

---

## 🗂 Project Structure

```
calorie-burnt-prediction/
│
├── app.py                    # 🚀 Main Streamlit entry point
├── model_training.py         # 🤖 ML training pipeline
├── generate_dataset.py       # 📦 Dataset generator
│
├── model.pkl                 # Saved XGBoost model
├── scaler.pkl                # Saved StandardScaler
├── model_meta.json           # Model metadata & results
│
├── dataset/
│   ├── exercise.csv          # Exercise features (15,000 records)
│   └── calories.csv          # Target calories
│
├── pages/
│   ├── predict.py            # 🏠 Home & prediction UI
│   ├── eda.py                # 📊 EDA & visualizations
│   ├── model_comparison.py   # 🤖 Model benchmarking
│   ├── history.py            # 📜 Session workout log
│   └── report.py             # 📄 PDF report generator
│
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Generate dataset (already done if dataset/ exists)
```bash
python generate_dataset.py
```

### 3. Train the models
```bash
python model_training.py
```

### 4. Run the web app
```bash
streamlit run app.py
```

---

## 🤖 Models Compared

| Model              | MAE (kcal) | RMSE (kcal) | R² Score |
|--------------------|-----------|------------|---------|
| Linear Regression  | 19.03     | 25.65      | 0.9811  |
| Random Forest      | 7.37      | 9.44       | 0.9974  |
| **XGBoost** ⭐     | **7.04**  | **8.90**   | **0.9977** |

---

## 📊 Features Used

| Feature       | Type        | Description                    |
|---------------|-------------|--------------------------------|
| Gender        | Categorical | Male (0) / Female (1)          |
| Age           | Numerical   | Years                          |
| Height        | Numerical   | Centimetres                    |
| Weight        | Numerical   | Kilograms                      |
| Duration      | Numerical   | Exercise minutes               |
| Heart Rate    | Numerical   | Beats per minute               |
| Body Temp     | Numerical   | Degrees Celsius                |
| BMI           | Derived     | Weight / Height²               |
| Effort Index  | Derived     | Heart Rate × Duration          |

---

## 🖥️ App Pages

| Page              | Description                                        |
|-------------------|----------------------------------------------------|
| 🏠 Home & Predict  | Enter stats → get instant calorie prediction        |
| 📊 EDA & Insights  | 6 interactive charts exploring the dataset          |
| 🤖 Model Comparison| R², MAE, RMSE side-by-side + feature importance     |
| 📜 Workout History | Log & track predictions across a session            |
| 📄 Export Report   | One-click PDF report for your project documentation |

---

## 🎓 Academic Details

- **Problem Type:** Supervised Regression
- **Algorithm:** XGBoost (eXtreme Gradient Boosting)
- **Evaluation Metrics:** R², MAE, RMSE
- **Train/Test Split:** 80% / 20%
- **Preprocessing:** StandardScaler normalization

---

*Built with Python · Scikit-learn · XGBoost · Streamlit · Plotly*
