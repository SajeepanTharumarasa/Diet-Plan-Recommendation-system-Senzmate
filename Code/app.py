import base64
import textwrap as tw
from io import BytesIO

import diet_planner
import make_conditions
import pandas as pd
import streamlit as st

# from care_note_enhancement import note_enhancer
# from care_plan_generator import generate_plan
from gemini_initializer import GeminiInitializer
from KG_retrever import run_query

# from graph_initializer import GraphInitializer
# from knowledge_graph import add_patient, get_next_patient_id
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from streamlit_option_menu import option_menu

# Check if the session state variables are initialized
if "bmi" not in st.session_state:
    st.session_state.bmi = 29.5
if "body_fat" not in st.session_state:
    st.session_state.body_fat = 19.71
if "glucose" not in st.session_state:
    st.session_state.glucose = 245.0
if "tc" not in st.session_state:
    st.session_state.tc = 166.0
if "bp_sys" not in st.session_state:
    st.session_state.bp_sys = 113.0
if "hba1c" not in st.session_state:
    st.session_state.hba1c = 2.2
if "tg" not in st.session_state:
    st.session_state.tg = 175.0
if "hdl" not in st.session_state:
    st.session_state.hdl = 55.0
if "ldl" not in st.session_state:
    st.session_state.ldl = 97.0
if "tc_hdl" not in st.session_state:
    st.session_state.tc_hdl = 3.77
if "bp_dias" not in st.session_state:
    st.session_state.bp_dias = 66.0
if "user_age" not in st.session_state:
    st.session_state.user_age = 30
if "user_weight" not in st.session_state:
    st.session_state.user_weight = 70
if "user_height" not in st.session_state:
    st.session_state.user_height = 172
if "food_preference" not in st.session_state:
    st.session_state.food_preference = "Veg"
if "food_type" not in st.session_state:
    st.session_state.food_type = "North Indian"
if "user_gender" not in st.session_state:
    st.session_state.user_gender = "Male"

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
    options=["Home","General Info","Medical Info","Diet-Planning"],
    icons=["house","clipboard-heart-fill","card-list","calendar-heart-fill"],
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
    image_path = "backround.jpg" 
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
    

elif selected == "General Info":
    st.title("General Info")

    general_detail_container = st.container(border=True)

    with general_detail_container:
        col1, col2 = st.columns(2)
        

        with col1:
            st.session_state.elder_id = st.text_input("User ID", value="D0001", help="Enter the numerical ID")
            st.session_state.user_age = st.number_input("Age", value=st.session_state.user_age, help="Enter your age")
            st.session_state.food_preference  = st.selectbox("Food Preference", ("Veg", "Non-Veg"))
            st.session_state.food_type = option = st.selectbox("Food Region", ("North Indian","South Indian"))

                    
        with col2:
            st.session_state.user_gender = option = st.selectbox("Gender", ("Male", "Female"))
            st.session_state.user_weight = st.number_input("Weight(Kg)", value=st.session_state.user_weight, help="Enter your Weight")
            st.session_state.user_height = st.number_input("Height(cm)", value=st.session_state.user_height, help="Enter your Height")

elif selected == "Medical Info":
    st.title("Medical Info")

    medical_detail_container = st.container(border=True)

    with medical_detail_container:
        col1, col2 = st.columns(2)
        
        with col1:
            st.session_state.bmi = st.number_input("BMI", value=st.session_state.bmi, help="Enter your BMI")
            st.session_state.body_fat = st.number_input("Body fat", value=st.session_state.body_fat, help="Enter your Body fat")
            st.session_state.glucose = st.number_input("Glucose", value=st.session_state.glucose, help="Enter your Glucose")
            st.session_state.tc = st.number_input("Total Cholesterol (Tc)", value=st.session_state.tc, help="Enter your Total Cholesterol")
            st.session_state.bp_sys = st.number_input("Systolic Blood Pressure", value=st.session_state.bp_sys, help="Enter your Systolic Blood Pressure")
            st.session_state.hba1c = st.number_input("Diastolic Blood Pressure", value=st.session_state.hba1c, help="Enter your Diastolic Blood Pressure")

                    
        with col2:
            st.session_state.tg = st.number_input("Triglycerides", value=st.session_state.tg, help="Enter your Triglycerides")
            st.session_state.hdl = st.number_input("High-Density Lipoprotein (HDL)", value=st.session_state.hdl, help="Enter your Weight")
            st.session_state.ldl = st.number_input("Low-Density Lipoprotein ", value=st.session_state.ldl, help="Enter your Low-Density Lipoprotein ")
            st.session_state.tc_hdl = st.number_input("Total Cholesterol/HDL Ratio (Tc/Hdl)", value=st.session_state.tc_hdl, help="Enter your Height")
            st.session_state.bp_dias = st.number_input("Height", value=st.session_state.bp_dias, help="Enter your Height")

elif selected == "Diet-Planning":
    st.title("Diet-Planning")

    user_note = st.container(border=True)
    generated_plan = st.container(border=True)
    save_expert_suggestion = st.container(border=True)

    daily_need_calori, diet_recommendation, dieses = make_conditions.make_conditioner(st.session_state.user_gender, 
                                                                                              st.session_state.user_age, 
                                                                                              st.session_state.bmi, 
                                                                                              st.session_state.glucose, 
                                                                                              st.session_state.user_height, 
                                                                                              st.session_state.user_weight, 
                                                                                              st.session_state.tc, 
                                                                                              st.session_state.tg, 
                                                                                              st.session_state.hdl, 
                                                                                              st.session_state.ldl, 
                                                                                              st.session_state.tc_hdl, 
                                                                                              st.session_state.hba1c)

    with user_note:
        st.write("Summary of Your Health & Daily Needs")
        st.write(f" - Age: {st.session_state.user_age}")
        st.write(f" - Gender: {st.session_state.user_gender}")
        st.write(f" - BMI: {st.session_state.bmi:.2f}")
        st.write(f" - According to your BMI your diet goal is {diet_recommendation}")
        st.write(f" - You have {dieses} dieses")
        st.write(f" - Your Daily Calori need for your diet goal is {daily_need_calori} Cal")

        
        
        # button = st.button("Submit", type = "primary", use_container_width=True)


    with generated_plan:
        button = st.button("Generate Diet Plan", type = "primary", use_container_width=True)
        if button:
            
            kg_data = run_query(st.session_state.food_type, 
                                st.session_state.food_preference, 
                                dieses, 
                                diet_recommendation, 
                                daily_need_calori)
            data = {
                    "food_type": st.session_state.food_type,
                    "food_preference": st.session_state.food_preference,
                    "diseases": dieses,
                    "diet_recommendation": diet_recommendation,
                    "daily_need_calories": daily_need_calori
                        }
            print(kg_data)
            response = diet_planner.gemini_bot(data,kg_data)
            st.write(response)

    with save_expert_suggestion:
        expert_suggestion = st.text_input("Expert Suggestion", value="", help="Enter expert suggestion")
        save_button = st.button("Save", type = "primary", use_container_width=True)
            

