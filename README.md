# 🛍️ Black Friday Sales Prediction App

This is a **Streamlit-based web app** that predicts customer purchase amounts during Black Friday sales based on user demographics and product information. It uses a machine learning model trained on real sales data to provide instant predictions.

🌐 **Live Demo**: [Click here to use the app](https://black-friday-streamlit-app.onrender.com)  
📁 **Dataset Used**: [Black Friday Sales Dataset – Kaggle](https://www.kaggle.com/datasets/sdolezel/black-friday)

---

## 🚀 Features

- 🧠 Trained Machine Learning Model (e.g., Random Forest)
- 👤 Login and Signup functionality
- 📊 Real-time prediction of purchase amounts
- 📈 Visual dashboard with charts and inputs
- 🌍 Deployed seamlessly using Render

---

## 📁 Project Structure

. ├── app.py # Main Streamlit app (all logic here) ├── model.pkl # Trained ML model ├── train_model.py # Script to train the model ├── requirements.txt # Python packages required ├── render.yaml # Render deployment file ├── Data/ │ └── BlackFridaySales.csv # Dataset used for model training

yaml
Copy
Edit

---

## 🧠 How It Works

1. Users sign up or log in  
2. Enter customer and product information  
3. The model processes inputs and predicts the **purchase amount**  
4. Prediction is shown in a clean interface  

---

## 🛠 Tech Stack

- **Frontend/UI**: Streamlit  
- **ML/Backend**: Scikit-learn, Pandas, NumPy  
- **Deployment**: Render  
- **Model**: Trained using `RandomForestRegressor`

---

## 💻 Run It Locally

### 1. Clone the repository

```bash
git clone https://github.com/Manu040405/Black-friday-sales-prediction.git
cd Black-friday-sales-prediction
2. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
3. Run the app
bash
Copy
Edit
streamlit run app.py
🚀 Deployment on Render
This app uses a render.yaml file for automatic deployment via Render's Blueprint feature.

render.yaml
yaml
Copy
Edit
services:
  - type: web
    name: black-friday-streamlit-app
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: streamlit run app.py --server.port=$PORT --server.enableCORS=false
    repo: https://github.com/Manu040405/Black-friday-sales-prediction
    branch: main
    autoDeploy: true
requirements.txt
txt
Copy
Edit
streamlit
pandas
numpy
scikit-learn
matplotlib
plotly
📊 Data & Model Info
Dataset: Black Friday Sales Dataset from Kaggle

Target Variable: Purchase (amount spent)

Features Used: Age, Gender, Occupation, Product Category, City Category, Stay Duration, etc.

Model Used: RandomForestRegressor (or similar)

🙌 Acknowledgements
Streamlit – UI framework

Render – Hosting & Deployment

Kaggle Black Friday Dataset

📫 Contact
Created by Manu040405
