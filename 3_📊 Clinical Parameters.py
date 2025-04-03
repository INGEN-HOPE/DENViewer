import streamlit as st
import pandas as pd
import plotly.express as px


# Set Streamlit page config
st.set_page_config(
    page_title="DENViewer ", #Decoding 
    page_icon="🧫",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": None,
    }    
)

# Add logo (replace with your image path)
st.sidebar.image("pages/images/lab_logo.png", use_container_width=True)
# Add Dashboard Name
st.sidebar.markdown('<p class="sidebar-title">DENViewer</p>', unsafe_allow_html=True)


# Sidebar customization
st.sidebar.markdown(
    """
    <style>
        .sidebar-title {
            font-size: 24px;
            font-weight: bold;
            text-align: center;
            color: "white";
            margin-bottom: 10px;
        }
        .sidebar-logo {
            display: block;
            margin: 0 auto;
            width: 150px;  /* Adjust size as needed */
            border-radius: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)
# Optional: Add a separator for aesthetics
st.sidebar.markdown("---")

# Load Data
data_file = "pages/files/all_demographics.csv"  # Update the path if needed
df = pd.read_csv(data_file)

# Ensure column names are stripped of any extra spaces
df.columns = df.columns.str.strip()

# Convert categorical columns to strings
categorical_cols = ["Gender", "Severity", "Age","Collection_date"]  # Adjust if needed
df[categorical_cols] = df[categorical_cols].astype(str)

# Streamlit App Layout
st.title("Interactive Data Visualization")

# Dropdown to Select Plot Type
plot_type = st.selectbox(
    "Select Plot Type", 
    ["Bar Plot", "Boxplot", "Histogram", "Pie Chart", "Sunburst Chart"]
)

# Dropdown to Select X-axis (only for relevant plots)
if plot_type not in ["Pie Chart", "Sunburst Chart"]:
    x_axis = st.selectbox("Select X-axis", df.columns)
else:
    x_axis = None  # No need for X-axis in Pie/Sunburst

# Dropdown to Select Coloring (Optional)
color_option = st.selectbox(
    "Select Column for Coloring (Optional)", 
    ["None"] + categorical_cols
)
color_column = None if color_option == "None" else color_option

# Create Plots Based on Selection
fig = None  # Initialize empty figure

if plot_type == "Bar Plot":
    df_grouped = df.groupby([x_axis, color_column]).size().reset_index(name="Count")
    fig = px.bar(df_grouped, x=x_axis, y="Count", color=color_column)
    fig.update_layout(yaxis_title="Count")  # Proper y-axis labeling
    fig.update_traces(hovertemplate="%{x}: %{y}")

elif plot_type == "Boxplot":
    fig = px.box(df, x=x_axis, y="Age", color=color_column)
    fig.update_traces(hovertemplate="%{x}: Median=%{y}")

elif plot_type == "Histogram":
    fig = px.histogram(df, x=x_axis, color=color_column, nbins=20, barmode="overlay")
    fig.update_traces(hovertemplate="%{x}: Count=%{y}")

elif plot_type == "Pie Chart":
    category_column = st.selectbox("Select Column for Pie Chart", categorical_cols)
    fig = px.pie(df, names=category_column, title=f"Distribution of {category_column}", color=category_column)
    fig.update_traces(hovertemplate="<b>%{label}</b>: %{percent:.1%}")

elif plot_type == "Sunburst Chart":
    path_columns = st.multiselect("Select Hierarchy for Sunburst", categorical_cols, default=["Severity", "Gender"])
    if len(path_columns) > 0:
        fig = px.sunburst(df, path=path_columns, title="Sunburst Chart of Selected Categories", color=path_columns[-1])
        fig.update_traces(hovertemplate="<b>%{label}</b>: %{percentRoot:.1%} of Total")

# Fix Y-axis for Age
if fig and x_axis == "Age":
    fig.update_layout(yaxis=dict(range=[0, 70]))

if fig:
    st.plotly_chart(fig, use_container_width=True)

with st.expander('About', expanded=True):
        st.write('''
            - :orange[**Severity Classification**]: 
                -Mild: (Dengue without warning signs): Patients with normal platelet and leukocyte counts (no thrombocytopenia or leukopenia).
                -Moderate (Dengue with warning signs): Patients with normal platelet counts but decreased leukocyte counts (leukopenia without thrombocytopenia). 
                -Severe: Patients with both low platelet counts (thrombocytopenia) and decreased leukocyte counts (leukopenia).
            - :orange[**Sequencing platform**]: Oxford Nanopore Technology
            ''')

# Footer
st.markdown(
    """
    <hr>
    <p style='text-align: center;'>
    © 2024 Rajesh Pandey | Ingen-hope Lab
    </p>
    """,
    unsafe_allow_html=True
)
