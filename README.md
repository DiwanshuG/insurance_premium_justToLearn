# Insurance Prediction App

This project is built **for learning purposes**.
It demonstrates a simple ML model integrated with a backend API and a Streamlit frontend.
It predict the client will take which type of premium based on certain factors.

> Demo video will be added later.

---

## 🚀 Setup Instructions

### 1. Create a virtual environment

```bash
python -m venv env
```

### 2. Activate environment

**Windows**

```bash
env\Scripts\activate
```

**Mac/Linux**

```bash
source env/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Project

### Step 1: Start the API server

```bash
uvicorn main:app --reload
```

### Step 2: Run the frontend (in a new terminal)

```bash
streamlit run frontend.py
```

---

## ⚠️ Important Note

Make sure the API is running on a **separate terminal/server** before starting the frontend.

---

##  Features

* Predict insurance charges
* FastAPI backend
* Streamlit frontend
* Pre-trained ML model included

---

## 🛠️ Tech Stack

* Python
* FastAPI
* Streamlit
* Scikit-learn
