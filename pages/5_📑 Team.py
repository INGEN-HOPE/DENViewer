import streamlit as st
from st_social_media_links import SocialMediaIcons

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

# Title for the page
st.title("About Us")

# Brief introduction text
st.markdown("### Learning Genomics to Learn Genomes")
st.markdown("""Our team is dedicated to the development of an interactive Infectious Diseases Dashboard, integrating genomic and clinical data for better information dissemination. 
By leveraging data visualization, algorithm development, and real-time updates, we aim to create a dynamic platform that strengthens the public health paradigm.
""")

# Create a container for each creator with their name, LinkedIn link, and photo
# You can adjust the number of creators and their details as needed.

# Team Lead
team_lead = {
    "name": "Dr Rajesh Pandey",
    "title": "mentor",
    "photo": "pages/images/rajesh.jpg",
    "linkedin": "https://linkedin.com/in/rajesh-pandey-01238656",
    "twitter": "https://x.com/RajeshPandeyLab",
    "github": "https://github.com/INGEN-HOPE",
}

# Team Members
team_members = [
    {"name": "Priyanka Mehta", "photo": "pages/images/priyanka.jpg", "linkedin": "https://www.linkedin.com/in/priyanka-mehta-92339a355", "twitter": "https://x.com/priyankammehta", "github": "https://github.com/priyankamehta1811"},
    {"name": "Varsha Ravi", "photo": "pages/images/varsha.jpeg", "linkedin": "https://www.linkedin.com/in/varsha-ravi-818526107", "twitter": "https://x.com/varsha_ravi_", "github": "#"},
    {"name": "M D Imran", "photo": "pages/images/imran.jpg", "linkedin": "#", "twitter": "#", "github": "#"},
    {"name": "Ramakant Mohite", "photo": "pages/images/rama.jpg", "linkedin": "https://www.linkedin.com/in/ramakant-mohite-42875a212", "twitter": "https://x.com/mohite_ramakant", "github": "#"},
    {"name": "Jyoti Soni", "photo": "pages/images/jyoti.jpg", "linkedin": "#", "twitter": "https://x.com/Sonijyoti63", "github": "#"},
    {"name": "Balendu Upmanyu", "photo": "pages/images/Balendu.jpg", "linkedin": "https://www.linkedin.com/in/balendu-upmanyu-64b684217", "twitter": "#", "github": "#"},
    {"name": "Keerti Aswin", "photo": "pages/images/Aswin.jpg", "linkedin": "#", "twitter": "https://x.com/keerthic_aswin", "github": "#"},
 #   {"name": "Raj Rajeshwar Choudhury", "photo": "pages/images/", "linkedin": "#", "twitter": "#", "github": "#"},
 #   {"name": "Talibhu", "photo": "pages/images/", "linkedin": "#", "twitter": "#", "github": "#"},
 #   {"name": "Ayesha", "photo": "pages/images/", "linkedin": "#", "twitter": "#", "github": "#"},
]

# Custom CSS for Proper Vertical Alignment
st.markdown(
    """
    <style>
        .team-container { display: flex; flex-direction: column; align-items: center; text-align: center; margin-bottom: 20px; }
        .team-name { font-size: 16px; font-weight: bold; margin-top: 8px; }
        .team-lead-title { font-size: 18px; font-weight: bold; color: #0073e6; margin-top: 5px; }
        .social-icons { display: flex; justify-content: left; gap: 1px; margin-top: 8px; }
        .profile-pic { width: 300px; height: 300px; border-radius: 50%; object-fit: cover; }
    .team-lead-social-icons { 
                display: flex; 
                justify-content: flex-start; 
                gap: 10px; 
                margin-top: 8px; 
            }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Meet the Team")
st.markdown("#### Mentor", unsafe_allow_html=True)

cols_lead1 = st.columns(1)
for i in range(1):
    with cols_lead1[0]: 

        # Display Team Lead Separately
            st.markdown('<div class="team-container">', unsafe_allow_html=True)
            # Create a custom HTML to center the image
            st.image(team_lead["photo"], width=300, output_format="PNG")
            st.markdown("""<div style="display: flex; justify-content: center;">
            </div>""", unsafe_allow_html=True)
            # Optionally, display the name below the image
            st.markdown(f"### {team_lead['name']}")

            # Team Lead Social Media Links
            lead_links = [link for link in [team_lead["linkedin"], team_lead["twitter"], team_lead["github"]] if link and link != "#"]
            if lead_links:
                    social_media_icons = SocialMediaIcons(lead_links)
                    social_media_icons.render()

            st.markdown('</div>', unsafe_allow_html=True)

# Horizontal Divider
st.markdown("---")

# Display Other Team Members in Rows of 3
for i in range(0, len(team_members), 3):
    cols = st.columns(3)
    
    for j in range(3):
        if i + j < len(team_members):
            member = team_members[i + j]
            with cols[j]:
                st.markdown('<div class="team-container">', unsafe_allow_html=True)
                
                # Image (Centered)
                st.image(member["photo"], width=300, output_format="PNG")

                # Name (Centered)
                st.markdown(f'<p class="team-name">{member["name"]}</p>', unsafe_allow_html=True)

                # Social Media Links (Centered)
                social_links = [link for link in [member["linkedin"], member["twitter"], member["github"]] if link and link != "#"]
                if social_links:
                    social_media_icons = SocialMediaIcons(social_links)
                    social_media_icons.render()

                st.markdown('</div>', unsafe_allow_html=True)


# Additional information or contact can go here
st.markdown("""
    Feel free to reach out to us for any inquiries or collaborations. We appreciate your interest in our work!
""")



st.header(":mailbox: Get In Touch With US!")
st.markdown(" ### To contribute to the dashboard:")


#Contact form
contact_form = """
    <form class="contact-form" action="https://formsubmit.co/priyanka.m@igib.in" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="name" placeholder="Your name" required><br><br>
        <input type="email" name="email" placeholder="Your email" required><br><br>
        <input type="Institute" name="Institute" placeholder="Institute" required><br><br>
        <input type="Lab Name" name="Lab Name" placeholder="Lab Name" required><br><br>
        <input type="Lab Website" name="Lab Website" placeholder="Lab Website" ><br><br>
        <textarea name="message" placeholder="Your message here"></textarea><br><br>
        <button type="submit">Send</button>
    </form>
"""

# Render the contact form in the Contact section
st.markdown(contact_form, unsafe_allow_html=True)
# Additional contact details
st.write("""

         """)



# Footer
st.markdown(
    """
    <hr>
    <p style='text-align: center;'>
    © 2024 Rajesh Pandey| Ingen-hope Lab
    </p>
    """,
    unsafe_allow_html=True
)
