import base64
import textwrap as tw
from io import BytesIO

import streamlit as st

# from care_note_enhancement import note_enhancer
# from care_plan_generator import generate_plan
from gemini_initializer import GeminiInitializer

# from graph_initializer import GraphInitializer
# from knowledge_graph import add_patient, get_next_patient_id
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from streamlit_option_menu import option_menu


def get_image_as_base64(url):
    with open(url, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    
def create_pdf(content):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    Story = []

    styles = getSampleStyleSheet()

    sections = content.split("**")

    for index, section in enumerate(sections):
        if section.strip():
            if index == 0: 
                ptext = '<font size=20 color="red"><b>%s</b></font>' % section.strip()
                ptext = ptext.replace("#","")
                Story.append(Paragraph(ptext, styles["Heading1"]))
            elif section[-1] == ":":
                ptext = '<font size=14 color="blue"><b>%s</b></font>' % section.strip()
                Story.append(Paragraph(ptext, styles["Heading2"]))
            else:
                ptext = '<font size=12>%s</font>' % section.strip()
                Story.append(Paragraph(ptext, styles["BodyText"]))
                Story.append(Spacer(1, 0.2 * inch))

    doc.build(Story)
    buffer.seek(0)
    return buffer


st.set_page_config(
    page_title="Elders home Monitoring App",
    page_icon="👨‍⚕️",
    layout="centered",
    initial_sidebar_state="auto"
)

# Initilizing the gemini and graph
if "model_init" not in st.session_state:
    st.session_state.my_gemini = GeminiInitializer()
    # st.session_state.my_graph = GraphInitializer()   
    st.session_state.model_init = True

if "button_clicked" not in st.session_state:
    st.session_state.button_clicked = False

selected =option_menu(
    menu_title= None,
    options=["Home","Diet-Planning"],
    icons=["house","clipboard-heart-fill"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

if "active_tab" not in st.session_state:
    st.session_state.active_tab = selected

if selected != st.session_state.active_tab:
    if "text_copy" in st.session_state:
        del st.session_state.text_copy
    st.session_state.active_tab = selected

# Home tab
if selected == "Home":
    image_path = "E:\\SenzMate\\Diet-Plan\\Code\\backround.jpg" 
    base64_image = get_image_as_base64(image_path)
    background_image_css = f"background-image: url('data:image/png;base64,{base64_image}');"

    description = f"""
    <div style="
        position: relative;
        text-align: justify;
        color: black;
        {background_image_css}
        background-size: cover;
        border-radius: 10px;
        padding: 50px;
        ">
        <div style="
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 80%;  # Adjust the width as needed
            ">
            <h1 style='text-align: center; color: black'>Diet Plan Recommendation System</h1>
            <p style="background-color: rgba(128, 128, 128, 0.6); padding: 20px; border-radius: 10px;">Welcome to our state-of-the-art Personalized Diet Recommendation System, where precision meets personalization to enhance your journey towards optimal health. Our innovative platform is designed to analyze a comprehensive range of user data, including weight, height, age, gender and midical report. By leveraging this vital information, our system meticulously categorizes patients based on their unique needs and health goals, offering tailored diet plans that promote wellness and vitality.</p>
        </div>
    </div>
    """
    st.markdown(description, unsafe_allow_html=True)
    

elif selected == "Diet-Planning":
    st.title("Diet-Planning")

    general_detail_container = st.container(border=True)

    with general_detail_container:
        st.title("User General Details")
        col1, col2 = st.columns(2)
        

        with col1:
            elder_id = st.text_input("User ID", value="D0001", help="Enter the numerical ID")
            user_age = st.text_input("Age", value=None, help="Enter your age")
            
        
        # uploaded_file = st.file_uploader("Choose a txt file", type=['txt'], accept_multiple_files=False)
        
        # if uploaded_file:
        #     bytes_data = ""
        #     bytes_data = uploaded_file.read()

        # col1, col2 = st.columns([4,1])
        
        with col2:
            user_gender = option = st.selectbox("Gender", ("Male", "Female"))
            button = st.button("Submit", type = "primary", use_container_width=True)

    # if button: 
    #     if elder_id == "":
    #         st.warning("Please enter the Elder ID")
    #     elif not uploaded_file:
    #         st.warning("Please upload a text file")
    #     elif elder_id < default_elder_id:
    #         st.error(f"Elder id already exists. Please use {default_elder_id} as elder id")
    #     elif uploaded_file and elder_id != "":
    #         data = str(bytes_data)
    #         state = True #add_patient(st.session_state.my_gemini, st.session_state.my_graph, elder_id, care_note_mode=False, care_note="", data=data)
    #         if state:
    #             st.success("Elder added successfully")
    #         if not state:
    #             st.error("There was a error while adding the Elder.")
    #         pass
        

# elif selected == "Care Note Enhancement":
#     st.title("Care Note Enhancement")

#     with st.form(key='care_note_form'):
#         col1, col2 = st.columns(2)

#         with col1:
#             elder_id = st.text_input("Elder ID", value="", help="Enter the numerical ID")
        
#         with col2:
#             date = st.date_input("Date")
#             time = st.time_input("Time")

#         # Care note text area outside the columns but still inside the form
#         original_care_note = st.text_area("Enter the Care Note:", height=200)

#         # Form submit button
#         col1, col2 = st.columns([4,1])

#         with col2:
#             st.session_state.button = st.form_submit_button("Submit", type = "primary", use_container_width=True)
        
#     if 'button_clicked' not in st.session_state:
#         st.session_state.button_clicked = False
#     if 'add_button_shown' not in st.session_state:
#         st.session_state.add_button_shown = True

#     # Your existing button and condition checks
#     if st.session_state.button and not elder_id:
#         st.warning("Please enter the Elder ID")
#     elif st.session_state.button and not original_care_note:
#         st.warning("Please enter the care note to enhance")
#     elif st.session_state.button and elder_id and original_care_note:
#         st.session_state.enhanced_note, st.session_state.suggestions_note  = note_enhancer(original_care_note, st.session_state.my_gemini)
#         st.session_state.text_copy = f"""{st.session_state.enhanced_note}"""
#         st.session_state.text_copy_suggestions = f"""{st.session_state.suggestions_note}"""
#         st.session_state.button_clicked = True
        
#     if "text_copy" in st.session_state and st.session_state.text_copy:
#         st.subheader("Generated Care Enhancement Note")
#         editable_note = st.text_area(label="",value=st.session_state.text_copy, height=200)
#         st.subheader("Generated Suggestions")
#         st.code("\n".join(tw.wrap(st.session_state.text_copy_suggestions, width=80)), language="md")
#         #st.code("\n".join(tw.wrap(st.session_state.text_copy, width=80)), language="md")

#         col1, col2 = st.columns([4,1])
#         if st.session_state.button_clicked:
#             with col2:
#                 add_button = st.button("Add Care Note", type = "primary", use_container_width=True)
#             if add_button:
#                 print("Adding the care note")
#                 state = add_patient(st.session_state.my_gemini, st.session_state.my_graph, elder_id, care_note_mode=True, care_note=editable_note, data="")
#                 if state:
#                     st.success("Care Note added successfully")
#                 else:
#                     st.error("There was an error while adding the care note.")
        
# elif selected == "Care Plan Generation":
#     st.title("Care Plan Generation")

#     col1, col2 = st.columns(2)

#     with col1:
#         elder_id = st.text_input("Elder ID", value="", help="Enter the numerical ID")

#     with col2:
#         st.write("") 
#         st.write("")  
#         generation_button = st.button("Submit", type="primary")

#     if generation_button and elder_id:
#         care_plan = generate_plan(elder_id, GeminiInitializer=st.session_state.my_gemini, GraphInitializer=st.session_state.my_graph)
#         st.session_state.care_plan = care_plan 
#     elif not elder_id and generation_button:
#         st.warning("Please fill in the elder ID to generate the care plan.")

#     if 'care_plan' in st.session_state and st.session_state.care_plan:
#         st.subheader("Generated Care Plan")
#         st.markdown(st.session_state.care_plan)

#         result_pdf = create_pdf("\n".join(tw.wrap(st.session_state.care_plan, width=80)))

#         # Download button
#         col1, col2 = st.columns([2,1])

#         with col2:
#             st.download_button(label="Download Care Plan as a PDF",
#                             data=result_pdf,
#                             file_name=f"care_plan_{elder_id}.pdf",
#                             mime='application/pdf',
#                             type="primary")
