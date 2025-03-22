import pickle
from typing import Dict, Any, Tuple
import pandas as pd
def load_model(model_path: str) -> Tuple[Any, list]:
    """
    Load the trained model and feature names from pickle file
    
    Args:
        model_path: Path to the pickle file containing model and features
        
    Returns:
        Tuple containing model and feature names
        
    Raises:
        FileNotFoundError: If model file doesn't exist
        pickle.UnpicklingError: If model file is corrupted
    """
    try:
        with open(model_path, "rb") as f:
            data = pickle.load(f)
            return data["model"], data["features"]
    except FileNotFoundError:
        raise FileNotFoundError("Model file not found. Please ensure model.pkl exists in the current directory.")
    except pickle.UnpicklingError:
        raise pickle.UnpicklingError("Error loading model. The model file may be corrupted.")

def process_input_features(
    gender: str,
    age: str,
    occupation: int,
    city_category: str,
    stay_years: str,
    marital_status: str,
    product_category_1: int,
    product_category_2: str,
    product_category_3: str,
    feature_names: list
) -> pd.DataFrame:
    """
    Process user inputs into model-compatible features
    
    Args:
        Various user input parameters and feature names
        
    Returns:
        DataFrame with processed features
    """
    # Convert categorical variables
    gender_encoded = 1 if gender == "Male" else 0
    marital_status_encoded = 1 if marital_status == "Married" else 0
    
    # Handle optional product categories
    product_category_2_encoded = int(product_category_2) if product_category_2 != "None" else 0
    product_category_3_encoded = int(product_category_3) if product_category_3 != "None" else 0
    
    # Initialize input dictionary
    input_dict = {
        "Gender": gender_encoded,
        "Occupation": occupation,
        "Marital_Status": marital_status_encoded,
        "Product_Category_1": product_category_1,
        "Product_Category_2": product_category_2_encoded,
        "Product_Category_3": product_category_3_encoded,
    }
    
    # One-hot encoding for Age, City_Category, and Stay duration
    for category in feature_names:
        if category.startswith("Age_"):
            input_dict[category] = 1 if category == f"Age_{age}" else 0
        elif category.startswith("City_Category_"):
            input_dict[category] = 1 if category == f"City_Category_{city_category}" else 0
        elif category.startswith("Stay_In_Current_City_Years_"):
            input_dict[category] = 1 if category == f"Stay_In_Current_City_Years_{stay_years}" else 0
    
    return pd.DataFrame([input_dict])[feature_names]
