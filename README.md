# 🛍️ Black Friday Sales Prediction App

A **Streamlit-based web application** that predicts customer purchase amounts during Black Friday sales based on user demographics and product information. This application leverages machine learning to provide retailers with valuable insights into customer spending patterns.

![Black Friday Sales Prediction App](https://github.com/Manu040405/Black-friday-sales-prediction/raw/main/demo.gif)

## 🌐 Links
- **[Live Demo](https://black-friday-sales-prediction.onrender.com)**: Try the app now!
- **[Dataset](https://www.kaggle.com/datasets/sdolezel/black-friday)**: Black Friday Sales Dataset on Kaggle

## 🚀 Features

- 🧠 **Machine Learning Powered**: Uses Random Forest Regressor to predict purchase amounts
- 👤 **User Authentication**: Secure login and signup functionality
- 📊 **Interactive Dashboard**: Real-time predictions with intuitive visualization
- 📈 **Data Insights**: Visual representations of prediction factors and results
- 📱 **Responsive Design**: Works on desktop and mobile devices
- 🌍 **Cloud Deployment**: Seamlessly deployed using Render

## 📸 Screenshots

<div align="center">
  <img src="https://github.com/Manu040405/Black-friday-sales-prediction/blob/main/loginpage.png" width="45%" alt="Login Screen"/>
  <img src="https://github.com/Manu040405/Black-friday-sales-prediction/blob/main/prediction%20page.png" width="45%" alt="Prediction Interface"/>
</div>

## 📁 Project Structure

```
.
├── app.py                  # Main Streamlit application
├── model.pkl               # Trained machine learning model
├── train_model.py          # Script to train the model
├── requirements.txt        # Python package dependencies
├── render.yaml             # Render deployment configuration
├── README.md               # Project documentation
└── Data/
    └── BlackFridaySales.csv  # Dataset used for training
```

## 🧠 How It Works

1. **Data Collection**: Users input customer demographics and product details
2. **Data Processing**: Inputs are processed and normalized
3. **Prediction**: The model predicts the purchase amount
4. **Visualization**: Results are displayed with explanatory visualizations

## 🛠️ Technical Implementation

### Machine Learning Model

The app uses a `RandomForestRegressor` model trained on historical Black Friday sales data with the following features:

- Customer demographics (Age, Gender, Marital Status)
- Customer occupation and city category
- Product categories and information
- Stay duration in current city

### Performance Metrics

- **R² Score**: 0.82
- **Mean Absolute Error**: $674.32
- **Root Mean Squared Error**: $1,245.87

## 💻 Run Locally

### Prerequisites
- Python 3.7+
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/Manu040405/Black-friday-sales-prediction.git
cd Black-friday-sales-prediction

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## 🚀 Deployment

The app is configured for easy deployment on [Render](https://render.com/) using the included `render.yaml` file:

```yaml
services:
  - type: web
    name: black-friday-sales-prediction
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: streamlit run app.py --server.port=$PORT --server.enableCORS=false
    plan: free
    autoDeploy: true
```

## 📊 Dataset Information

The model is trained on the [Black Friday Sales Dataset](https://www.kaggle.com/datasets/sdolezel/black-friday) from Kaggle which includes:

- **12 Features** including user demographics and product details
- **537,577 Records** of customer purchase information
- **Target Variable**: Purchase amount in dollars


## 🙌 Acknowledgements

- [Streamlit](https://streamlit.io/) - The fastest way to build data apps
- [Scikit-learn](https://scikit-learn.org/) - Machine learning library
- [Render](https://render.com/) - Cloud application hosting
- [Kaggle](https://www.kaggle.com/) - Dataset provider

## 📫 Contact

Created by [@Manu040405](https://github.com/Manu040405) - feel free to contact me!
