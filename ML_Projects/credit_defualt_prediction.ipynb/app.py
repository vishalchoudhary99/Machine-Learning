import streamlit as st
import numpy as np
import pickle
from pathlib import Path

# ----------------------------
# Page config & styling
# ----------------------------
st.set_page_config(
    page_title="Credit Default Prediction",
    page_icon="💳",
    layout="wide"
)

st.markdown("""
<style>
    .main-header {font-size: 2rem; font-weight: 700; margin-bottom: 0.5rem;}
    .sub-header {font-size: 1.2rem; font-weight: 600; margin-top: 1rem;}
    .metric-box {
        padding: 0.75rem;
        border-radius: 0.5rem;
        background-color: #f0f2f6;
        border: 1px solid #ddd;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Load model & threshold
# ----------------------------
@st.cache_resource
def load_model_and_threshold():
    model_path = Path(r"D:\MachineLearning.py\ML_Projects\credit_defualt_prediction.ipynb\model.pkl")
    threshold_path = Path(r"D:\MachineLearning.py\ML_Projects\credit_defualt_prediction.ipynb\optimal_threshold")

    with open(model_path, "rb") as f:
        model = pickle.load(f)
    with open(threshold_path, "rb") as f:
        optimal_threshold = pickle.load(f)
    return model, optimal_threshold

try:
    model, optimal_threshold = load_model_and_threshold()
except Exception as e:
    st.error(f"Error loading model or threshold: {e}")
    st.stop()

# ----------------------------
# Helper functions
# ----------------------------
def map_gender(val: str) -> int:
    return 1 if val == "Male" else 0

def map_education(val: str) -> int:
    mapping = {
        "Graduate School": 1,
        "University": 2,
        "High School": 3,
        "Others": 0
    }
    return mapping[val]

def map_marital(val: str) -> int:
    mapping = {
        "Married": 1,
        "Single": 2,
        "Others": 0
    }
    return mapping[val]

DELAY_OPTIONS = [
    "No Bill Generated",
    "Paid On Time",
    "Late But Not Overdue",
    "One Month",
    "Two Month",
    "Three Month",
    "Four Month",
    "Five Month",
    "Six Month",
    "Seven Month",
    "Eight Month"
]

DELAY_MAPPING = {
    "No Bill Generated": -2,
    "Paid On Time": -1,
    "Late But Not Overdue": 0,
    "One Month": 1,
    "Two Month": 2,
    "Three Month": 3,
    "Four Month": 4,
    "Five Month": 5,
    "Six Month": 6,
    "Seven Month": 7,
    "Eight Month": 8
}

def map_delay(val: str) -> int:
    return DELAY_MAPPING[val]

def format_inr(value: float) -> str:
    return f"₹{value:,.0f}"

def risk_label(pred_prob: float) -> str:
    if pred_prob < 0.2:
        return "🟢 Low Risk"
    elif pred_prob < 0.5:
        return "🟡 Medium Risk"
    else:
        return "🔴 High Risk"

# ----------------------------
# Title & intro
# ----------------------------
st.markdown('<div class="main-header">Credit Default Prediction</div>', unsafe_allow_html=True)
st.markdown(
    "Enter the customer’s credit and repayment details to estimate the probability of default."
)

# ----------------------------
# Input sections
# ----------------------------
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="sub-header">Customer Profile</div>', unsafe_allow_html=True)

    Limit_Bal = st.number_input(
        "Credit Card Limit (₹)",
        min_value=10000,
        max_value=3_000_000,
        step=5000,
        value=100000
    )

    Gender = st.selectbox("Gender", ["Male", "Female"])
    Gender = map_gender(Gender)

    Education = st.selectbox(
        "Education",
        ["Graduate School", "University", "High School", "Others"]
    )
    Education = map_education(Education)

    Marital_Status = st.selectbox(
        "Marital Status",
        ["Married", "Single", "Others"]
    )
    Marital_Status = map_marital(Marital_Status)

    Age = st.number_input("Age", min_value=18, max_value=100, step=1, value=30)

with col2:
    st.markdown('<div class="sub-header">Repayment Behavior (Apr–Sep)</div>', unsafe_allow_html=True)

    def delay_selector(month: str):
        return st.selectbox(f"{month} Delay", DELAY_OPTIONS, key=f"delay_{month}")

    Apr_Delay = map_delay(delay_selector("April"))
    May_Delay = map_delay(delay_selector("May"))
    Jun_Delay = map_delay(delay_selector("June"))
    Jul_Delay = map_delay(delay_selector("July"))
    Aug_Delay = map_delay(delay_selector("August"))
    Sep_Delay = map_delay(delay_selector("September"))

# ----------------------------
# Bills & Payments
# ----------------------------
st.markdown('<div class="sub-header">Monthly Bills & Payments (₹)</div>', unsafe_allow_html=True)

def bill_paid_inputs():
    cols = st.columns(3)
    months = ["April", "May", "June", "July", "August", "September"]
    bill_gen = {}
    amt_paid = {}

    for i, month in enumerate(months):
        col = cols[i % 3]
        with col:
            bill_gen[month] = st.number_input(
                f"Bill Generated – {month}",
                min_value=0,
                max_value=3_000_000,
                step=1000,
                value=0,
                key=f"bill_{month}"
            )
            amt_paid[month] = st.number_input(
                f"Amount Paid – {month}",
                min_value=0,
                max_value=3_000_000,
                step=1000,
                value=0,
                key=f"paid_{month}"
            )
    return bill_gen, amt_paid

bill_gen, amt_paid = bill_paid_inputs()

Bill_Gen_Apr = bill_gen["April"]
Bill_Gen_May = bill_gen["May"]
Bill_Gen_Jun = bill_gen["June"]
Bill_Gen_Jul = bill_gen["July"]
Bill_Gen_Aug = bill_gen["August"]
Bill_Gen_Sep = bill_gen["September"]

Amt_Paid_Apr = amt_paid["April"]
Amt_Paid_May = amt_paid["May"]
Amt_Paid_Jun = amt_paid["June"]
Amt_Paid_Jul = amt_paid["July"]
Amt_Paid_Aug = amt_paid["August"]
Amt_Paid_Sep = amt_paid["September"]

# ----------------------------
# Feature engineering
# ----------------------------
# Fix: Negative_Bill_Count logic (original had some mistakes)
Negative_Bill_Count = (
    int(Bill_Gen_Apr < 0) +
    int(Bill_Gen_May < 0) +
    int(Bill_Gen_Jun < 0) +
    int(Bill_Gen_Jul < 0) +
    int(Bill_Gen_Aug < 0) +
    int(Bill_Gen_Sep < 0)
)

Total_Bill = Bill_Gen_Apr + Bill_Gen_May + Bill_Gen_Jun + Bill_Gen_Jul + Bill_Gen_Aug + Bill_Gen_Sep
Total_Pay = Amt_Paid_Apr + Amt_Paid_May + Amt_Paid_Jun + Amt_Paid_Jul + Amt_Paid_Aug + Amt_Paid_Sep

Avg_Bill = Total_Bill / 6 if Total_Bill > 0 else 0
Avg_Pay = Total_Pay / 6 if Total_Pay > 0 else 0

Payment_Bill_Ratio = round(Avg_Pay / Avg_Bill, 2) if Avg_Bill > 0 else 0
Credit_Utilization = round(Avg_Bill / Limit_Bal, 2) if Limit_Bal > 0 else 0

delays = np.array([Apr_Delay, May_Delay, Jun_Delay, Jul_Delay, Aug_Delay, Sep_Delay])
count_overdue = int(np.sum(delays > 0))

Max_Delay = int(delays.max())
Avg_Delay = round(float(np.sum(np.where(delays > 0, delays, 0)) / count_overdue), 2) if count_overdue > 0 else 0
Delay_Count = count_overdue
On_time_count = 6 - count_overdue

No_Bill_Count = int(np.sum(delays == -2))
No_Overdue_Count = int(np.sum(delays == 0))

Maximum_Bill = max([Bill_Gen_Apr, Bill_Gen_May, Bill_Gen_Jun, Bill_Gen_Jul, Bill_Gen_Aug, Bill_Gen_Sep])

# Feature vector in the same order as your model expects
query = np.array([
    Limit_Bal, Gender, Education, Marital_Status, Age,
    Sep_Delay, Aug_Delay, Jul_Delay, Jun_Delay, May_Delay, Apr_Delay,
    Bill_Gen_Sep, Bill_Gen_Aug, Bill_Gen_Jul, Bill_Gen_Jun, Bill_Gen_May, Bill_Gen_Apr,
    Amt_Paid_Sep, Amt_Paid_Aug, Amt_Paid_Jul, Amt_Paid_Jun, Amt_Paid_May, Amt_Paid_Apr,
    Negative_Bill_Count,
    Total_Bill,
    Total_Pay,
    Avg_Bill,
    Avg_Pay,
    Payment_Bill_Ratio,
    Credit_Utilization,
    Max_Delay,
    Avg_Delay,
    Delay_Count,
    On_time_count,
    No_Bill_Count,
    No_Overdue_Count,
    Maximum_Bill
]).reshape(1, 37)

# ----------------------------
# Prediction & interactive output
# ----------------------------
st.markdown("---")
st.markdown('<div class="sub-header">Prediction</div>', unsafe_allow_html=True)

if st.button("Predict Default", type="primary", use_container_width=True):
    pred_prob = float(model.predict_proba(query)[0, 1])
    prediction = int(pred_prob >= optimal_threshold)

    st.markdown("### Result")

    col_a, col_b = st.columns([2, 1])

    with col_a:
        if prediction == 0:
            st.success("🟢 Customer is NOT likely to default.")
        else:
            st.error("🔴 Customer is likely to default.")

        st.write(f"**Probability of Default:** {pred_prob * 100:.2f}%")

        risk_text = risk_label(pred_prob)
        st.write(f"**Risk Level:** {risk_text}")

        # Probability bar
        st.progress(pred_prob)

    with col_b:
        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
        st.write("**Key Indicators**")
        st.write(f"Credit Utilization: {Credit_Utilization:.2f}")
        st.write(f"Max Delay (months): {Max_Delay}")
        st.write(f"Delayed Months: {Delay_Count}")
        st.write(f"On-time Months: {On_time_count}")
        st.write(f"Avg Bill / Limit: {Avg_Bill:,}")
        st.markdown('</div>', unsafe_allow_html=True)

    with st.expander("See detailed explanation"):
        if prediction == 0:
            st.write(
                "The customer has a relatively low estimated probability of default based on the "
                "entered financial and repayment history."
            )
        else:
            st.write(
                "The customer has a high estimated probability of default. "
                "Additional financial assessment is recommended before granting new credit."
            )

# Optional: show feature vector for debugging
with st.expander("Debug: Feature vector sent to model"):
    st.write(query)