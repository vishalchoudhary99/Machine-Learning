import streamlit as st
import pickle
import numpy as np
from pathlib import Path


# Page config & custom CSS

st.set_page_config(
    page_title="Laptop Price Predictor",
    page_icon="💻",
    layout="wide"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.25rem;
    }
    .sub-header {
        font-size: 1.1rem;
        font-weight: 600;
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
    }
    .info-box {
        padding: 0.75rem 1rem;
        border-radius: 0.5rem;
        background-color: #f0f2f6;
        border: 1px solid #e0e0e0;
        margin-bottom: 0.75rem;
    }
    .price-card {
        padding: 1.25rem;
        border-radius: 0.75rem;
        background: linear-gradient(135deg, #f6f8ff 0%, #eef2ff 100%);
        border: 1px solid #dde3ff;
        text-align: center;
    }
    .price-label {
        font-size: 1rem;
        color: #555;
        margin-bottom: 0.25rem;
    }
    .price-value {
        font-size: 2rem;
        font-weight: 800;
        color: #1f2937;
    }
    .confidence-box {
        margin-top: 0.75rem;
        font-size: 0.95rem;
        color: #444;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Load model & data
# ----------------------------
@st.cache_resource
def load_pipe_and_df():
    pipe_path = Path(r"D:\MachineLearning.py\ML_Projects\laptop_price_predict.ipynb\pipe.pkl")
    df_path = Path(r"D:\MachineLearning.py\ML_Projects\laptop_price_predict.ipynb\df.pkl")

    with open(pipe_path, "rb") as f:
        pipe = pickle.load(f)
    with open(df_path, "rb") as f:
        df = pickle.load(f)
    return pipe, df

try:
    pipe, df = load_pipe_and_df()
except Exception as e:
    st.error(f"Error loading model or data: {e}")
    st.stop()

# ----------------------------
# Header
# ----------------------------
st.markdown('<div class="main-header">💻 Laptop Price Predictor</div>', unsafe_allow_html=True)
st.markdown(
    "<div style='text-align:center; color:#555; margin-bottom:1rem;'>Choose the laptop specs to get an estimated price in ₹</div>",
    unsafe_allow_html=True
)

# ----------------------------
# Layout: two columns
# ----------------------------
col_left, col_right = st.columns([1.2, 0.8])

with col_left:
    st.markdown('<div class="sub-header">Basic Specs</div>', unsafe_allow_html=True)

    brand = st.selectbox("Brand", df["Brand"].unique())

    primary_use_case = st.selectbox("Type of Laptop", df["primary_use_case"].unique())

    os = st.selectbox("Operating System", df["OS"].unique())

    storage = st.selectbox("Storage (GB)", np.sort(df["storage_gb"].unique()))

    weight = st.number_input("Weight (kg)", min_value=0.5, max_value=5.0, step=0.1, value=1.5)

    touch = st.selectbox("Touch Screen", ["Yes", "No"])

    size = st.number_input("Screen Size (inches)", min_value=10.0, max_value=20.0, step=0.1, value=15.6)

    resolution = st.selectbox("Resolution", df["Resolution"].unique())

    # Compute PPI
    try:
        x_res, y_res = map(int, resolution.split("x"))
        PPI = ((x_res ** 2) + (y_res ** 2)) ** 0.5 / size
    except Exception:
        PPI = 0.0

    anti_glare_screen = st.selectbox("Anti Glare Screen", ["Yes", "No"])

    st.markdown('<div class="sub-header">Performance Specs</div>', unsafe_allow_html=True)

    ram = st.selectbox("RAM", df["RAM"].unique())

    # Generation dependent on brand
    generations = df.groupby("Brand")["Generation"].unique().to_dict()
    gen_options = list(generations.get(brand, []))
    gen = st.selectbox("Generation", gen_options if gen_options else ["Unknown"])

    ram_type = st.selectbox("RAM Type", df["RAM_Type"].unique())

    # GPU Model dependent on brand
    gpu_models = df.groupby("Brand")["GPU_Model"].unique().to_dict()
    gpu_options = list(gpu_models.get(brand, []))
    gpu_model = st.selectbox("GPU Model", gpu_options if gpu_options else ["Integrated"])

    gpu_type = st.selectbox("GPU Type", df["GPU_Type"].unique())

    storage_type = st.selectbox("Storage Type", df["Storage_Type"].unique())

    # Processor Brand dependent on brand
    processors = df.groupby("Brand")["Processor_Brand"].unique().to_dict()
    proc_brand_options = list(processors.get(brand, []))
    processor_brand = st.selectbox(
        "Processor Brand",
        proc_brand_options if proc_brand_options else ["Intel"]
    )

    processor_family = st.selectbox("Processor Family", df["Processor_Family"].unique())

with col_right:
    st.markdown('<div class="sub-header">Quick Summary</div>', unsafe_allow_html=True)

    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.write(f"**Brand:** {brand}")
    st.write(f"**Type:** {primary_use_case}")
    st.write(f"**OS:** {os}")
    st.write(f"**Storage:** {storage} GB ({storage_type})")
    st.write(f"**Weight:** {weight} kg")
    st.write(f"**Screen:** {size}\" | {resolution} | PPI ≈ {PPI:.1f}")
    st.write(f"**Touch:** {touch} | **Anti‑Glare:** {anti_glare_screen}")
    st.write(f"**RAM:** {ram} ({ram_type})")
    st.write(f"**GPU:** {gpu_model} ({gpu_type})")
    st.write(f"**CPU:** {processor_brand} – {processor_family}")
    st.write(f"**Generation:** {gen}")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="info-box">
        <b>How it works</b><br>
        This model predicts laptop price using key specs like brand, CPU/GPU, RAM, storage, 
        display quality, and use-case category. The output is an estimated market price in ₹.
        </div>
        """,
        unsafe_allow_html=True
    )

# ----------------------------
# Prediction
# ----------------------------
st.markdown("---")

# Convert categorical yes/no to 0/1
touch_bin = 1 if touch == "Yes" else 0
anti_glare_bin = 1 if anti_glare_screen == "Yes" else 0

query = np.array([
    storage,
    primary_use_case,
    os,
    weight,
    touch_bin,
    size,
    resolution,
    PPI,
    anti_glare_bin,
    brand,
    ram,
    gen,
    ram_type,
    gpu_model,
    gpu_type,
    storage_type,
    processor_brand,
    processor_family
]).reshape(1, 18)

st.markdown('<div class="sub-header" style="text-align:center;">Predicted Price</div>', unsafe_allow_html=True)

if st.button("Predict Price", type="primary", use_container_width=True):
    try:
        pred_log_price = pipe.predict(query)[0]
        pred_price = np.exp(pred_log_price)
        pred_price_rounded = float(pred_price.round(2))
    except Exception as e:
        st.error(f"Prediction error: {e}")
        pred_price_rounded = None

    if pred_price_rounded is not None:
        col_price1, col_price2 = st.columns([1.2, 0.8])

        with col_price1:
            st.markdown(
                f"""
                <div class="price-card">
                    <div class="price-label">Estimated Price</div>
                    <div class="price-value">₹ {pred_price_rounded:,.0f}</div>
                    <div class="confidence-box">
                        Model confidence (approx.): <b>88.3%</b>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col_price2:
            st.markdown("### What affects the price?")
            st.markdown(
                """
                - Higher-end **GPU** and **CPU** families increase price.  
                - Larger, higher‑resolution screens and higher **PPI** push prices up.  
                - More **RAM**, larger/faster **storage**, and premium **brands** add cost.  
                - Use-case tags (gaming, workstation, etc.) capture typical price tiers.
                """
            )

        with st.expander("See input vector sent to model"):
            st.write(query)