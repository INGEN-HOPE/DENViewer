import streamlit as st


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
