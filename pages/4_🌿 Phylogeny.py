import streamlit as st
import pandas as pd
from ete3 import Tree
import plotly.graph_objects as go
from plotly.graph_objects import Scattergl

# Cache data loading and processing
@st.cache_data
def load_metadata():
    df = pd.read_csv("pages/files/all_clade.csv")
    df.columns = df.columns.str.strip()
    return df

@st.cache_resource
def load_tree():
    return Tree("pages/files/tree.nwk", format=1)

# Streamlit page setup
st.set_page_config(
    page_title="DENViewer",
    page_icon="🦧",
    layout="wide"
)

# Sidebar configuration
st.sidebar.image("pages/images/lab_logo.png", use_container_width=True)
st.sidebar.markdown('<p class="sidebar-title">DENViewer</p>', unsafe_allow_html=True)
st.sidebar.markdown("""
<style>
.sidebar-title {
    font-size: 24px;
    font-weight: bold;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)
st.sidebar.markdown("---")

# Load data
metadata = load_metadata()
tree = load_tree()

# User input for metadata coloring
selected_column = st.selectbox("Select metadata column for coloring:", metadata.columns, index=2)
unique_values = metadata[selected_column].dropna().unique()
selected_values = st.multiselect("Filter by category:", sorted(unique_values), default=sorted(unique_values)[:5])
filtered_metadata = metadata[metadata[selected_column].isin(selected_values)]

# Assign tree positions
y_positions, x_positions, y_offset = {}, {}, 0

def assign_positions(node, depth=0):
    global y_offset
    if node.is_leaf():
        y_positions[node] = y_offset
        x_positions[node] = depth
        y_offset += 1
    else:
        child_y = []
        for child in node.children:
            assign_positions(child, depth + 1)
            child_y.append(y_positions[child])
        y_positions[node] = sum(child_y) / len(child_y)
        x_positions[node] = depth

assign_positions(tree)

# Create color palette
color_palette = ["blue", "green", "red", "orange", "purple", "magenta", "cyan", "olive", "brown", "teal"]
category_colors = {val: color_palette[i % len(color_palette)] for i, val in enumerate(unique_values)}

# Start Plotly figure
fig = go.Figure()

# Draw branches
for node in tree.traverse():
    if not node.is_root():
        parent = node.up
        if parent in x_positions and node in x_positions:
            fig.add_trace(Scattergl(
                x=[x_positions[parent], x_positions[parent]],
                y=[y_positions[parent], y_positions[node]],
                mode="lines",
                line=dict(color="black", width=1),
                showlegend=False
            ))
            fig.add_trace(Scattergl(
                x=[x_positions[parent], x_positions[node]],
                y=[y_positions[node], y_positions[node]],
                mode="lines",
                line=dict(color="black", width=1),
                showlegend=False
            ))

# Plot leaf nodes
legend_seen = set()
for leaf in tree.iter_leaves():
    row = filtered_metadata.loc[filtered_metadata["IGIB_id"] == leaf.name]
    if not row.empty:
        category = row[selected_column].values[0]
        color = category_colors.get(category, "grey")
        tooltip = f"{leaf.name}<br>{selected_column}: {category}"

        fig.add_trace(Scattergl(
            x=[x_positions[leaf]],
            y=[y_positions[leaf]],
            mode="markers",
            marker=dict(color=color, size=6),
            text=tooltip,
            hoverinfo="text",
            name=category if category not in legend_seen else None,
            showlegend=category not in legend_seen
        ))
        legend_seen.add(category)

# Layout config
fig.update_layout(
    showlegend=True,
    legend_title=selected_column,
    xaxis=dict(title="Tree Depth (Evolutionary Distance)", zeroline=False),
    yaxis=dict(title="Leaf Nodes", showticklabels=False, zeroline=False),
    width=1500,
    height=900,
    margin=dict(l=20, r=20, t=60, b=20)
)

# Display
st.title("Phylogenetic Tree")
st.markdown("Disclaimer: Some visualizations may take time to load due to the complexity of the data.")
st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("""
<hr>
<p style='text-align: center;'>
© 2024 Rajesh Pandey | Ingen-hope Lab
</p>
""", unsafe_allow_html=True)
