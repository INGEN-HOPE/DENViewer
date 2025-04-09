import streamlit as st
import altair as alt
import pandas as pd
import plotly.express as px
import streamlit_shadcn_ui as ui



# Set Streamlit page config
st.set_page_config(
    page_title="DENViewer ", #Decoding 
    page_icon="🧫",
    layout="wide",
    initial_sidebar_state="auto",
)

# App content
st.markdown("<h1 style='text-align: center;'>Welcome to DENViewer</h1>", unsafe_allow_html=True)
# Add logo (replace with your image path)


st.sidebar.image("pages/images/lab_logo.png", use_container_width=True)
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
#st.image("pages/images/background.webp", caption="created using DALL.E")

#Description
st.markdown(
        """
        <p class='sub-header' style='text-align: justify;'><
        
        font size=1
        Genomic surveillance plays a critical role in understanding and controlling dengue virus outbreaks. Explore the Dengue Genomic Surveillance Dashboard to dive into real-time sequencing data and trends! 🚀

        an interactive platform showcasing genomic insights from over 4,000 dengue virus genomes sequenced using NGS platforms for 2022-2023 at [INGEN-HOPE Lab](https://ingen-hope.github.io/). This active surveillance effort focuses on hospital-admitted patients in the Delhi NCR region, providing a real-time view of dengue virus evolution, serotype distribution, and emerging genomic patterns.

        This dashboard serves for the exploration of researchers, clinicians, and public health officials to explore serotype prevalence, lineage dynamics, and geographical trends, aiding in a deeper understanding of the ongoing dengue epidemic. Stay informed with data-driven insights to support surveillance, outbreak preparedness, and public health interventions.
        </p>
        """,
        unsafe_allow_html=True
    )


#Load GISAID data
df = pd.read_csv('pages/files/gisaid_arbo_2025_03_31_07.csv')
df2 = pd.read_csv('pages/files/all_demographics.csv')
df3 = pd.read_csv('pages/files/Cases prevalent in India over time.csv')

#piechart count
total_samples = len(df2)  




df_count = df.groupby(["Serotype", "Date"]).size().reset_index(name="Count")

# Create bar chart
fig2= px.area(
    df_count,
    x="Date",
    y="Count",
    color="Serotype",
    title="Prevalence of Serotypes Over Time",
    labels={"Count": "Number of Sequences", "Date": "Date"},
    height=500,
    line_group="Serotype"
)

# Update layout for stacked area
fig2.update_layout(
    xaxis=dict(title="Date", tickvals=df["Date"].unique(),),
    yaxis=dict(title="Number of Sequences"),
    legend_title="Serotype",
)

col1, col2 = st.columns((1.5,5), gap='medium')

with col1:
    st.markdown('#### In-House Dengue Genome Surveillance Stats')
    
    ui.metric_card(title="Total Genomes Sequenced", content=f"{total_samples}", description="2022-2023")
    
    df_gen = df2.dropna(subset=["Gender", "Severity"])  

    gender_order = ["Male", "Female", "Child"]
    df2["Gender"] = pd.Categorical(df2["Gender"], categories=gender_order, ordered=True)
    
    if "Gender" in df2.columns:
        gender_counts = df2["Gender"].value_counts().reset_index()
        gender_counts.columns = ["Gender", "Count"]
        
        fig_gender = px.pie(
            gender_counts, 
            names="Gender", 
            values="Count", 
            title="Gender Distribution",
            hole=0.4,
            category_orders={"Gender": gender_order}
        ).update_layout(width=500, height=500)

    severity_order = ["Mild", "Moderate", "Severe"]
    df2["Severity"] = pd.Categorical(df2["Severity"], categories=severity_order, ordered=True)

    fig_gvs = px.sunburst(df_gen, 
        path=["Gender", "Severity"], 
        title="Severity Distribution by Gender"
    ).update_layout(width=500, height=500)
    
    st.plotly_chart(fig_gvs, use_container_width=True)

    fig_gva = px.box(df_gen, x="Gender", y="Age", color="Severity",
    category_orders={"Severity": severity_order, "Gender": gender_order}, title="Age Distribution across Severity"
    ).update_layout(width=500, height=500)
    st.plotly_chart(fig_gva, use_container_width=True)

with col2:
    st.markdown("<h1 style='text-align: center;'>Dengue Surveillance in Asia Over Time</h1>",unsafe_allow_html=True)
    
    sub_col1, sub_col2 = st.columns([2.5,1.5])
    
    with sub_col1:
# Group by Date, Location, and Serotype to get the count
        df_scatter = df.groupby(["Date", "Location", "Serotype"]).size().reset_index(name="Count")

# Dropdown to select serotype
        serotype_options = ["All"] + sorted(df_scatter["Serotype"].unique().tolist())
        selected_serotype = st.selectbox("Select Serotype:", serotype_options)

# Filter data based on selection
        if selected_serotype == "All":
            df_filtered = df_scatter.groupby(["Date", "Location"], as_index=False)["Count"].sum()
        else:
            df_filtered = df_scatter[df_scatter["Serotype"] == selected_serotype]

# Plotly Scatter Plot
        fig1 = px.scatter(
        df_filtered,
        x="Date",
        y="Location",
        size="Count",
        color="Location",
        title="Country-wise Dengue Genome Surveillance",
        height=800, width= 800,
        opacity =1,
        )


# Force all y-axis values to display
        fig1.update_layout(
        xaxis=dict(
        type="-",  # Ensures proper numerical representation
        tickmode="array",
        tickvals=df["Date"].unique(),  # Show all unique x-values
        ),  
      yaxis=dict(
        categoryorder="total ascending",
        tickmode="array",
        tickvals=df["Location"].unique(),
        ),
    )

        fig1.update_traces(textposition="middle right")

   # Display in Streamlit
        st.plotly_chart(fig1)
# Display second plot
        st.plotly_chart(fig2, use_container_width=True)

    with sub_col2:
        st.markdown('#### Case and Death Reports in Indian States')

        year_list = list(df3.Year.unique())[::-1]
        selected_year = st.selectbox('Select a year', year_list, index=0)

        df_selected_year = df3[df3.Year == selected_year].sort_values(by="Cases", ascending=False)
        st.dataframe(
            df_selected_year[["State", "Cases"]],
                hide_index=True,
                column_config={
                "State": st.column_config.TextColumn("State"),
                "Cases": st.column_config.ProgressColumn(
                    "Cases",
                        format="%d",
                        min_value=0,
                        max_value=df_selected_year["Cases"].max(),
                    ),
                },
                width=None,
            )
    
        df_selected_year = df3[df3.Year == selected_year].sort_values(by="Cases", ascending=False)
        st.dataframe(
            df_selected_year[["State", "Deaths"]],
                hide_index=True,
                column_config={
                "State": st.column_config.TextColumn("State"),
                "Deaths": st.column_config.ProgressColumn(
                    "Deaths",
                        format="%d",
                        min_value=0,
                        max_value=df_selected_year["Deaths"].max(),
                    ),
                },
                width=None,
            )    

        st.write('''
        Plot Data Source: [NCVBDC](<https://ncvbdc.mohfw.gov.in/index4.php?lang=1&level=0&linkid=431&lid=3715>).
        ''')

        with st.expander('Other Dengue Resources', expanded=True):
            st.write('''
            - :orange[**NCVBDC**]: Dengue Situtation in India. [Click here](<https://ncvbdc.mohfw.gov.in/index.php>)
            - :orange[**Nextclade**]: Clade assignment, mutation calling, and sequence quality checks [Click here](<https://clades.nextstrain.org/>).
            - :orange[**GISAID-Dengue**]: Global Initiative for sharing Surveillance Data [Click here](<https://gisaid.org/phylogeny-dengue/>).
            ''')

# Footer
st.markdown(
    """
    <hr>
    <p style='text-align: center;'>
    © 2024 Rajesh Pandey | INGEN-HOPE Lab
    </p>
    """,
    unsafe_allow_html=True
)
