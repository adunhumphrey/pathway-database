import streamlit as st
import pandas as pd
from io import BytesIO

# Set page config to full screen
st.set_page_config(layout="wide")

# Function to load data for preview (only first 1000 rows to avoid huge data loads)
@st.cache_data
def load_data_preview(file_path):
    if file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path, nrows=1000)  # Only load a preview of 1000 rows
    elif file_path.endswith('.csv'):
        df = pd.read_csv(file_path, nrows=1000)  # Only load a preview of 1000 rows
    else:
        return None
    return df

# Function to load full data (for applying filters)
@st.cache_data
def load_full_data(file_path):
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
        if value and col in df.columns:
            df = df[df[col].astype(str).str.contains(value, case=False, na=False)]
    return df

# Function to filter based on year range (specific to Dataset 1)
def filter_by_year(df, filter_columns, start_year, end_year):
    year_columns = [col for col in df.columns if col.isdigit()]
    year_columns = sorted(year_columns, key=int)
    selected_years = [year for year in year_columns if start_year <= int(year) <= end_year]
    return df[filter_columns + selected_years]

# Function to convert DataFrame to Excel for download
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    processed_data = output.getvalue()
    return processed_data

# Streamlit UI
st.title("Data Explorer")
st.write("Here you can find all the raw data that is used in the other modules across the site. Filter the data using the picklists at the top and download data for that module or the whole site for your own analysis.")

# Define tabs for multiple data sources
tabs = st.tabs(["IPCC", "Cross-Sector Pathways", "Power Sector", "Aviation", "Building", "Industry"])

# File paths and filter columns for different datasets
datasets_info = {
    "IPCC": {
        "file_path": "C1-3_summary_2050_variable.csv",
        "filter_columns": ["Category", "Model", "Scenario", "Region", "Variable", "Unit"],
        "apply_year_filter": True
    },
    "Cross-Sectional Pathways": {
        "file_path": "AllData.csv",
        "filter_columns": ["Model", "Scenario", "Region", "Variable",],
        
        "apply_year_filter": True
    },
    "Power": {
        "file_path": "Pathway Database - Updated 2024-205.xlsx",
        "filter_columns": ["Metric","Model", "Scenario", "Variable"],
        "apply_year_filter": False
    },
    "Aviation": {
        "file_path": "2.csv",
        "filter_columns": ["Model", "Scenario"],
        "apply_year_filter": False
    },
    "Building": {
        "file_path": "3.csv",
        "filter_columns": ["Model", "Scenario"],
        "apply_year_filter": False
    },
    "Industry": {
        "file_path": "4.csv",
        "filter_columns": ["Model", "Scenario"],
        "apply_year_filter": False
    }
}

# Iterate over each tab and display corresponding data
for idx, tab in enumerate(tabs):
    dataset_name = list(datasets_info.keys())[idx]
    dataset_info = datasets_info[dataset_name]

    with tab:
        st.subheader(f"View and Filter {dataset_name}")
        
        # Load data preview (first 1000 rows only)
        file_path = dataset_info["file_path"]
        df_preview = load_data_preview(file_path)

        if df_preview is not None:
            st.write("### Data Preview")
            st.dataframe(df_preview.head())

            # Load full data for filtering purposes (without limiting to preview rows)
            df_full = load_full_data(file_path)

            # Filtering UI based on the full data columns (not preview)
            st.write("### Filter Data")
            filters = {}
            filter_columns = dataset_info["filter_columns"]
            cols = st.columns(len(filter_columns))

            selected_values = {}  # For storing selected filter values

            # Update filter options dynamically based on previous selections
            for i, col in enumerate(filter_columns):
                if col in df_full.columns:
                    options = [""] + df_full[col].astype(str).unique().tolist()
                    selected_values[col] = cols[i].selectbox(f"{col}", options, key=f"{col}_{idx}")

                    # Apply the filter to the dataset
                    if selected_values[col]:
                        df_full = df_full[df_full[col].astype(str).str.contains(selected_values[col], case=False, na=False)]

            # Add year range filters for 'AllData' dataset or any dataset requiring year filtering
            if dataset_info["apply_year_filter"]:
                # Get list of years from the dataset
                year_columns = [col for col in df_full.columns if col.isdigit()]
                year_columns = sorted(year_columns, key=int)  # Sort years in ascending order

                # Dropdown for Start Year
                start_year = st.selectbox(
                    "Select Start Year:",
                    options=year_columns,
                    index=0,  # Default to the first year
                    key=f"start_year_{dataset_name}_{idx}"
                )

                # Dropdown for End Year
                end_year = st.selectbox(
                    "Select End Year:",
                    options=year_columns,
                    index=len(year_columns)-1,  # Default to the last year
                    key=f"end_year_{dataset_name}_{idx}"
                )

                # Ensure end year is greater than or equal to start year
                if int(end_year) < int(start_year):
                    st.error("End Year must be greater than or equal to Start Year.")
                    end_year = start_year

                # Apply the year filter to the dataset
                df_full = filter_by_year(df_full, filter_columns, int(start_year), int(end_year))

            # Button to load full data and apply filters
            if st.button("Apply Filters", key=f"apply_filters_{dataset_name}_{idx}"):
                # Show filtered data
                st.write("### Filtered Data")
                st.dataframe(df_full.head(10))

                # Button to download filtered data
                excel_data = to_excel(df_full)
                st.download_button(
                    label="Download Excel",
                    data=excel_data,
                    file_name=f"{dataset_name}_filtered_data.xlsx",
                    mime="application/vnd.ms-excel",
                    key=f"download_button_{dataset_name}_{idx}"  # Ensure unique key for download button
                )
        else:
            st.error("Error loading data preview.")
