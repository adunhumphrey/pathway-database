import streamlit as st
import pandas as pd
import os
import base64
import docx
from io import BytesIO
from io import BytesIO
from streamlit import session_state as ss
import plotly.express as px
from streamlit_pdf_viewer import pdf_viewer
 

# Set page title and wide layout
st.set_page_config(page_title="My Streamlit App", layout="wide")

# Function to load data preview (first 100 rows)
@st.cache_data
def load_data_preview(file_path):
    try:
        if file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path, nrows=100, engine='openpyxl',)
        elif file_path.endswith('.csv'):
            df = pd.read_csv(file_path, encoding="utf-8", nrows=100)
        else:
            return None
        return df
    except FileNotFoundError:
        st.warning(f"File not found: {file_path}. Upload it below if missing.")
        return None
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        return None

# Function to load full dataset
@st.cache_data
def load_full_data(file_path,sheet, skip_row):
    try:
        if file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path, engine='openpyxl')
        elif file_path.endswith('.csv'):
            df = pd.read_csv(file_path, encoding="utf-8")
        elif file_path.endswith("Out.xlsx"):
            df = pd.read_excel(file_path, engine='openpyxl',sheet_name=sheet, skiprows=skip_row)
        else:
            return None
        return df
    except FileNotFoundError:
        st.warning(f"File not found: {file_path}. Upload it below if missing.")
        return None
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        return None

# Function to filter data
def filter_data(df, filters):
    for col, value in filters.items():
        if value and col in df.columns:
            df = df[df[col].astype(str).str.contains(value, case=False, na=False)]
    return df

# Function to filter based on year range (specific to Dataset 1)
def filter_by_year(df, filter_columns, start_year, end_year):
    year_columns = [(col) for col in df_full.columns if str(col).isdigit()]
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

import streamlit as st

# Inject custom CSS to apply a background color with opacity to the margin area
st.markdown("""
    <style>
    /* Apply grey background with opacity to the margin area (outer portion) */
    .reportview-container {
        background-color: rgba(77, 73, 73, 0.1);  /* Grey with 50% opacity */
        padding: 30px;  /* Add padding around the content */
    }

    /* Keep content area white with no opacity */
    .main {
        background-color: rgba(11, 11, 11, 0.1);  /* Keep content area white */
        margin: 50px;  /* No padding inside the content area */
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state for active page
if "page" not in st.session_state:
    st.session_state["page"] = "Home"  # Default active page

# Function to update session state and rerun
def set_page(page_name):
    st.session_state["page"] = page_name
    st.rerun()  # Forces UI to update immediately

# Create column layout
col1, col2, col3, col4 = st.columns([7, 1, 1, 1])

# Render buttons with conditional highlighting
with col2:
    if st.button("Home", use_container_width=True, 
                 type="primary" if st.session_state["page"] == "Home" else "secondary"):
        set_page("Home")

with col3:
    if st.button("Reference", use_container_width=True, 
                 type="primary" if st.session_state["page"] == "Reference" else "secondary"):
        set_page("Reference")

with col4:
    if st.button("The Science", use_container_width=True, 
                 type="primary" if st.session_state["page"] == "Document" else "secondary"):
        set_page("Document")




image_path = "background.jpg"  # Specify the image path
with open(image_path, "rb") as image_file:
    image_base64 = base64.b64encode(image_file.read()).decode()

# Custom CSS to set the background image with size and opacity for just the background
st.markdown(
    f"""
    <style>
    .stApp {{
        position: absolute;
        width: 100%;
        height: 100vh;  /* Ensure it takes full viewport height */
    }}

    .stApp::before {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: url("data:image/jpeg;base64,{image_base64}");
        background-size: cover;  /* Change to cover for better scaling */
        background-position: center center;
        background-repeat: no-repeat;
        z-index: -1; /* Make sure content is above the background */
        opacity: 0.9; /* Set opacity for the background image */
    }}
    </style>
    """,
    unsafe_allow_html=True
)


# Display the content based on the selected page
if st.session_state["page"] == "Home":

    #"
    # Streamlit UI
    # Display logo and title
    col1, col2 = st.columns([1, 5])
    with col1:

        st.image("SBT_Logo.png", width=300)  # Set both width and height

    with col2:
        # Add custom styles for tooltips
        st.markdown(
            """
            <style>
            /* Tooltip styling for title */
            .title-tooltip {
                position: relative;
                display: inline-block;
                cursor: pointer;
            }

            /* Tooltip text */
            .title-tooltip:hover::after {
                content: attr(data-tooltip);
                position: absolute;
                bottom: 100%;
                left: 50%;
                transform: translateX(-50%);
                background-color: rgba(0, 0, 0, 0.7); /* Dark background for the tooltip */
                color: white;
                padding: 5px;
                border-radius: 5px;
                font-size: 12px;
                white-space: nowrap;
                z-index: 1;  /* Ensure tooltip is above */
                opacity: 1;
                transition: opacity 0.3s;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        # Add the title with a tooltip
        st.markdown(
            """
            <style>
            .title-tooltip {
                position: relative;
                top: 50px;   /* Moves the text down */
                left: 100px; /* Moves the text to the right */
                text-align: right;  /* Aligns the text to the right */
            }
            </style>
            <div class="title-tooltip" data-tooltip="Explore various pathways for climate action">
                <span style="font-size: 48px; font-weight: bold;">Pathway Explorer</span>
            </div>
            """,
            unsafe_allow_html=True
        )
            

    st.write("Here you can find all the raw data, eligible scenarios and pathways that informs the cross sector and sector-specific standards in the SBTi")
    # Add custom CSS to style the tabs with the same background color
    st.markdown(
        """
        <style>
        /* Style for the tab container to ensure even distribution */
        .stTabs [data-baseweb="tablist"] {
            display: flex;
            justify-content: flex-start;  /* Align tabs to the left without extra space */
            gap: 5px;  /* Reduced space between tabs */
        }

        /* Style for each individual tab */
        .stTabs [data-baseweb="tab"] {
            background-color:rgb(42,52,68);  /* Green background for all tabs */
            color: white;
            padding: 10px;
            text-align: center;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
            flex-grow: 0;  /* Ensure tabs are not stretched */
        }

        /* Style for tab when hovered */
        .stTabs [data-baseweb="tab"]:hover {
            background-color:rgb(211, 151, 133);  /* Darker green when hovered */
            cursor: pointer;  /* Change cursor to pointer when hovered */
        }

        /* Style for active tab (clicked tab) */
        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background-color:rgb(234,137,71);  /* Dark green when tab is selected */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Define tabs for multiple data sources
    tabs = st.tabs(["IPCC", "Cross-Sector Pathways", "Power", "Chemical", "Building", "Oil & Gas","FINZ","FLAG","Aluminium","Cement","Pulp & Paper","Steel", "Other Industries","Others"])


    # File paths and filter columns for different datasets
    datasets_info = {
        "IPCC": {
            "file_path": "C1-3_summary_2050_variable.csv",
            "filter_columns": ["Category", "Model", "Scenario", "Region", "Variable",'Unit'],
            "remove_columns": [],
            "apply_year_filter": True
        },
        "Cross-Sector Pathways": {
            "file_path": "Alldata.xlsx",
            "filter_columns": ["Model", "Scenario", "Region", "Variable", "Unit"],
            "remove_columns": [],
            "apply_year_filter": True
        },
        "Power": {
            "file_path": "Pathway Database - Updated 2024-205.xlsx",
            "filter_columns": ["Metric","Model", "Scenario", "Unit"],
            "remove_columns": [],
            "apply_year_filter": False
        },
        "Chemical": {
            "file_path": "N2Oandchemical.xlsx",
            "filter_columns": ["Category", "Parameter", "Unit"],
            "remove_columns": [],
            "apply_year_filter": False
        },
        "Building": {
            "file_path": "buildings.xlsx",
            "filter_columns": ["Target type", "Scope / Emissions boundary",	"Unit", "Geography","Country", "Building type"],
            "remove_columns": [],
            "apply_year_filter": False
        },
        "Oil & Gas": {
            "file_path": "Oil & Gas.xlsx",
            "filter_columns": ["Model", "Scenario", "Variable", "Unit"],
            "remove_columns": [],
            "apply_year_filter": False},
        
        "FINZ": {
            "file_path": "FINZ.xlsx",
            "filter_columns": ["Model", "Scenario"],
            "remove_columns": [],
            "apply_year_filter": False
            },
        "FLAG": {
            "file_path": "Flag.xlsx",
            "filter_columns": ["Activity", "Region", "Commodity", "Unit"],
            "remove_columns": [],
            "apply_year_filter": False
        },
        "Aluminium": {
            "file_path": "Aluminium.xlsx",
            "filter_columns": ["Scenario", "Region", "Variable", "Unit"],
            "remove_columns": [],
            "apply_year_filter": False
        },
        "Cement": {
            "file_path": "Cement.xlsx",
            "filter_columns": ["Scenario", "Region", "Variable", "Unit"],
            "remove_columns": [],
            "apply_year_filter": False
        },
        "Pulp & Paper": {
            "file_path": "Pulp & Paper.xlsx",
            "filter_columns": ["Scenario", "Region", "Variable", "Unit"],
            "remove_columns": [],
            "apply_year_filter": False
        },
        "Steel": {
            "file_path": "Steel.xlsx",
            "filter_columns": ["Scenario", "Region", "Variable", "Unit"],
            "remove_columns": [],
            "apply_year_filter": False
        },
        "Other Industries": {
            "file_path": "Other Industries.xlsx",
            "filter_columns": ["Scenario", "Region", "Variable", "Unit"],
            "remove_columns": [],
            "apply_year_filter": False
        },
        "Others": {
            "file_path": "Phase-Out.xlsx",
            "filter_columns": ["Model", "Scenario"],
            "remove_columns": [],
            "apply_year_filter": False}

    }

    # Iterate over each tab and display corresponding data
    for idx, tab in enumerate(tabs):
        dataset_name = list(datasets_info.keys())[idx]
        dataset_info = datasets_info[dataset_name]
        #st.write(tab)
        # Document Tab

        with tab:
            if dataset_name not in ["Others","FINZ"]:
                st.subheader(f"View and Filter {dataset_name}")
                
                # Load data preview (first 1000 rows only)
                file_path = dataset_info["file_path"]
                remove_cols = dataset_info['remove_columns']
                #st.write(remove_cols)
                df_preview = load_data_preview(file_path)
                df_preview.drop(columns=remove_cols,inplace=True)
                if df_preview is not None:
                    st.write("### Data Preview")
                    st.dataframe(df_preview.head(), hide_index=True)

                    # Load full data for filtering purposes (without limiting to preview rows)
                    df_full = load_full_data(file_path,None,None)
                    df_full.drop(columns=remove_cols,inplace=True)
                

                    # Filtering UI based on the full data columns (not preview)
                    st.write("### Filter Data")
                    filters = {}
                    
                    filter_columns = dataset_info["filter_columns"]
                    cols = st.columns(len(filter_columns))

                    selected_values = {}  # For storing selected filter values
                    
                    # Update filter options dynamically based on previous selections
                    # Update filter options dynamically based on previous selections
                    
                    for i, col in enumerate(filter_columns):
                        if col in df_full.columns:
                            options = df_full[col].astype(str).unique().tolist()
                            selected_values[col] = cols[i].multiselect(f"{col}", options, key=f"{col}_{idx}")

                    # Apply the filter to the dataset
                    for col, values in selected_values.items():
                        if values:  # Ensure selections are made
                            df_full = df_full[df_full[col].astype(str).str.lower().isin([v.lower() for v in values])]

                    
                    # Add year range filters for 'AllData' dataset or any dataset requiring year filtering
                    if dataset_info["apply_year_filter"]:
                        # Get list of years from the dataset
                        year_columns = [str(col) for col in df_full.columns if str(col).isdigit()]
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
                        st.write(f"### Filtered Data {dataset_name}")
                        st.dataframe(df_full.head(100), hide_index=True)

                        # Button to download filtered data
                        excel_data = to_excel(df_full)
                        st.download_button(
                            label="Download Excel",
                            data=excel_data,
                            file_name=f"{dataset_name}_filtered_data.xlsx",
                            mime="application/vnd.ms-excel",
                            key=f"download_button_{dataset_name}_{idx}"  # Ensure unique key for download button
                        )

                        # Identify year columns (assuming they are numeric)
                        year_columns = [(col) for col in df_full.columns if str(col).isdigit()]
                        year_columns = sorted(year_columns, key=int)

                        if dataset_name in ("IPCC", "Cross-Sector Pathways", "Oil & Gas", "Aluminium", "Cement","Steel","Pulp & Paper", "Other Industries"):

                            #st.write("### Visualizing Data")
                            
                            df_model = df_full.copy()
                            df_model.fillna(0, inplace=True)

                            # Ensure year columns are numeric
                            df_model[year_columns] = df_model[year_columns].apply(pd.to_numeric, errors='coerce')

                            # Reshape data from wide to long format
                            df_melted = df_model.melt(id_vars=filter_columns,
                                                    value_vars=year_columns, 
                                                    var_name="Year", value_name="Value")
                            
                            #df_melted = df_melted.groupby(['Variable','Year'])['Value'].median().reset_index()
                            # Convert Year column to integer
                            df_melted["Year"] = pd.to_numeric(df_melted["Year"], errors='coerce')
                            df_melted["Value"] = pd.to_numeric(df_melted["Value"], errors='coerce')

                            median_values = df_melted.groupby('Year')['Value'].median().reset_index()
                            median_values['Scenario'] = 'Median'

                            # Combine the original data with the median data
                            if dataset_name not in ('Oil & Gas', "Aluminium", "Cement","Steel","Pulp & Paper", "Other Industries"):
                                df_combined = pd.concat([df_melted, median_values])
                            else:
                                df_combined = pd.concat([df_melted])

                            df_combined.dropna(subset=["Value"], inplace=True)
                            df_combined = df_combined[df_combined['Value']!=0]

                            if df_combined["Unit"].nunique()==1:
                                unit = df_combined["Unit"].unique()[0]
                            else: unit='Unit (Mixed)'

                            if df_combined["Variable"].nunique()==1:
                                title_val = df_combined["Variable"].unique()[0]
                            else: title_val='Multiple Variables'
                            
                            
                            # Plotly line chart with multiple lines for different models
                            fig = px.line(df_combined, x="Year", y="Value", color="Scenario",
                                        title=f'"{title_val}" - Trend Comparison',
                                        labels={"Value": unit, "Year": "Year", "Scenario": "Scenario"},
                                        markers=True)  # Add markers to check if points are plotted
                            
                            fig.update_xaxes(type="linear",)
                            # Set chart height
                            fig.update_layout(height=600, width=1200)  # Adjust the height as needed (default is ~450)
                            if dataset_name!='Oil & Gas':
                                fig.update_traces(line=dict(color="black", width=4), selector=dict(name="Median"),)

                            st.plotly_chart(fig)      

                        if dataset_name=="Power-Sector":
                            #st.write("### Visualizing Data")
                            # Calculate the median line across all years
                            #print(df_full.columns)
                            df_full = df_full[~df_full.apply(lambda row: row.astype(str).str.contains('Median').any(), axis=1)]

                            df_melted = df_full.melt(id_vars=["Metric", "Model", "Scenario", "Unit", "scen_id"], 
                                                value_vars=[(year) for year in range(2020, 2051, 5)], 
                                                var_name="Year", value_name="Value")

                            # Calculate the median across all models for each year
                            median_values = df_melted.groupby('Year')['Value'].median().reset_index()
                            median_values['Model'] = 'Median - ALL'
                            median_values['Scenario'] = 'Median - ALL'
                            median_values['scen_id'] = 'Median - ALL'

                            # Combine the original data with the median data
                            df_combined = pd.concat([df_melted, median_values])
                            
                            if df_combined["Unit"].nunique()==1:
                                unit = df_combined["Unit"].unique()[0]
                                metric_name = df_combined["Metric"].unique()[0]
                            else: 
                                unit='Unit (Mixed)'
                                metric_name = "Multiple Metric"

                            # Plot the line chart
                            fig = px.line(df_combined, x="Year", y="Value", color="Scenario", 
                                        title= metric_name, 
                                        labels={"Value": unit, "Year": "Year", "Scenario": "Scenario"},
                                        markers=True)

                            # Set the line styles for median and other models
                            fig.update_traces(line=dict(color="grey"), selector=dict(name="scen_id"))
                            fig.update_traces(line=dict(color="black", width=4), selector=dict(name="Median - ALL"),)

                            # Set chart height
                            fig.update_layout(height=600, width=1200)  # Adjust the height as needed (default is ~450)
                            # Display the plot in Streamlit
                            st.plotly_chart(fig)
                        
                        if dataset_name=="Building":
                            #st.write("### Visualizing Data")
                            # Calculate the median line across all years
                            #print(df_full.columns)
                            df_full = df_full[~df_full.apply(lambda row: row.astype(str).str.contains('Median').any(), axis=1)]

                            df_melted = df_full.melt(id_vars=filter_columns, 
                                                value_vars=[(year) for year in range(2030, 2055, 5)], 
                                                var_name="Year", value_name="Value")

                            # Calculate the median across all models for each year
                            median_values = df_melted.groupby('Year')['Value'].median().reset_index()
                            median_values['Model'] = 'Median - ALL'
                            median_values['Scenario'] = 'Median - ALL'
                            median_values['scen_id'] = 'Median - ALL'
                            
                            
                            if df_melted["Building type"].nunique()==1:

                                if df_melted["Unit"].nunique()==1:
                                    unit = df_melted["Unit"].unique()[0]
                                    metric_name = df_melted["Building type"].unique()[0]
                                else: 
                                    unit='Unit (Mixed)'
                                    metric_name = "Multiple Building type"
                                # Plot the line chart
                                fig = px.line(df_melted, x="Year", y="Value", color="Country", 
                                            title= metric_name, 
                                            labels={"Value": unit, "Year": "Year", "Country": "Country"},
                                            markers=True)

                                # Set the line styles for median and other models
                                fig.update_traces(line=dict(color="grey"), selector=dict(name="Country"))
                                fig.update_traces(line=dict(color="black", width=4), selector=dict(name="Median - ALL"),)

                                # Set chart height
                                fig.update_layout(height=600, width=1200)  # Adjust the height as needed (default is ~450)
                                # Display the plot in Streamlit
                                st.plotly_chart(fig)

                            elif df_melted["Country"].nunique()==1:
                                if df_melted["Unit"].nunique()==1:
                                    unit = df_melted["Unit"].unique()[0]
                                    metric_name = df_melted["Country"].unique()[0]
                                else: 
                                    unit='Unit (Mixed)'
                                    metric_name = "Multiple Country"
                                # Plot the line chart
                                fig = px.line(df_melted, x="Year", y="Value", color="Building type", 
                                            title= metric_name, 
                                            labels={"Value": unit, "Year": "Year", "Building type": "Building type"},
                                            markers=True)

                                # Set the line styles for median and other models
                                fig.update_traces(line=dict(color="grey"), selector=dict(name="Building type"))
                                fig.update_traces(line=dict(color="black", width=4), selector=dict(name="Median - ALL"),)

                                # Set chart height
                                fig.update_layout(height=600, width=1200)  # Adjust the height as needed (default is ~450)
                                # Display the plot in Streamlit
                                st.plotly_chart(fig)

                            else:
                                st.write('Either choose 1 County or 1 Building type')

                        if dataset_name=="FLAG":
                            #st.write("### Visualizing Data")
                            # Calculate the median line across all years
                            #print(df_full.columns)
                            df_full = df_full[~df_full.apply(lambda row: row.astype(str).str.contains('Median').any(), axis=1)]

                            df_melted = df_full.melt(id_vars=filter_columns, 
                                                value_vars=[(year) for year in range(2030, 2055, 5)], 
                                                var_name="Year", value_name="Value")
                            
                            
                            if df_melted["Commodity"].nunique()==1:

                                if df_melted["Unit"].nunique()==1:
                                    unit = df_melted["Unit"].unique()[0]
                                    metric_name = df_melted["Commodity"].unique()[0]
                                else: 
                                    unit='Unit (Mixed)'
                                    metric_name = "Multiple Region"
                                # Plot the line chart
                                fig = px.line(df_melted, x="Year", y="Value", color="Region", 
                                            title= metric_name, 
                                            labels={"Value": unit, "Year": "Year", "Region": "Region"},
                                            markers=True)

                                # Set the line styles for median and other models
                                fig.update_traces(line=dict(color="grey"), selector=dict(name="Region"))

                                # Set chart height
                                fig.update_layout(height=600, width=1200)  # Adjust the height as needed (default is ~450)
                                # Display the plot in Streamlit
                                st.plotly_chart(fig)

                            elif df_melted["Region"].nunique()==1:
                                if df_melted["Unit"].nunique()==1:
                                    unit = df_melted["Unit"].unique()[0]
                                    metric_name = df_melted["Region"].unique()[0]
                                else: 
                                    unit='Unit (Mixed)'
                                    metric_name = "Multiple Commodity"
                                # Plot the line chart
                                fig = px.line(df_melted, x="Year", y="Value", color="Commodity", 
                                            title= metric_name, 
                                            labels={"Value": unit, "Year": "Year", "Commodity": "Commodity"},
                                            markers=True)

                                # Set the line styles for median and other models
                                fig.update_traces(line=dict(color="grey"), selector=dict(name="Commodity"))

                                # Set chart height
                                fig.update_layout(height=600, width=1200)  # Adjust the height as needed (default is ~450)
                                # Display the plot in Streamlit
                                st.plotly_chart(fig)

                            else:
                                st.write('Either choose 1 Region or 1 Commodity')
                        
                        if dataset_name == "Chemical":
                            df_full.columns = df_full.columns.astype(str)

                            # Melt DataFrame for Plotly
                            df_melted = df_full.melt(id_vars=["Category", "Parameter", "Unit"], 
                                                    var_name="Year", 
                                                    value_name="Value")

                            # Streamlit App
                            st.title("Parameter Trends Over Time")

                            # Loop through each unique Parameter and plot separate charts
                            for i, param in enumerate(df_melted["Parameter"].unique()):
                                df_filtered = df_melted[df_melted["Parameter"] == param]
                                unit = df_melted["Unit"].unique()[0]

                                # Create line chart
                                fig = px.line(df_filtered, 
                                            x="Year", 
                                            y="Value", 
                                            color="Category",
                                            markers=True,  # Add markers to data points
                                            labels={"Value": unit},
                                            title=f"{param} - Line Chart by Category")
                                
                                # Ensure x-axis only shows the available years in data
                                fig.update_xaxes(type="linear")

                                # Display chart in Streamlit
                                st.plotly_chart(fig, use_container_width=True)
            elif dataset_name == "FINZ" :
                # File paths and filter columns for different datasets
                datasets_info2 = {
                    "FINZ-1": {
                        "file_path": "FINZ.xlsx",
                        "filter_columns": ["Variable", "scen_id"],
                        "remove_columns": [],
                        "apply_year_filter": False
                    },
                     "FINZ-2": {
                        "file_path": "FINZ.xlsx",
                        "filter_columns": ["Variable", "Region"],
                        "remove_columns": [],
                        "apply_year_filter": False
                    } }
                tab2 = st.tabs(["FINZ-1", "FINZ-2"])
                # Iterate over each tab and display corresponding data
                for idx, tab in enumerate(tab2):
                    dataset_name = list(datasets_info2.keys())[idx]
                    dataset_info2 = datasets_info2[dataset_name]
                    with tab:
                        if dataset_name=="FINZ-1":
                            file_path = dataset_info2["file_path"]
                            remove_cols = dataset_info2['remove_columns']
                            df = pd.read_excel(file_path,sheet_name='FINZ_NGFS')
                            st.write("### Data Preview")
                            st.dataframe(df.head(), hide_index=True)
                            col1, col2 = st.columns([1, 5])
                            categorical_columns = dataset_info2["filter_columns"]
                            # Identify year columns (assuming they are numeric)
                            year_columns = [(col) for col in df.columns if str(col).isdigit()]
                            year_columns = sorted(year_columns, key=int)

                            # Filtering UI based on the full data columns (not preview)
                            st.write("### Filter Data")
                            filters = {}
                            filter_columns = dataset_info2["filter_columns"]
                            cols = st.columns(len(filter_columns))

                            selected_values = {}  # For storing selected filter values
                            
                            # Update filter options dynamically based on previous selections
                            # Update filter options dynamically based on previous selections
                            for i, col in enumerate(filter_columns):
                                if col in df.columns:
                                    options = df[col].astype(str).unique().tolist()
                                    selected_values[col] = cols[i].multiselect(f"{col}", options, key=f"{col}")

                            # Apply the filter to the dataset
                            for col, values in selected_values.items():
                                if values:  # Ensure selections are made
                                    df = df[df[col].astype(str).str.lower().isin([v.lower() for v in values])]
                            
                            # Add year range filters for 'AllData' dataset or any dataset requiring year filtering
                            if dataset_info["apply_year_filter"]:
                                # Get list of years from the dataset
                                year_columns = [str(col) for col in df.columns if str(col).isdigit()]
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
                                df = filter_by_year(df, filter_columns, int(start_year), int(end_year))

                            # Button to load full data and apply filters
                            if st.button("Apply Filters", key=f"apply_filters_{dataset_name}_{idx}"):
                                # Show filtered data
                                st.write(f"### Filtered Data {dataset_name}")
                                st.dataframe(df.head(100), hide_index=True)

                                # Button to download filtered data
                                excel_data = to_excel(df_full)
                                st.download_button(
                                    label="Download Excel",
                                    data=excel_data,
                                    file_name=f"{dataset_name}_filtered_data.xlsx",
                                    mime="application/vnd.ms-excel",
                                    key=f"download_button_{dataset_name}_{idx}"  # Ensure unique key for download button
                                )

                                # Identify year columns (assuming they are numeric)
                                year_columns = [(col) for col in df.columns if str(col).isdigit()]
                                year_columns = sorted(year_columns, key=int)


                                df.fillna(0, inplace=True)

                                # Ensure year columns are numeric
                                df[year_columns] = df[year_columns].apply(pd.to_numeric, errors='coerce')

                                # Reshape data from wide to long format
                                df_melted = df.melt(id_vars=["scen_id", "Model" ,"Scenario", "Region", "Variable", "Unit"], 
                                                        value_vars=year_columns, 
                                                        var_name="Year", value_name="Value")
                                
                                #df_melted = df_melted.groupby(['Variable','Region','Year'])['Value'].median().reset_index()
                                # Convert Year column to integer
                                df_melted["Year"] = pd.to_numeric(df_melted["Year"], errors='coerce')
                                df_melted["Value"] = pd.to_numeric(df_melted["Value"], errors='coerce')

                                median_values = df_melted.groupby('Year')['Value'].median().reset_index()
                                median_values['scen_id'] = 'Median'

                                df_melted = pd.concat([df_melted,median_values])

                                if df_melted["Unit"].nunique()==1:
                                    unit = df_melted["Unit"].unique()[0]
                                else: unit='Unit (Mixed)'
                                if df_melted["Variable"].nunique()==1:
                                    title_val = df_melted["Variable"].unique()[0]
                                else: title_val='Multiple Variables'
                                
                                # Plotly line chart with multiple lines for different models
                                fig = px.line(df_melted, x="Year", y="Value", color='scen_id',
                                            title=f'"{title_val}" - Trend Comparison',
                                            labels={"Value": unit, "Year": "Year", "scen_id": "scen_id"},
                                            markers=True)  # Add markers to check if points are plotted
                                
                                fig.update_xaxes(type="linear",)
                                # Set chart height
                                fig.update_layout(height=600, width=1200)  # Adjust the height as needed (default is ~450)
                                fig.update_traces(line=dict(color="black", width=4), selector=dict(name="Median"),)
                                # Display chart in Streamlit
                                st.plotly_chart(fig, use_container_width=True)
                        
                        else:  #dataset_name=="FINZ-1":
                            
                            file_path = dataset_info2["file_path"]
                            remove_cols = dataset_info2['remove_columns']
                            df = pd.read_excel(file_path,sheet_name='FINZ_OECM')
                            st.write("### Data Preview")
                            st.dataframe(df.head(), hide_index=True)
                            col1, col2 = st.columns([1, 5])
                            categorical_columns = dataset_info2["filter_columns"]
                            # Identify year columns (assuming they are numeric)
                            year_columns = [(col) for col in df.columns if str(col).isdigit()]
                            year_columns = sorted(year_columns, key=int)

                            # Filtering UI based on the full data columns (not preview)
                            st.write("### Filter Data")
                            filters = {}
                            filter_columns = dataset_info2["filter_columns"]
                            cols = st.columns(len(filter_columns))

                            selected_values = {}  # For storing selected filter values
                            
                            # Update filter options dynamically based on previous selections
                            # Update filter options dynamically based on previous selections
                            for i, col in enumerate(filter_columns):
                                if col in df.columns:
                                    options = df[col].astype(str).unique().tolist()
                                    selected_values[col] = cols[i].multiselect(f"{col}", options,)

                            # Apply the filter to the dataset
                            for col, values in selected_values.items():
                                if values:  # Ensure selections are made
                                    df = df[df[col].astype(str).str.lower().isin([v.lower() for v in values])]

                            # Add year range filters for 'AllData' dataset or any dataset requiring year filtering
                            if dataset_info["apply_year_filter"]:
                                # Get list of years from the dataset
                                year_columns = [str(col) for col in df.columns if str(col).isdigit()]
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
                                df = filter_by_year(df, filter_columns, int(start_year), int(end_year))

                            # Button to load full data and apply filters
                            if st.button("Apply Filters", key=f"apply_filters_{dataset_name}_{idx}"):
                                # Show filtered data
                                st.write(f"### Filtered Data {dataset_name}")
                                st.dataframe(df.head(100), hide_index=True)

                                # Button to download filtered data
                                excel_data = to_excel(df_full)
                                st.download_button(
                                    label="Download Excel",
                                    data=excel_data,
                                    file_name=f"{dataset_name}_filtered_data.xlsx",
                                    mime="application/vnd.ms-excel",
                                    key=f"download_button_{dataset_name}_{idx}"  # Ensure unique key for download button
                                )

                                # Identify year columns (assuming they are numeric)
                                year_columns = [(col) for col in df.columns if str(col).isdigit()]
                                year_columns = sorted(year_columns, key=int)
 
                                df.fillna(0, inplace=True)

                                # Ensure year columns are numeric
                                df[year_columns] = df[year_columns].apply(pd.to_numeric, errors='coerce')

                                # Reshape data from wide to long format
                                df_melted = df.melt(id_vars=["Model", "Scenario", "Region", "Variable", "Unit"], 
                                                        value_vars=year_columns, 
                                                        var_name="Year", value_name="Value")
                                    
                                #df_melted = df_melted.groupby(['Variable','Region','Year'])['Value'].median().reset_index()
                                # Convert Year column to integer
                                df_melted["Year"] = pd.to_numeric(df_melted["Year"], errors='coerce')
                                df_melted["Value"] = pd.to_numeric(df_melted["Value"], errors='coerce')
                                if df_melted["Unit"].nunique()==1:
                                    unit = df_melted["Unit"].unique()[0]
                                else: unit='Unit (Mixed)'
                                if df_melted["Variable"].nunique()==1:
                                    title_val = df_melted["Variable"].unique()[0]
                                else: title_val='Multiple Variables'
                                
                                
                                # Plotly line chart with multiple lines for different models
                                fig = px.line(df_melted, x="Year", y="Value", color='Region',
                                            title=f'"{title_val}" - Trend Comparison',
                                            labels={"Value": unit, "Year": "Year", "Region": "Region"},
                                            markers=True)  # Add markers to check if points are plotted
                                
                                fig.update_xaxes(type="linear",)
                                # Set chart height
                                fig.update_layout(height=600, width=1200)  # Adjust the height as needed (default is ~450)
                                # Display chart in Streamlit
                                st.plotly_chart(fig, use_container_width=True)
                                



            elif dataset_name == "Others" :
                # File paths and filter columns for different datasets
                datasets_info3 = {
                    "Phase-Out": {
                        "file_path": "Phase-Out.xlsx",
                        "filter_columns": ["Model", "Scenario"],
                        "remove_columns": [],
                        "apply_year_filter": False
                    },
                     "Residuals": {
                        "file_path": "Phase-Out.xlsx",
                        "filter_columns": ["Model", "Scenario"],
                        "remove_columns": [],
                        "apply_year_filter": False
                    } }
                tab3 = st.tabs(["Phase-Out", "Residuals"])
                # Iterate over each tab and display corresponding data
                for idx, tab in enumerate(tab3):
                    dataset_name = list(datasets_info3.keys())[idx]
                    dataset_info3 = datasets_info3[dataset_name]
                    with tab:
                        if dataset_name=="Phase-Out":
                            file_path = dataset_info3["file_path"]
                            remove_cols = dataset_info3['remove_columns']
                            df = pd.read_excel(file_path,sheet_name='Phase out dates',skiprows=3)
                            st.dataframe(df, hide_index=True)
                        
                        else:
                            file_path = dataset_info3["file_path"]
                            remove_cols = dataset_info3['remove_columns']
                            df = pd.read_excel(file_path,sheet_name='Residuals',skiprows=2)
                            st.dataframe(df, hide_index=True)
                            

            else:
                st.error("Error loading data preview.")


elif st.session_state["page"] == "Reference":
    # Streamlit UI
    # Display logo and title
    col1, col2 = st.columns([1, 5])
    with col1:
        # Define the path to your local background image
        background_image_path = r"C:\Users\puroh\Downloads\PIXNIO-350667-4130x2309 (2).jpg"

        # Add custom CSS to set the background image
        st.markdown(
            f"""
            <style>
            body {{
                background-image: url('file:///{background_image_path}');
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
        st.image("SBT_Logo.jpg", width=300)  # Set both width and height

    with col2:
        # Add custom styles for tooltips
        st.markdown(
            """
            <style>
            /* Tooltip styling for title */
            .title-tooltip {
                position: relative;
                display: inline-block;
                cursor: pointer;
            }

            /* Tooltip text */
            .title-tooltip:hover::after {
                content: attr(data-tooltip);
                position: absolute;
                bottom: 100%;
                left: 50%;
                transform: translateX(-50%);
                background-color: rgba(0, 0, 0, 0.7); /* Dark background for the tooltip */
                color: white;
                padding: 5px;
                border-radius: 5px;
                font-size: 12px;
                white-space: nowrap;
                z-index: 1;  /* Ensure tooltip is above */
                opacity: 1;
                transition: opacity 0.3s;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        # Add the title with a tooltip
        st.markdown(
            """
            <style>
            .title-tooltip {
                position: relative;
                top: 50px;   /* Moves the text down */
                left: 100px; /* Moves the text to the right */
                text-align: right;  /* Aligns the text to the right */
            }
            </style>
            <div class="title-tooltip" data-tooltip="Explore various pathways for climate action">
                <span style="font-size: 48px; font-weight: bold;">Pathway Explorer</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("Here you can find all the raw data, eligible scenarios and pathways that informs the cross sector and sector-specific standards in the SBTi")

    st.markdown(
        """
        <style>
        /* Style for the tab container to ensure even distribution */
        .stTabs [data-baseweb="tablist"] {
            display: flex;
            justify-content: flex-start;  /* Align tabs to the left without extra space */
            gap: 5px;  /* Reduced space between tabs */
        }

        /* Style for each individual tab */
        .stTabs [data-baseweb="tab"] {
            background-color:rgb(42,52,68);  /* Green background for all tabs */
            color: white;
            padding: 10px;
            text-align: center;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
            flex-grow: 0;  /* Ensure tabs are not stretched */
        }

        /* Style for tab when hovered */
        .stTabs [data-baseweb="tab"]:hover {
            background-color:rgb(211, 151, 133);  /* Darker green when hovered */
            cursor: pointer;  /* Change cursor to pointer when hovered */
        }

        /* Style for active tab (clicked tab) */
        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background-color:rgb(234,137,71);  /* Dark green when tab is selected */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    # Define tabs for multiple data sources
    tabs = st.tabs(["Document", "Criteria"])

    # File paths and filter columns for different datasets
    datasets_info = {
        "Document": {
            "file_path": "Alldata.xlsx",
            "filter_columns": ["Model", "Scenario", "Region", "Variable"],
            "remove_columns": [],
            "apply_year_filter": False
        },
        "Criteria": {
            "file_path": "Phase-Out.xlsx",
            "filter_columns": ["Model", "Scenario", "Region", "Variable"],
            "remove_columns": [],
            "apply_year_filter": False
        }
    }

    # Iterate over each tab and display corresponding data
    for idx, tab in enumerate(tabs):
        dataset_name = list(datasets_info.keys())[idx]
        dataset_info = datasets_info[dataset_name]
        #st.write(tab)
        # Document Tab

        with tab:
            if dataset_name=='Document':
                
                file_path = dataset_info["file_path"]

                df = load_full_data(file_path,None,None)

                # Drop integer and float columns, keeping only categorical columns
                #categorical_columns = df.select_dtypes(exclude=['int64', 'float64']).columns

                # Remove unwated columns
                categorical_columns = dataset_info['filter_columns']

                # Initialize session state for selection persistence
                if "selected_var" not in st.session_state:
                    st.session_state["selected_var"] = categorical_columns[0]

                st.title("Eligible SBTi Scenarios")
                st.write("These are the eligible Scenarios that pass the principled-driven criteria used in cross-sector pathway")
                # Layout: Left (buttons) | Right (data)
                col1, col2 = st.columns([1, 5])

                with col1:
                        
                    for col in categorical_columns:
                        if st.button(str(df[col].nunique())+" "+col):
                            st.session_state["selected_var"] = col  # Store selection persistently

                # Right Column: Display unique values
                with col2:
                    if st.session_state["selected_var"]:
                        selected_var = st.session_state["selected_var"]
                        #st.subheader(f"Unique Values for: {selected_var}")

                        # Search box for filtering unique values
                        search_query = st.text_input("Search:", "")

                        # Get unique values and filter based on search query
                        unique_values = df[selected_var].dropna().unique()
                        filtered_values = [val for val in unique_values if search_query.lower() in str(val).lower()]
                            
                        # Convert to DataFrame and display
                        unique_df = pd.DataFrame(filtered_values, columns=[selected_var]).reset_index()
                        #st.write(f'{unique_df[selected_var].nunique()}, unique {selected_var}')
                        st.dataframe(unique_df[selected_var].values, use_container_width=True, height=600)  # Full-width display


            elif dataset_name == 'Criteria':

                file_path = dataset_info["file_path"]
                remove_cols = dataset_info['remove_columns']
                df = load_full_data(file_path,None, None)
                st.write('')
                st.write('The SBTi applies these filters to align scenario selection with its key principles—ambition, responsibility, scientific rigor, actionability, robustness, and transparency. By applying these quantitative criteria, SBTi prioritizes scientifically robust and equitable pathways. This approach maintains credibility, ensuring pathways meet high scientific and ethical standards.')
                st.dataframe(df, hide_index=True)
            else:
                st.error("Error loading data preview.")
elif st.session_state["page"] == "Document":
 # Redirect to document page
        st.title("Under construction")

        # Local file path (Replace this with your actual path)
        pdf_path = "documents/sample.pdf"


        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                ss.pdf_ref = f.read()  # Store binary content
        else:
            st.error("File not found. Please check the path.")
            ss.pdf_ref = None

        # Display PDF using `streamlit_pdf_viewer`
        if st.session_state.pdf_ref:
            pdf_viewer(input=st.session_state.pdf_ref, width="100%")
            # Download Button
            st.download_button(label="📥 Download PDF", 
                            data=ss.pdf_ref, 
                            file_name="sample.pdf", 
                            mime="application/pdf")