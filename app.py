import streamlit as st
from modules.data_ingestion      import load_data
from modules.preprocessing       import preprocess
from modules.feature_engineering import engineer_features
from modules.eda                 import show_overview, show_monthly_trend, \
                                        show_top_products, show_regional_chart
from modules.ml_prediction       import train_and_predict

st.set_page_config(page_title="MarketLens", page_icon="telescope", layout="wide")

st.markdown("""
    <style>
    .icon { font-family: 'tabler-icons'; font-size: 20px; margin-right: 6px; vertical-align: middle; }
    </style>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css">
""", unsafe_allow_html=True)

st.markdown("""
    <h1 style='display:flex;align-items:center;gap:10px'>
        <i class='ti ti-telescope' style='font-size:32px'></i>
        MarketLens — Sales Analytics & Prediction
    </h1>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css">
    <h3><i class='ti ti-upload'></i> Upload Your Data</h3>
""", unsafe_allow_html=True)

uploaded_file = st.sidebar.file_uploader(
    "Upload your sales data",
    type=["csv", "tsv", "xlsx", "xls", "json", "txt"]
)

section = st.sidebar.radio("Navigate", ["Overview", "Visualizations", "Predictions"])

if uploaded_file:
    df_raw, error = load_data(uploaded_file)

    if error:
        st.error(error)
        st.stop()

    df_clean = preprocess(df_raw)
    df       = engineer_features(df_clean)

    if section == "Overview":
        show_overview(df)

    elif section == "Visualizations":
        show_monthly_trend(df)
        show_top_products(df)
        show_regional_chart(df)

    elif section == "Predictions":
        model_name = st.selectbox("Select Model", [
            "Linear Regression",
            "Decision Tree",
            "Random Forest",
            "Gradient Boosting"
        ])

        st.markdown("#### How many months to predict?")
        col1, col2 = st.columns([3, 1])
        with col1:
            future_months = st.slider("Drag to select months", 1, 24, 6)
        with col2:
            custom = st.number_input("Or type exact", min_value=1, max_value=60,
                                     value=future_months, step=1)

        final_months = max(future_months, custom)
        st.info(f"Predicting next {final_months} months using {model_name}")

        if st.button("Generate Prediction"):
            train_and_predict(df, model_name, final_months)

else:
    st.info("Upload a sales CSV file from the sidebar to get started.")
    st.markdown("""
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css">
        <div style='background:var(--background-color);padding:1rem;border-radius:8px;border:0.5px solid #ccc'>
            <p><i class='ti ti-calendar' style='font-size:16px'></i> <b>Order Date</b> — e.g. 01/01/2024</p>
            <p><i class='ti ti-package' style='font-size:16px'></i> <b>Product Name</b></p>
            <p><i class='ti ti-hash' style='font-size:16px'></i> <b>Quantity</b></p>
            <p><i class='ti ti-currency-rupee' style='font-size:16px'></i> <b>Unit Price / Sales</b></p>
            <p><i class='ti ti-map-pin' style='font-size:16px'></i> <b>Region</b> (optional)</p>
        </div>
    """, unsafe_allow_html=True)