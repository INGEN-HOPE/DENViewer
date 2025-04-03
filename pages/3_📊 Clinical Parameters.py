import streamlit as st
import pandas as pd
import plotly.express as px

# Set Streamlit page config
st.set_page_config(
    page_title="DENViewer",
    page_icon="🧫",
    layout="wide",
    initial_sidebar_state="auto"
)

# Add Sidebar Content
st.sidebar.image("pages/images/lab_logo.png", use_container_width=True)
st.sidebar.markdown('<p class="sidebar-title">DENViewer</p>', unsafe_allow_html=True)
st.sidebar.markdown("---")


# Load Data
data_file = "pages/files/all_demographics.csv"  # Update the path if needed
df = pd.read_csv(data_file)

df = df.dropna(subset=["Severity", "Age"])

# Define severity order (Severe → Mild → Moderate)
severity_order = ["Severe", "Mild", "Moderate"]
df["Severity"] = pd.Categorical(df["Severity"], categories=severity_order, ordered=True)

# Convert categorical columns to strings
categorical_cols = ["Age","Gender", "Severity","Collection_date"]  # Adjust if needed
df[categorical_cols] = df[categorical_cols].astype(str)

# Streamlit App Layout
st.title("Clinical Parameters")

st.markdown(
        """
        <p class='sub-header' style='text-align: justify;'>
        This page provides an interactive platform to explore key clinical parameters related to dengue surveillance. By analyzing patient demographics, disease severity, and other clinical indicators, users can gain a deeper understanding of the impact of dengue infections.

         #### **Key Features:** 
        - **Severity Distribution:** Visualize how disease severity varies across different patient groups.
        - **Age and Gender Trends:** Examine how age and gender influence clinical outcomes.
        - **Clinical Insights:** Analyze key clinical parameters to identify patterns and associations.</p>
        """,
        unsafe_allow_html=True
    )
# Dropdown to Select Plot Type
plot_type = st.selectbox(
    "Select Plot Type", 
    ["Sunburst Chart","Bar Plot","Boxplot", "Histogram", "Pie Chart" ]
)

# Dropdown to Select X-axis (only for relevant plots)
if plot_type not in ["Pie Chart", "Sunburst Chart"]:
    x_axis = st.selectbox("Select X-axis", df.columns)
else:
    x_axis = None  # No need for X-axis in Pie/Sunburst

# Dropdown to Select Coloring (Optional)
color_option = st.selectbox(
    "Select Column for Coloring (Optional)", 
    ["Gender"] + categorical_cols
)
color_column = None if color_option == "None" else color_option

# Create Plots Based on Selection
fig = None  # Initialize empty figure

if plot_type == "Bar Plot":
    df_grouped = df.groupby([x_axis, color_column]).size().reset_index(name="Count")
    fig = px.bar(df_grouped, x=x_axis, y="Count", color=color_column, category_orders={"Severity": severity_order})
    fig.update_layout(yaxis_title="Count")
    fig.update_traces(hovertemplate="%{x}: %{y}")

elif plot_type == "Boxplot":
    fig = px.box(df, x=x_axis, y="Age", color=color_column, category_orders={"Severity": severity_order})
    fig.update_traces(hovertemplate="%{x}: Median=%{y}")

elif plot_type == "Histogram":
    fig = px.histogram(df, x=x_axis, color=color_column, nbins=20, barmode="overlay", category_orders={"Severity": severity_order})
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
            - **Mild**: Dengue without warning signs (normal platelet & leukocyte counts)
            - **Moderate**: Dengue with warning signs (normal platelet, decreased leukocytes)
            - **Severe**: Dengue with thrombocytopenia (low platelets & leukocytes)
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
