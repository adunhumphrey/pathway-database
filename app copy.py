import streamlit as st
import pandas as pd
from io import BytesIO

# Set page config to full screen
st.set_page_config(layout="wide")

# Load data with caching to prevent reloading
@st.cache_data
def load_data():
    file_path = "Alldata.csv"  # Update with the correct path
    dtype_dict = {str(year): 'float32' for year in range(1995, 2022)}  # Reduce memory usage
    df = pd.read_csv(file_path, dtype=dtype_dict, low_memory=False)
    return df

# Function to filter data efficiently
def filter_data(df, filters):
    for col, value in filters.items():
        if value:
            df = df[df[col].astype(str).str.contains(value, case=False, na=False)]
    return df

# Convert DataFrame to Excel for download (memory efficient)
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()

# Load data
df = load_data()

# Sidebar Navigation for Multiple Datasets
st.sidebar.title("Data Selection")
data_option = st.sidebar.selectbox("Choose Dataset", ["Dataset 1", "Dataset 2", "Dataset 3"])

if data_option == "Dataset 1":
    filter_columns = ["Model", "Scenario", "Region", "Variable", "Unit"]
    year_columns = [col for col in df.columns if col.isdigit()]  # Extract year columns
elif data_option == "Dataset 2":
    filter_columns = ["Product", "Category", "Region"]
    year_columns = [col for col in df.columns if col.isdigit()]
elif data_option == "Dataset 3":
    filter_columns = ["Country", "Sector", "Indicator"]
    year_columns = [col for col in df.columns if col.isdigit()]

st.write(f"### Viewing: {data_option}")

# Filtering UI
st.write("#### Apply Filters")
filters = {}
cols = st.columns(len(filter_columns))
for idx, col in enumerate(filter_columns):
    if col in df.columns:
        options = [""] + df[col].astype(str).unique().tolist()
        filters[col] = cols[idx].selectbox(f"{col}", options)

# Filter Year Range Selection
start_year, end_year = st.select_slider(
    "Select Year Range",
    options=year_columns,
    value=(year_columns[0], year_columns[-1])
)

# Apply Filters
filtered_df = filter_data(df, filters)
filtered_df = filtered_df[['Model', 'Scenario', 'Region', 'Variable', 'Unit'] + 
                          list(map(str, range(int(start_year), int(end_year) + 1)))]

# Paginate Data for Performance Optimization
st.write("#### Filtered Data (Paginated)")
page_size = 1000
total_rows = len(filtered_df)
page_number = st.number_input("Page Number", min_value=1, max_value=(total_rows // page_size) + 1, step=1)
start_row = (page_number - 1) * page_size
end_row = start_row + page_size

st.dataframe(filtered_df.iloc[start_row:end_row])  # Show paginated data

# Download Filtered Data
st.write("#### Download Filtered Data")
excel_data = to_excel(filtered_df)
st.download_button("Download Excel", data=excel_data, file_name=f"{data_option}_filtered_data.xlsx")

st.success("Data filtered and displayed successfully!")
