import pandas as pd
import streamlit as st

def detect_columns(df):
    detected = {}
    date_keywords     = ['date','time','day','month','year','order','period','invoice']
    product_keywords  = ['product','item','name','description','title',
                         'goods','service','sku','model','brand']
    quantity_keywords = ['qty','quantity','units','count','amount',
                         'volume','sold','purchases','number']
    price_keywords    = ['price','sales','revenue','cost','value',
                         'amount','income','profit','total','earning']

    for col in df.columns:
        col_lower = col.lower().strip()

        # Detect date column
        if 'date' not in detected:
            if any(k in col_lower for k in date_keywords):
                try:
                    pd.to_datetime(df[col], errors='raise')
                    detected['date'] = col
                    continue
                except:
                    pass
            # Try parsing even without keyword
            if pd.api.types.is_object_dtype(df[col]):
                try:
                    parsed = pd.to_datetime(df[col], errors='coerce')
                    if parsed.notna().sum() > len(df) * 0.5:
                        detected['date'] = col
                        continue
                except:
                    pass

        # Detect product column
        if 'product' not in detected:
            if any(k in col_lower for k in product_keywords):
                if pd.api.types.is_object_dtype(df[col]):
                    detected['product'] = col
                    continue

        # Detect quantity column
        if 'quantity' not in detected:
            if any(k in col_lower for k in quantity_keywords):
                if pd.api.types.is_numeric_dtype(df[col]):
                    detected['quantity'] = col
                    continue

        # Detect price column
        if 'price' not in detected:
            if any(k in col_lower for k in price_keywords):
                if pd.api.types.is_numeric_dtype(df[col]):
                    detected['price'] = col
                    continue

    return detected

def load_data(uploaded_file):
    if uploaded_file is None:
        return None, "No file uploaded."

    filename = uploaded_file.name.lower()

    try:
        if filename.endswith('.csv') or filename.endswith('.tsv'):
            df = pd.read_csv(uploaded_file, encoding='latin1',
                             sep=None, engine='python')
        elif filename.endswith('.xlsx') or filename.endswith('.xls'):
            df = pd.read_excel(uploaded_file)
        elif filename.endswith('.json'):
            df = pd.read_json(uploaded_file)
        elif filename.endswith('.txt'):
            df = pd.read_csv(uploaded_file, encoding='latin1',
                             sep=None, engine='python')
        else:
            return None, (
                f"Unsupported file: '{uploaded_file.name}'. "
                f"Use CSV, TSV, XLSX, XLS, JSON, or TXT."
            )
    except Exception as e:
        return None, f"Error reading file: {e}"

    if df.empty:
        return None, "Dataset is empty."

    df.columns = df.columns.str.strip()

    # ── Auto detect columns ───────────────────────────────────────────────────
    detected = detect_columns(df)

    # ── Show what was detected in the UI ──────────────────────────────────────
    st.sidebar.markdown("---")
    st.sidebar.markdown("**🔍 Auto-detected columns**")

    rename_map = {}

    if 'date' in detected:
        st.sidebar.success(f"📅 Date → `{detected['date']}`")
        rename_map[detected['date']] = 'Order Date'
    else:
        st.sidebar.error("📅 Date column — not found")

    if 'product' in detected:
        st.sidebar.success(f"📦 Product → `{detected['product']}`")
        rename_map[detected['product']] = 'Product Name'
    else:
        st.sidebar.warning("📦 Product column — not found (optional)")

    if 'quantity' in detected:
        st.sidebar.success(f"🔢 Quantity → `{detected['quantity']}`")
        rename_map[detected['quantity']] = 'Quantity'
    else:
        st.sidebar.warning("🔢 Quantity — not found, defaulting to 1")
        df['Quantity'] = 1

    if 'price' in detected:
        st.sidebar.success(f"💰 Price → `{detected['price']}`")
        rename_map[detected['price']] = 'Unit Price'
    else:
        st.sidebar.error("💰 Price/Revenue column — not found")

    df.rename(columns=rename_map, inplace=True)

    # ── Add missing optional columns ──────────────────────────────────────────
    if 'Product Name' not in df.columns:
        df['Product Name'] = 'Unknown Product'
    if 'Quantity' not in df.columns:
        df['Quantity'] = 1

    # ── Check critical columns ─────────────────────────────────────────────────
    missing = []
    if 'Order Date' not in df.columns:
        missing.append('Date column')
    if 'Unit Price' not in df.columns:
        missing.append('Price/Revenue column')

    if missing:
        return None, (
            f"Could not detect: {missing}\n\n"
            f"Your file has these columns: {list(df.columns)}\n\n"
            f"Please rename one column to 'Date' and one to 'Sales' or 'Price'."
        )

    return df, None