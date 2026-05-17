def engineer_features(df):
    df = df.copy()

    df['Total Revenue'] = df['Quantity'] * df['Unit Price']
    df['Month']         = df['Order Date'].dt.month
    df['Year']          = df['Order Date'].dt.year
    df['MonthYear']     = df['Order Date'].dt.to_period('M').astype(str)

    return df
