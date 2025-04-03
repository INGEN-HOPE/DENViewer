import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import plotly.express as px
import streamlit_shadcn_ui as ui

# Set Streamlit page config
st.set_page_config(
    page_title="DENViewer",
    page_icon="🧫",
    layout="wide",
    initial_sidebar_state="auto",
)

# Sidebar: Add logo and title
st.sidebar.image("pages/images/lab_logo.png", use_container_width=True)
st.sidebar.markdown('<p class="sidebar-title">DENViewer</p>', unsafe_allow_html=True)

# Sidebar styling
st.sidebar.markdown(
    """
    <style>
        .sidebar-title {
            font-size: 24px;
            font-weight: bold;
            text-align: center;
            color: white;
            margin-bottom: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("---")

# Load Data
try:
    df = pd.read_csv('pages/files/all_Mutations.csv')
except FileNotFoundError:
    st.error("File 'all_Mutations.csv' not found. Please check the file path.")
    st.stop()

# Add a sidebar option to select the year (assuming you have a 'Year' column)
selected_year = st.sidebar.selectbox("Select Year", df["Year"].unique())

# Filter data based on selected year
df_selected_year = df[df["Year"] == selected_year]

# Compute statistics
total_mutations = len(df_selected_year)
synonymous_mutations = len(df_selected_year[df_selected_year["Mutation Type"] == "Synonymous Variant"])
unique_positions = df_selected_year["Position"].nunique()

# Layout for metrics (4 cards in a row)
col1, col2, col3, col4 = st.columns(4)

with col1:
    ui.metric_card(title="Total Mutations", content=total_mutations, description="Count of all mutations")

with col2:
     ui.metric_card(title="Synonymous Mutations", content=synonymous_mutations, description="Mutations that do not change amino acid")

with col3:
     ui.metric_card(title="Unique Positions", content=unique_positions, description="Distinct mutation positions in the genome")

with col4:
     ui.metric_card(title="Selected Year", content=selected_year, description="Year selected for mutation statistics")

# Ensure numeric columns
df['Position'] = pd.to_numeric(df['Position'], errors='coerce')
df['Frequency'] = pd.to_numeric(df['Frequency'], errors='coerce')

# Drop rows with NaN values in essential columns
df.dropna(subset=['Position', 'Frequency'], inplace=True)

# Add small jitter to position
df['Position Jittered'] = df['Position'] + np.random.uniform(-0.5, 0.5, size=len(df))

# Define mutation types and colors
mutation_types = df['Mutation Type'].unique()
colors = px.colors.qualitative.Set1[:len(mutation_types)]

# Create a dictionary of DataFrames for each mutation type
filtered_dataframes = {mt: df[df['Mutation Type'] == mt] for mt in mutation_types}

# Function to create scatter plots (lollipop chart)
def create_figure(data, color):
    return [
        go.Scatter(
            x=data['Position Jittered'],
            y=data['Frequency'],
            mode='lines',
            line=dict(color='SlateGrey', width=0.25),
            hoverinfo='skip',
            showlegend=False
        ),
        go.Scatter(
            x=data['Position Jittered'],
            y=data['Frequency'],
            mode='markers',
            marker=dict(
                size=np.maximum(data['Frequency'] * 10, 5),   # Scale marker size
                color=color,
                opacity=0.6
            ),
            hoverinfo='text',
            text=[
                f"Position: {row['Position']}<br>"
                f"Mutation Type: {row['Mutation Type']}<br>"
                f"Frequency: {row['Frequency']}<br>"
                f"Mild Frequency: {row['Mild Frequency']}<br>"
                f"Moderate Frequency: {row['Moderate Frequency']}<br>"
                f"Severe Frequency: {row['Severe Frequency']}"
                for index, row in data.iterrows()
            ],
            name=data['Mutation Type'].iloc[0]  
        )
    ]

# Initialize figure
fig = go.Figure()

# Add traces for each mutation type
for mt, color in zip(mutation_types, colors):
    traces = create_figure(filtered_dataframes[mt], color)
    for trace in traces:
        fig.add_trace(trace)

# Define gene regions with distinct colors
gene_ranges = [
    {'start': 1, 'end': 99, 'gene': '5 UTR', 'color': '#FFA07A'},  # Light Salmon
    {'start': 100, 'end': 441, 'gene': 'C', 'color': '#20B2AA'},  # Light Sea Green
    {'start': 442, 'end': 939, 'gene': 'M', 'color': '#FF6347'},  # Tomato
    {'start': 940, 'end': 2424, 'gene': 'E', 'color': '#8A2BE2'},  # Blue Violet
    {'start': 2425, 'end': 3480, 'gene': 'NS1', 'color': '#4682B4'},  # Steel Blue
    {'start': 3481, 'end': 4134, 'gene': 'NS2A', 'color': '#32CD32'},  # Lime Green
    {'start': 4135, 'end': 4524, 'gene': 'NS2B', 'color': '#FFD700'},  # Gold
    {'start': 4525, 'end': 6378, 'gene': 'NS3', 'color': '#DC143C'},  # Crimson
    {'start': 6379, 'end': 6828, 'gene': 'NS4A', 'color': '#FF4500'},  # Orange Red
    {'start': 6829, 'end': 7572, 'gene': 'NS4B', 'color': '#1E90FF'},  # Dodger Blue
    {'start': 7573, 'end': 10275, 'gene': 'NS5', 'color': '#C71585'},  # Medium Violet Red
    {'start': 10276, 'end': 11000, 'gene': '3 UTR', 'color': '#2E8B57'}  # Sea Green
]

gene_bar_height = 0.08 * max(df['Frequency'])  # Adjust height relative to max Frequency

for gene in gene_ranges:
    fig.add_shape(
        type='rect',
        x0=gene['start'], x1=gene['end'],
        y0=-gene_bar_height, y1=0,  # Extend the height downwards
        fillcolor=gene['color'], opacity=0.5,  # Increase opacity for better visibility
        layer='below', line_width=0
    )
    fig.add_annotation(
        x=(gene['start'] + gene['end']) / 2,
        y=-1.5 * gene_bar_height,  # Move labels slightly lower
        text=gene['gene'],
        showarrow=False,
        font=dict(size=14, color='black', family="Arial Bold"),  # Larger & bolder text
        textangle=0,  # Keep horizontal for better readability
        align='center'
    )
    
# Create dropdown buttons
dropdown_buttons = [
    {'label': 'All Mutation Types', 'method': 'update',
     'args': [{'visible': [True] * (2 * len(mutation_types))},
              {'title': 'All Mutation Types'}]}
]

for i, mt in enumerate(mutation_types):
    visibility = [False] * (2 * len(mutation_types))
    visibility[2 * i] = True
    visibility[2 * i + 1] = True
    dropdown_buttons.append({
        'label': mt,
        'method': 'update',
        'args': [{'visible': visibility},
                 {'title': mt}]
    })

# Reset button
dropdown_buttons.append({
    'label': 'Reset Filter',
    'method': 'update',
    'args': [{'visible': [True] * (2 * len(mutation_types))},
             {'title': 'Reset Filter'}]
})

# Update figure layout
fig.update_layout(
    updatemenus=[{
        'buttons': dropdown_buttons,
        'direction': 'up',
        'showactive': True,
        'x': 0.9,
        'xanchor': 'right',
        'y': -0.2,
        'yanchor': 'bottom',
    }],
    legend=dict(
        orientation="h",
        x=0, y=-0.3,
        title="Mutation Type",
        traceorder="normal",
        itemsizing="constant",
        font=dict(size=14),
    ),
    margin=dict(l=40, r=40, t=40, b=150),
    height=600,
    plot_bgcolor='white',
    xaxis=dict(title='Position', showgrid=False),
    yaxis=dict(title='Mutation Frequency', showgrid=False),
    title='Dengue Virus Mutation Frequency'
)

# Display in Streamlit
st.plotly_chart(fig, use_container_width=True)

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
