"""Streamlit frontend for insurance premium category prediction."""

from __future__ import annotations

from typing import Any

import requests
import streamlit as st


OCCUPATIONS = [
	"retired",
	"freelancer",
	"student",
	"government_job",
	"business_owner",
	"unemployed",
	"private_job",
]

TIER_1_CITIES = [
	"Mumbai",
	"Delhi",
	"Bangalore",
	"Chennai",
	"Kolkata",
	"Hyderabad",
	"Pune",
]

TIER_2_CITIES = [
	"Jaipur",
	"Chandigarh",
	"Indore",
	"Lucknow",
	"Patna",
	"Ranchi",
	"Visakhapatnam",
	"Coimbatore",
	"Bhopal",
	"Nagpur",
	"Vadodara",
	"Surat",
	"Rajkot",
	"Jodhpur",
	"Raipur",
	"Amritsar",
	"Varanasi",
	"Agra",
	"Dehradun",
	"Mysore",
	"Jabalpur",
	"Guwahati",
	"Thiruvananthapuram",
	"Ludhiana",
	"Nashik",
	"Allahabad",
	"Udaipur",
	"Aurangabad",
	"Hubli",
	"Belgaum",
	"Salem",
	"Vijayawada",
	"Tiruchirappalli",
	"Bhavnagar",
	"Gwalior",
	"Dhanbad",
	"Bareilly",
	"Aligarh",
	"Gaya",
	"Kozhikode",
	"Warangal",
	"Kolhapur",
	"Bilaspur",
	"Jalandhar",
	"Noida",
	"Guntur",
	"Asansol",
	"Siliguri",
]

CITY_OPTIONS = sorted(set(TIER_1_CITIES + TIER_2_CITIES + ["Kota"]))


def compute_age_group(age: int) -> str:
	if age < 25:
		return "young"
	if age < 45:
		return "adult"
	if age < 60:
		return "middle_aged"
	return "senior"


def compute_city_tier(city: str) -> int:
	if city in TIER_1_CITIES:
		return 1
	if city in TIER_2_CITIES:
		return 2
	return 3


def compute_lifestyle_risk(smoker: bool, bmi: float) -> str:
	if smoker and bmi > 30:
		return "high"
	if smoker or bmi > 27:
		return "medium"
	return "low"


def predict(api_url: str, payload: dict[str, Any], timeout: int) -> requests.Response:
	return requests.post(api_url, json=payload, timeout=timeout)


st.set_page_config(
	page_title="Insurance Premium Predictor",
	page_icon="\U0001F4CA",
	layout="wide",
)

st.markdown(
	"""
	<style>
	.stApp {
		background: linear-gradient(180deg, #f7faf8 0%, #eef7f1 100%);
	}
	.block-container {
		padding-top: 1.5rem;
		padding-bottom: 1.5rem;
	}
	.hero {
		padding: 1rem 1.2rem;
		border-radius: 14px;
		background: linear-gradient(135deg, rgba(22, 101, 52, 0.12), rgba(20, 83, 45, 0.06));
		border: 1px solid rgba(22, 101, 52, 0.18);
	}
	.small-note {
		color: #374151;
		font-size: 0.92rem;
	}
	</style>
	""",
	unsafe_allow_html=True,
)

st.markdown(
	"""
	<div class="hero">
		<h2 style="margin:0; color:#14532d;">Insurance Premium Category Predictor</h2>
		<p style="margin:0.35rem 0 0 0; color:#1f2937;">
			Enter customer details, send them to your FastAPI model endpoint, and get the predicted premium band.
		</p>
	</div>
	""",
	unsafe_allow_html=True,
)

with st.sidebar:
	st.subheader("API Settings")
	api_url = st.text_input("Prediction Endpoint", value="http://127.0.0.1:8000/predict")
	timeout_seconds = st.slider("Request Timeout (seconds)", min_value=3, max_value=30, value=10)
	st.markdown(
		"<p class='small-note'>Run FastAPI first: <b>uvicorn main:app --reload</b></p>",
		unsafe_allow_html=True,
	)

left, right = st.columns(2)

with left:
	age = st.number_input("Age", min_value=1, max_value=119, value=30, step=1)
	weight = st.number_input("Weight (kg)", min_value=10.0, max_value=250.0, value=70.0, step=0.1)
	height = st.number_input("Height (m)", min_value=1.0, max_value=2.5, value=1.70, step=0.01, format="%.2f")
	smoker = st.toggle("Smoker", value=False)

with right:
	income_lpa = st.number_input(
		"Annual Income (LPA)",
		min_value=0.1,
		max_value=200.0,
		value=12.0,
		step=0.1,
	)
	city = st.selectbox("City", options=CITY_OPTIONS, index=0)
	occupation = st.selectbox("Occupation", options=OCCUPATIONS, index=1)

col_a, col_b, col_c = st.columns(3)
bmi = weight / (height**2)
age_group = compute_age_group(int(age))
city_tier = compute_city_tier(city)
lifestyle_risk = compute_lifestyle_risk(smoker, bmi)

with col_a:
	st.metric("BMI", f"{bmi:.2f}")
with col_b:
	st.metric("Age Group", age_group)
with col_c:
	st.metric("Lifestyle Risk", lifestyle_risk)

payload = {
	"age": int(age),
	"weight": float(weight),
	"height": float(height),
	"smoker": bool(smoker),
	"income_lpa": float(income_lpa),
	"city": city,
	"occupation": occupation,
}

if st.button("Predict Premium Category", type="primary", use_container_width=True):
	try:
		response = predict(api_url=api_url.strip(), payload=payload, timeout=timeout_seconds)
		response.raise_for_status()
		data = response.json()

		# Backend currently returns a non-standard key; support both this and cleaner keys.
		category = (
			data.get("predicted category")
			or data.get("predicted_category")
			or data.get("predicted category is  ")
			or next(iter(data.values()), "Unknown")
		)

		st.success(f"Predicted Premium Category: {category}")
		st.caption("Model features are generated in the backend (BMI, age group, lifestyle risk, city tier).")

	except requests.exceptions.ConnectionError:
		st.error("Could not connect to FastAPI. Check if the API server is running and the endpoint URL is correct.")
	except requests.exceptions.Timeout:
		st.error("Request timed out. Increase timeout or check API performance.")
	except requests.exceptions.HTTPError:
		error_text = response.text if "response" in locals() else "Unknown API error"
		st.error(f"API returned an error: {error_text}")
	except requests.exceptions.RequestException as exc:
		st.error(f"Request failed: {exc}")

with st.expander("Show request payload"):
	st.json(payload)

with st.expander("Derived features preview"):
	st.write(
		{
			"bmi": round(bmi, 2),
			"age_group": age_group,
			"lifestyle_risk": lifestyle_risk,
			"city_tier": city_tier,
		}
	)
