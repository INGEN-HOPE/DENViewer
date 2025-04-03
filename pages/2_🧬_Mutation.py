import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
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



# Load the data
df = pd.read_csv('pages/files/all_Mutations.csv')

# Add small jitter to the position
df['Position Jittered'] = df['Position'] + np.random.uniform(-0.5, 0.5, size=len(df))

# Define mutation types and colors
mutation_types = df['Mutation Type'].unique()
colors = px.colors.qualitative.Set1[:len(mutation_types)]

# Create individual DataFrames for each mutation type
filtered_dataframes = {mt: df[df['Mutation Type'] == mt] for mt in mutation_types}

# Base figure creation function for lollipop plot without connecting lines
def create_figure(data, color):
    return [
        # Add sticks (vertical lines) for lollipop
        go.Scatter(
            x=data['Position Jittered'],
            y=data['Frequency'],
            mode='lines',
            line=dict(color='SlateGrey', width=0.25),
            hoverinfo='skip',
            showlegend=False
        ),
        # Add markers at the top of the sticks
        go.Scatter(
            x=data['Position Jittered'],
            y=data['Frequency'],
            mode='markers',
            marker=dict(
                size= data['Frequency'] * 35,  # Scale size for visibility
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
            name=data['Mutation Type'].iloc[0]  # Use Mutation Type for legend
        )
    ]

# Initialize figure with all data
fig = go.Figure()

# Add lollipop traces for all mutation types
for mt, color in zip(mutation_types, colors):
    traces = create_figure(filtered_dataframes[mt], color)
    for trace in traces:
        fig.add_trace(trace)

# Add shaded regions and gene labels
gene_ranges = [
    {'start': 1, 'end': 99, 'gene': '5 UTR'},
    {'start': 100, 'end': 441, 'gene': 'C'},
    {'start': 442, 'end': 939, 'gene': 'M'},
    {'start': 940, 'end': 2424, 'gene': 'E'},
    {'start': 2425, 'end': 3480, 'gene': 'NS1'},
    {'start': 3481, 'end': 4134, 'gene': 'NS2A'},
    {'start': 4135, 'end': 4524, 'gene': 'NS2B'},
    {'start': 4525, 'end': 6378, 'gene': 'NS3'},
    {'start': 6379, 'end': 6828, 'gene': 'NS4A'},
    {'start': 6829, 'end': 7572, 'gene': 'NS4B'},
    {'start': 7573, 'end': 10275, 'gene': 'NS5'},
    {'start': 10276, 'end': 11000, 'gene': '3 UTR'}
]

for gene in gene_ranges:
    fig.add_shape(
        type='rect',
        x0=gene['start'], x1=gene['end'],
        y0=-0.02 * max(df['Frequency']), y1=0,
        fillcolor='grey', opacity=0.2,
        layer='below', line_width=0
    )
    fig.add_annotation(
        x=(gene['start'] + gene['end']) / 2,
        y=-0.1 * max(df['Frequency']),
        text=gene['gene'],
        showarrow=False,
        font=dict(size=12, color='black'),
        textangle=45,
        align='center'
    )

# Define dropdown buttons
dropdown_buttons = [
    {'label': 'All Mutation Types', 'method': 'update',
     'args': [{'visible': [True] * (2 * len(mutation_types))},
              {'title': 'All Mutation Types'}]},
]

# Add dropdown options for each mutation type
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

# Add reset button
dropdown_buttons.append({
    'label': 'Reset Filter',
    'method': 'update',
    'args': [{'visible': [True] * (2 * len(mutation_types))},
             {'title': 'Reset Filter'}]
})

# Update layout with dropdown menus and legend
fig.update_layout(
    updatemenus=[{
        'buttons': dropdown_buttons,
        'direction': 'up',
        'showactive': True,
        'x': 0.9,
        'xanchor': 'right',
        'y': -0.2,
        'yanchor': 'bottom',
        'pad': {'r': 10, 't': 10}
    }],
    legend={
        'orientation': "h",
        'x': 0, 'y': -0.3,
        'title': "Mutation Type",
        'traceorder': "normal",
        'itemsizing': "constant",
        'font': {'size': 14},
},
    margin=dict(l=40, r=40, t=40, b=150),
    height=600,
    plot_bgcolor='white',
    xaxis=dict(title='Position', showgrid=False),
    yaxis=dict(title='Mutation Frequency',showgrid=False),
    title='Dengue Virus Mutation Frequency'
)

# Display the plot
fig.show()




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
