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

st.title("Welcome to DENViewer")
#st.image("pages/images/background.webp", caption="created using DALL.E")

#Description
st.markdown(
        """
        <p class='sub-header' style='text-align: justify;'>
        Genomic surveillance plays a critical role in understanding and controlling dengue virus outbreaks. 

        This interactive platform showcases genomic insights from 4,000+ dengue virus genomes sequenced using Oxford Nanopore Technology for 2022-2023 at CSIR-IGIB, [INGEN-HOPE Lab](https://ingen-hope.github.io/). This active surveillance effort focuses on hospital-admitted patients in the Delhi NCR region, providing a real-time view of dengue virus evolution, serotype distribution, and emerging genomic patterns.

        Designed as an open-access resource for researchers, clinicians, and public health officials to explore serotype prevalence, lineage dynamics, and geographical trends, aiding in a deeper understanding of the ongoing dengue epidemic. Stay informed with data-driven insights to support surveillance, outbreak preparedness, and public health interventions.
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

# Count occurrences for size
df["Count"] = df.groupby(["Date", "Location"])["Location"].transform("count")

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
    st.markdown('#### In-House Dengue Surveillance Stats')
    
    ui.metric_card(title="Total Genomes Sequences", content=f"{total_samples}", description="2022-2023")
    
    # Remove NA
    df_gen = df2.dropna(subset=["Gender","Severity"])  

    # Define Gender order
    gender_order = ["Male", "Female", "Child"]
    df2["Gender"] = pd.Categorical(df2["Gender"], categories=gender_order, ordered=True)
    
    
        # Check if 'Gender' column exists in df2
    if "Gender" in df2.columns:
        # Count occurrences of each gender
        gender_counts = df2["Gender"].value_counts().reset_index()
        gender_counts.columns = ["Gender", "Count"]
        

        # Create a pie chart
        fig = px.pie(
            gender_counts, 
            names="Gender", 
            values="Count", 
            title="Gender Distribution",
            hole=0.4,  # Donut-style chart
            color_discrete_sequence=px.colors.qualitative.Set1,
            category_orders={"Gender":gender_order}
        ).update_layout(uniformtext=dict(minsize=16, mode='hide'),width=500, height=500)

        # Display in Streamlit
        #st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Gender column not found in the dataset.")
    

    # Define severity order
    severity_order = ["Mild", "Moderate", "Severe"]
    df2["Severity"] = pd.Categorical(df2["Severity"], categories=severity_order, ordered=True)

    #Plot
    fig_gvs = px.sunburst(df_gen, 
    path=["Gender", "Severity"], 
    title="Severity Distribution by Gender", 
    color_discrete_sequence=px.colors.qualitative.Set1,
    ).update_layout(uniformtext=dict(minsize=16, mode='hide'),width=500, height=500)
    st.plotly_chart(fig_gvs, use_container_width=True)

    fig_gva = px.box(df_gen, x="Gender", y="Age", color="Severity",
    category_orders={"Severity": severity_order,"Gender":gender_order}, title="Age Distribution across Severity",color_discrete_sequence=px.colors.qualitative.Set1).update_layout(width=500, height=500)
    st.plotly_chart(fig_gva, use_container_width=True)   


with col2:
    st.markdown("<h1 style='text-align: center;'>Dengue Surveillance in Asia Over Time</h1>",unsafe_allow_html=True)
    
    sub_col1, sub_col2 = st.columns([3.5,1.5])
    
    with sub_col1:

    # Streamlit Selectbox for filtering Serotype
        serotype_options = ["All"] + sorted(df["Serotype"].unique().tolist())
        selected_serotype = st.selectbox("Select Serotype:", serotype_options)

    # Filter data based on Serotype selection
        if selected_serotype != "All":
            df = df[df["Serotype"] == selected_serotype]

            # Plotly Scatter Plot
        fig1 = px.scatter(
            df,
            x="Date",
            y="Location",
            size="Count",
            text="Count",
            color="Location",
            title="Country-wise Dengue Surveillance",
            height=800, width= 600,
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

        # Streamlit Display
        st.plotly_chart(fig2, use_container_width=True)
    
        st.write('''
        Plot Data Source: [GISAID-Dengue](<https://gisaid.org/phylogeny-dengue/>).
        ''')

        
    with sub_col2:
        st.markdown('#### Top Indian States')

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
            - :orange[**GISAID-Dengue**]: Global Initiative for sharing Surveillance Data [Click here] (<https://gisaid.org/phylogeny-dengue/>).
            - :orange[**WHO**]:Dengue and Severe Dengue [Click here](https://www.who.int/news-room/fact-sheets/detail/dengue-and-severe-dengue)
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

