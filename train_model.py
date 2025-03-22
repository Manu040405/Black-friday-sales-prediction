import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Load dataset
file_path = "Data/BlackFridaySales.csv"  # Ensure this file is present
df = pd.read_csv(file_path)

# Selecting relevant features
features = ["Gender", "Age", "Occupation", "City_Category", "Stay_In_Current_City_Years", 
            "Marital_Status", "Product_Category_1", "Product_Category_2", "Product_Category_3"]

df = df.dropna()  # Drop missing values for simplicity
df = df[["Purchase"] + features]

# Encoding categorical variables
df["Gender"] = df["Gender"].map({"M": 1, "F": 0})
df["Marital_Status"] = df["Marital_Status"].astype(int)

# One-hot encoding for Age, City, and Stay duration
df = pd.get_dummies(df, columns=["Age", "City_Category", "Stay_In_Current_City_Years"], drop_first=True)

# Splitting data
X = df.drop("Purchase", axis=1)
y = df["Purchase"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Save feature names to ensure correct prediction input
feature_names = X.columns.tolist()

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Save the trained model with feature names
with open("model.pkl", "wb") as f:
    pickle.dump({"model": model, "features": feature_names}, f)

print("✅ Model Training Complete!")
print(f"📊 Features Used: {feature_names}")
