import streamlit as st
import pandas as pd
import plotly.express as px
from ete3 import Tree
import plotly.graph_objects as go

# Set Streamlit page config
st.set_page_config(
    page_title="DENViewer ",
    page_icon="🧫",
    layout="wide",
    initial_sidebar_state="auto",
)

# Sidebar (Logo + Title)
st.sidebar.image("pages/images/lab_logo.png", use_container_width=True)
st.sidebar.markdown('<p class="sidebar-title">DENViewer</p>', unsafe_allow_html=True)
st.sidebar.markdown("---")

# Custom CSS
st.markdown(
    """
    <style>
    .block-container { max-width: 95%; padding-left: 2rem; padding-right: 2rem; }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Phylogenetic Tree with Boxplot Analysis")

# Cache data loading
@st.cache_data
def load_metadata():
    df = pd.read_csv("pages/files/all_clade.csv")
    df.columns = df.columns.str.strip()
    return df.dropna()  # Filter out NA values

metadata = load_metadata()

# Cache tree loading
@st.cache_resource
def load_tree():
    return Tree("pages/files/tree.nwk", format=1)

tree = load_tree()

# Boxplot: Age vs Severity
if "Age" in metadata.columns and "Severity" in metadata.columns:
    st.subheader("Age Distribution by Severity")
    fig_box = px.box(metadata, x="Severity", y="Age", color="Severity", title="Boxplot of Age by Severity")
    st.plotly_chart(fig_box, use_container_width=True)

# Select metadata column for coloring
selected_column = st.selectbox("Select metadata column for coloring:", metadata.columns, index=2)

# Generate unique colors
unique_values = metadata[selected_column].dropna().unique()
color_palette = ["blue", "green", "red", "orange", "skyblue", "magenta", "cyan", "violet", "purple", "brown"]
category_colors = {value: color_palette[i % len(color_palette)] for i, value in enumerate(unique_values)}

# Assign positions
y_positions, x_positions = {}, {}
y_offset = 0

def assign_positions(node, depth=0):
    global y_offset
    if node.is_leaf():
        y_positions[node], x_positions[node] = y_offset, depth
        y_offset += 1
    else:
        child_positions = [assign_positions(child, depth + 1) or y_positions[child] for child in node.children]
        y_positions[node] = sum(child_positions) / len(child_positions)
        x_positions[node] = depth

assign_positions(tree)

# Create Phylogenetic Tree Figure
fig = go.Figure()

# Add tree branches
for node in tree.traverse():
    if not node.is_root():
        parent = node.up
        if parent in x_positions and node in x_positions:
            fig.add_trace(go.Scatter(x=[x_positions[parent], x_positions[parent]], y=[y_positions[parent], y_positions[node]], mode="lines", line=dict(color="black", width=1), showlegend=False))
            fig.add_trace(go.Scatter(x=[x_positions[parent], x_positions[node]], y=[y_positions[node], y_positions[node]], mode="lines", line=dict(color="black", width=1), showlegend=False))

# Add tree leaves with colors
legend_traces = {}
for leaf in tree.iter_leaves():
    matched_rows = metadata.loc[metadata["IGIB_id"] == leaf.name, selected_column]
    if not matched_rows.empty:
        category = matched_rows.values[0]
        color = category_colors.get(category, "black")
        tooltip_text = f"{leaf.name}<br>{selected_column}: {category}"
    else:
        continue

    trace = go.Scatter(
        x=[x_positions[leaf]],
        y=[y_positions[leaf]],
        mode="markers",
        marker=dict(color=color, size=10),
        text=tooltip_text,
        hoverinfo="text",
        name=str(category) if category not in legend_traces else None, 
        showlegend=category not in legend_traces
    )

    fig.add_trace(trace)
    legend_traces[category] = trace

# Update layout
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
st.subheader("Phylogenetic Tree")
st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("<hr><p style='text-align: center;'>© 2024 Rajesh Pandey | Ingen-hope Lab</p>", unsafe_allow_html=True)
