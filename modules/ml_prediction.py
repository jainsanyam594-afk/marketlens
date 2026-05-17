import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def prepare_features(df):
    monthly = df.groupby(['Year', 'Month'])['Total Revenue'].sum().reset_index()
    monthly = monthly.sort_values(['Year', 'Month']).reset_index(drop=True)
    monthly['TimeIndex'] = range(len(monthly))
    return monthly

def train_and_predict(df, model_name, future_months):
    monthly = prepare_features(df)
    
    if len(monthly) < 5:
        st.warning("⚠️ Insufficient training data (need at least 5 months).")
        return

    if future_months > len(monthly):
        st.warning(
            f"⚠️ You're predicting {future_months} months but only have "
            f"{len(monthly)} months of training data. "
            f"Accuracy may decrease for far-future predictions."
        )
    
    X = monthly[['TimeIndex', 'Month', 'Year']]
    y = monthly['Total Revenue']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False
    )
    
    # Choose model
    if model_name == "Linear Regression":
        model = LinearRegression()
    else:
        model = DecisionTreeRegressor(max_depth=5, random_state=42)
    
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    # Metrics
    mae  = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2   = r2_score(y_test, y_pred)
    
    st.subheader("📉 Model Performance")
    c1, c2, c3 = st.columns(3)
    c1.metric("MAE",  f"₹{mae:,.2f}")
    c2.metric("RMSE", f"₹{rmse:,.2f}")
    c3.metric("R² Score", f"{r2:.3f}")
    
    # Generate future predictions
    last_idx   = monthly['TimeIndex'].max()
    last_year  = monthly['Year'].iloc[-1]
    last_month = monthly['Month'].iloc[-1]
    
    future_rows = []
    for i in range(1, future_months + 1):
        m = (last_month + i - 1) % 12 + 1
        y = last_year + (last_month + i - 1) // 12
        future_rows.append({'TimeIndex': last_idx + i, 'Month': m, 'Year': y})
    
    future_df   = pd.DataFrame(future_rows)
    future_pred = model.predict(future_df)
    
    # Plot
    st.subheader("🔮 Sales Forecast")
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(monthly['TimeIndex'], monthly['Total Revenue'],
            label='Historical', marker='o', color='steelblue')
    ax.plot(future_df['TimeIndex'], future_pred,
            label='Predicted', marker='s', linestyle='--', color='orange')
    ax.set_xlabel("Time Index (Months)")
    ax.set_ylabel("Revenue (₹)")
    ax.set_title(f"Sales Prediction — {model_name}")
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)
    
    # Show prediction table
    future_df['Predicted Revenue'] = future_pred.round(2)
    st.dataframe(future_df[['Month', 'Year', 'Predicted Revenue']])