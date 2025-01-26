import streamlit as st
import pandas as pd
from io import BytesIO

# Set page config to full screen
st.set_page_config(layout="wide")

# Load data from backend
@st.cache_data
def load_data_from_backend():
    file_path = "Alldata.csv"  # Update with the correct path
    if file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path)
    elif file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    else:
        return None
    return df


# Function to filter data
def filter_data(df, filters):
    for col, value in filters.items():
        if value:
            df = df[df[col].astype(str).str.contains(value, case=False, na=False)]
    return df

# Function to convert DataFrame to Excel for download
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    processed_data = output.getvalue()
    return processed_data

# Streamlit UI
st.title("Data Viewer and Exporter")
st.write("Here you can find all the raw data that is used in the other modules across the site. Filter the data using the picklists at the top and download data for that module or the whole site for your own analysis.", )

df = load_data_from_backend()
if df is not None:
    st.write("### Data Preview")
    st.dataframe(df.head())

    # Fixed columns for filtering
    filter_columns = ["Model", "Scenario", "Variable"]  # Update with actual column names

    st.write("### Filter Data")
    filters = {}
    cols = st.columns(len(filter_columns))
    filtered_df = df.copy()
    for idx, col in enumerate(filter_columns):
        if col in df.columns:
            options = [""] + filtered_df[col].astype(str).unique().tolist()
            filters[col] = cols[idx].selectbox(f"{col}", options)
            filtered_df = filter_data(filtered_df, {col: filters[col]})
    
    st.write("### Filtered Data")
    st.dataframe(filtered_df)


        # Button to download filtered data
        #if st.button("Download Filtered Data"):
    excel_data = to_excel(filtered_df)
    st.download_button(label="Download Excel", data=excel_data, file_name="filtered_data.xlsx", mime="application/vnd.ms-excel")
else:
    st.error("Error loading data from backend.")
