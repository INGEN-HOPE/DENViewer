import streamlit as st
import pandas as pd
from ete3 import Tree
import plotly.graph_objects as go
from plotly.graph_objects import Scattergl

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


# Custom CSS to expand content area
st.markdown(
    """
    <style>
    .block-container {
        max-width: 95%;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Phylogenetic Tree")

st.markdown(""" Disclaimer: Some visualizations may take time to load due to the complexity of the data. Please be patient while the plots generate.""")
# Load the metadata
@st.cache_data
def load_metadata():
    metadata_file = "pages/files/all_clade.csv"
    metadata = pd.read_csv(metadata_file)
    metadata.columns = metadata.columns.str.strip()
    return metadata
# Let the user select the metadata column for coloring
selected_column = st.selectbox("Select metadata column for coloring:", metadata.columns, index=2)

# Generate unique colors for each category in the selected column
unique_values = metadata[selected_column].dropna().unique()
color_palette = [
    "blue", "green", "red", "orange", "skyblue", "magenta", "cyan", "violet", "purple", "brown"
]
category_colors = {value: color_palette[i % len(color_palette)] for i, value in enumerate(unique_values)}

# Load the Newick tree
tree_file = "pages/files/tree.nwk"
tree = Tree(tree_file, format=1)

# Assign positions for a rectangular layout
y_positions = {}
x_positions = {}
y_offset = 0


def assign_positions(node, depth=0):
    global y_offset
    if node.is_leaf():
        y_positions[node] = y_offset
        x_positions[node] = depth
        y_offset += 1
    else:
        child_positions = []
        for child in node.children:
            assign_positions(child, depth + 1)
            child_positions.append(y_positions[child])
        y_positions[node] = sum(child_positions) / len(child_positions)
        x_positions[node] = depth

assign_positions(tree)

# Create the figure
fig = go.Figure()

# Add tree branches
for node in tree.traverse():
    if not node.is_root():
        parent = node.up
        if parent in x_positions and node in x_positions:
            fig.add_trace(go.Scattergl(
                x=[x_positions[parent], x_positions[parent]],
                y=[y_positions[parent], y_positions[node]],
                mode="lines",
                line=dict(color="black", width=1),
                showlegend=False
            ))
            fig.add_trace(go.Scattergl(
                x=[x_positions[parent], x_positions[node]],
                y=[y_positions[node], y_positions[node]],
                mode="lines",
                line=dict(color="black", width=1),
                showlegend=False
            ))

# Add tree leaves with dynamic colors
legend_traces = {}
for leaf in tree.iter_leaves():
    matched_rows = metadata.loc[metadata["IGIB_id"] == leaf.name, selected_column]
    if not matched_rows.empty:
        category = matched_rows.values[0]
        color = category_colors.get(category, "black")
        tooltip_text = f"{leaf.name}<br>{selected_column}: {category}"
    else:
        continue

    trace = go.Scattergl(
    x=[x_positions[leaf]],
    y=[y_positions[leaf]],
    mode="markers",
    marker=dict(color=color, size=10),
    text=tooltip_text,
    hoverinfo="text",
    name=str(category) if category not in legend_traces else None,  # Convert to string
    showlegend=category not in legend_traces
)

    fig.add_trace(trace)
    legend_traces[category] = trace

# Update layout with larger size
fig.update_layout(
    showlegend=True,
    legend_title=selected_column,
    xaxis=dict(title="Tree Depth (Evolutionary Distance)", zeroline=False),
    yaxis=dict(title="Leaf Nodes", showticklabels=False, zeroline=False),
    width=1500,
    height=900,
    margin=dict(l=20, r=20, t=60, b=20)
)

# Display the tree

with st.container():
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
