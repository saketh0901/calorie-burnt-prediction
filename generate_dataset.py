import pandas as pd
import numpy as np

np.random.seed(42)
n = 15000

user_ids = np.arange(1, n+1)
genders = np.random.choice(['male', 'female'], n)
ages = np.random.randint(18, 70, n)
heights = np.where(genders == 'male',
    np.random.normal(175, 8, n),
    np.random.normal(163, 7, n))
weights = np.where(genders == 'male',
    np.random.normal(80, 12, n),
    np.random.normal(65, 10, n))
durations = np.random.randint(5, 120, n)
heart_rates = np.random.randint(65, 185, n)
body_temps = np.random.uniform(37.0, 41.5, n)

# Physics-inspired calorie formula with noise
gender_factor = np.where(genders == 'male', 1.0, 0.85)
calories = (
    gender_factor *
    (0.074 * ages +
     0.271 * weights +
     0.334 * heart_rates +
     0.481 * durations * (body_temps - 36.5) +
     durations * 4.5 +
     np.random.normal(0, 8, n))
).clip(10, None)

exercise_df = pd.DataFrame({
    'User_ID': user_ids,
    'Gender': genders,
    'Age': ages.astype(int),
    'Height': heights.round(1),
    'Weight': weights.round(1),
    'Duration': durations,
    'Heart_Rate': heart_rates,
    'Body_Temp': body_temps.round(1)
})

calories_df = pd.DataFrame({
    'User_ID': user_ids,
    'Calories': calories.round(2)
})

exercise_df.to_csv('/home/claude/calorie-burnt-prediction/dataset/exercise.csv', index=False)
calories_df.to_csv('/home/claude/calorie-burnt-prediction/dataset/calories.csv', index=False)
print("Dataset generated:", exercise_df.shape, calories_df.shape)
print(exercise_df.head())
