import streamlit as st
import requests
import base64
import re
from PIL import Image
import pdfplumber
from deep_translator import GoogleTranslator
from streamlit_js_eval import get_geolocation


# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="AI Medical Assistant",
    page_icon="🩺",
    layout="wide"
)

# ---------------- BACKGROUND IMAGE ---------------- #

def get_base64(image_path):
    with open(image_path, "rb") as img:
        data = base64.b64encode(img.read()).decode()
    return data

bg_image = get_base64("images/medical_bg.jpg")

# ---------------- CUSTOM CSS ---------------- #

page_bg = f"""
<style>

.stApp {{
    background-image: url("data:image/jpg;base64,{bg_image}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

.main-box {{
    background-color: rgba(255,255,255,0.90);
    padding: 35px;
    border-radius: 25px;
    box-shadow: 0px 5px 25px rgba(0,0,0,0.25);
    margin-top: 20px;
}}

.title {{
    text-align: center;
    font-size: 52px;
    font-weight: bold;
    color: #0d47a1;
}}

.subtitle {{
    text-align: center;
    font-size: 22px;
    color: #444;
    margin-bottom: 30px;
}}

textarea {{
    font-size: 18px !important;
}}

.stButton button {{
    width: 100%;
    background-color: #1565c0;
    color: white;
    border-radius: 12px;
    height: 52px;
    font-size: 18px;
    border: none;
    font-weight: bold;
}}

.stButton button:hover {{
    background-color: #0d47a1;
}}

section[data-testid="stSidebar"] {{
    background-color: #0d47a1;
}}

section[data-testid="stSidebar"] * {{
    color: white;
}}

[data-testid="stFileUploader"] {{
    background-color: rgba(255,255,255,0.85);
    border-radius: 15px;
    padding: 15px;
}}

.medical-response {{
    background-color: rgba(240,255,240,0.97);
    padding: 35px;
    border-radius: 20px;
    margin-top: 30px;
    border-left: 8px solid #43a047;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.15);
}}

.response-text {{
    white-space: pre-wrap;
    font-size: 18px;
    line-height: 2;
    color: #1b5e20;
    font-family: Arial, sans-serif;
    font-weight: 500;
}}

</style>
"""

st.markdown(page_bg, unsafe_allow_html=True)

# ---------------- SIDEBAR ---------------- #

st.sidebar.title("🩺 AI Medical Assistant")

st.sidebar.markdown("""
### Platform Features

🏥 Hospital Locator

💊 Medical Shop Finder

📄 PDF Report Analysis

🖼 Medical Image Analysis

🌍 Multi Language Support

🚨 Emergency Detection

📊 Health Risk Assessment

🤖 Gemini AI Powered
""")

st.sidebar.markdown("---")

st.sidebar.success("🟢 System Online")

# ---------------- MAIN CONTAINER ---------------- #

st.markdown(
    '<div class="main-box">',
    unsafe_allow_html=True
)

# ---------------- TITLE ---------------- #

st.markdown(
    '<div class="title">🩺 AI Medical Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
    AI Powered Healthcare Intelligence Platform
    </div>
    """,
    unsafe_allow_html=True
)

st.info(
    "🏥 Medical Consultation | 📄 Report Analysis | 🖼 Image Analysis | 🚨 Emergency Detection"
)

# ---------------- WARNING ---------------- #

st.warning(
    "This AI assistant is for educational purposes only."
)

# ---------------- LANGUAGE ---------------- #

language = st.selectbox(
    "🌍 Select Language",
    [
        "English",
        "Hindi",
        "Kannada",
        "Telugu",
        "Tamil"
    ]
)

lang_dict = {
    "English": "en",
    "Hindi": "hi",
    "Kannada": "kn",
    "Telugu": "te",
    "Tamil": "ta"
}

st.markdown("## 📊 Medical Dashboard")

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric("AI Status", "Online")

with m2:
    st.metric("Language", language)

with m3:
    st.metric("Reports", "Ready")

with m4:
    st.metric("Services", "10+")

# ---------------- LOCATION ---------------- #

location = get_geolocation()

lat = None
lon = None

if location:
    lat = location['coords']['latitude']
    lon = location['coords']['longitude']

# ---------------- QUESTION ---------------- #

question = st.text_area(
    "🎤 Ask Medical Question (Use Win + H for Voice Typing)",
    height=120,
    placeholder="Example: Snake bite with breathing problem"
)

# ---------------- FILE UPLOAD ---------------- #

uploaded_file = st.file_uploader(
    "📎 Upload Medical Report / Image",
    type=["pdf", "png", "jpg", "jpeg", "txt"]
)

document_text = ""

# ---------------- FILE PROCESSING ---------------- #

if uploaded_file is not None:

    if uploaded_file.type == "application/pdf":
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    document_text += text
        st.success("✅ PDF Uploaded Successfully")

    elif uploaded_file.type.startswith("image"):
        image = Image.open(uploaded_file)
        st.image(
            image,
            caption="Uploaded Medical Image",
            use_container_width=True
        )
        document_text = """
        Analyze this uploaded medical image carefully
        and provide medical insights.
        """
        st.success("✅ Medical Image Uploaded Successfully")

    elif uploaded_file.type == "text/plain":
        document_text = uploaded_file.read().decode("utf-8")
        st.success("✅ Text File Uploaded Successfully")

# ---------------- EMERGENCY SERVICES ---------------- #

st.markdown("---")
st.subheader("🚑 Emergency Healthcare Services")
st.caption("Find nearby hospitals and medical stores instantly")

col3, col4 = st.columns(2)

with col3:
    if lat and lon:
        hospital_url = (
            f"https://www.google.com/maps/search/hospitals/@{lat},{lon},15z"
        )
        st.link_button(
            "🏥 Nearby Hospitals",
            hospital_url
        )

with col4:
    if lat and lon:
        medical_url = (
            f"https://www.google.com/maps/search/medical+shops/@{lat},{lon},15z"
        )
        st.link_button(
            "💊 Nearby Medical Shops",
            medical_url
        )

# ---------------- BUTTONS ---------------- #

col1, col2 = st.columns(2)

with col1:
    ask_button = st.button("🧠 Generate Medical Intelligence Report")

with col2:
    clear_button = st.button("🗑 Clear")

# ---------------- CLEAR ---------------- #

if clear_button:
    st.rerun()

# ---------------- ASK AI ---------------- #

if ask_button:

    final_question = f"""
    You are an advanced medical AI assistant.

    Analyze the following medical condition carefully.

    User Medical Information:
    {question}

    Uploaded Medical Information:
    {document_text}

    Provide detailed professional medical analysis including:

    🩺 Disease
    🧬 Causes
    🤒 Symptoms
    💊 Medicines
    🩹 Treatment
    🥗 Diet Suggestions
    ⚠ Precautions
    🚨 Emergency Warning

    At the absolute end of your response, you MUST print these exact three lines with your final assessment:
    [SEVERITY] -> High (or Medium or Low)
    [DEATH_RISK] -> High (or Medium or Low)
    [ATTENTION] -> Yes (or No)

    Use real medical reasoning.
    """

    if question.strip() or document_text.strip():

        with st.spinner("🔍 AI is analyzing medical information..."):

            try:
                response = requests.post(
                    "http://127.0.0.1:8000/ask",
                    json={
                        "question": final_question
                    },
                    timeout=60
                )

                if response.status_code == 200:
                    data = response.json()
                    answer = data.get(
                        "response",
                        "No response from AI"
                    )
                else:
                    answer = "Backend API Error"

                # ---------------- TRANSLATION ---------------- #

                translated_answer = GoogleTranslator(
                    source='auto',
                    target=lang_dict[language]
                ).translate(answer)

                # ---------------- CLEAN RESPONSE ---------------- #

                clean_answer = translated_answer

                # REMOVE HTML TAGS
                clean_answer = re.sub(
                    r'<[^>]+>',
                    '',
                    clean_answer
                )

                # REMOVE MARKDOWN SYMBOLS
                symbols_to_remove = [
                    "**",
                    "##",
                    "###",
                    "`"
                ]

                for symbol in symbols_to_remove:
                    clean_answer = clean_answer.replace(
                        symbol,
                        ""
                    )

                # ---------------- NORMALIZED TEXT FOR LOGIC ---------------- #

                normalized_answer = answer.lower()

                # ---------------- EXTENDED MULTI-COLOR RISK DETECTION ---------------- #

                severity = "low"
                show_emergency_alert = False

                # 1. Tier 1 (Critical Black): Absolute top risk condition triggers (e.g. Strokes, Attacks, Kidney Failures)
                black_keywords = [
                    "intracranial hemorrhage", 
                    "hemorrhagic stroke", 
                    "acute myocardial infarction", 
                    "cardiac troponin i", 
                    "brain parenchyma",
                    "stage 5 acute-on-chronic kidney"
                ]

                # 2. Tier 2 (Severe Red): Severe progressive parameters that trigger long term complications
                red_keywords = [
                    "primary lung carcinoma", 
                    "tuberculous consolidation", 
                    "neoplastic mass", 
                    "necrotizing lobar pneumonia",
                    "[severity] -> high"
                ]

                # 3. Tier 3 (Medium Yellow): Moderate updates
                medium_keywords = [
                    "[severity] -> medium",
                    "progressive shortness of breath"
                ]

                # Evaluate risk matching cascade down
                for word in black_keywords:
                    if word in normalized_answer:
                        severity = "critical_black"
                        break

                if severity == "low":
                    for word in red_keywords:
                        if word in normalized_answer:
                            severity = "severe_red"
                            break

                if severity == "low":
                    for word in medium_keywords:
                        if word in normalized_answer:
                            severity = "medium_yellow"
                            break

                # Safety validation block to ensure normal checks never trigger alarms
                if "[severity] -> low" in normalized_answer or "low risk / healthy profile" in normalized_answer:
                    severity = "low"

                # Establish emergency system alert mapping
                if severity in ["critical_black", "severe_red"] or "[attention] -> yes" in normalized_answer:
                    show_emergency_alert = True

                # ---------------- HEALTH RISK METER ---------------- #

                st.subheader("📊 Dynamic Health Risk Assessment")

                if severity == "critical_black":
                    meter_color = "#000000"  # Solid Black
                    percentage = "100%"
                    status_text = "🚨 CRITICAL THREAT: IMMEDIATE LIFE-SPAN REDUCTION AND IMMINENT FATAL RISK EFFECT"
                    alert_function = st.error

                elif severity == "severe_red":
                    meter_color = "#d32f2f"  # Deep Progressive Red
                    percentage = "75%"
                    status_text = "⚠ SEVERE PROGRESSION RISK: PROLONGED COMPLICATIONS & EXTREME SUFFERING WITHOUT IMMEDIATE TREATMENT"
                    alert_function = st.error

                elif severity == "medium_yellow":
                    meter_color = "#fbc02d"  # Warning Yellow
                    percentage = "50%"
                    status_text = "⚠ MODERATE RISK: CLINICAL INVESTIGATION AND GENERAL CONSULTATION REQUIRED"
                    alert_function = st.warning

                else:
                    meter_color = "#388e3c"  # Safety Green
                    percentage = "25%"
                    status_text = "✅ SAFE PROFILE: PARAMETERS ARE SAFELY WITHIN NORMAL BIOLOGICAL REFERENCE RANGES"
                    alert_function = st.success

                # Display text description box
                alert_function(status_text)

                # Inject dynamic custom HTML color changing progress bar
                st.markdown(
                    f"""
                    <div style="
                        width: 100%; 
                        background-color: #e0e0e0; 
                        border-radius: 10px; 
                        padding: 3px; 
                        box-shadow: inset 0 1px 3px rgba(0,0,0,.2);
                        margin-bottom: 25px;
                    ">
                        <div style="
                            width: {percentage}; 
                            background-color: {meter_color}; 
                            height: 20px; 
                            border-radius: 8px;
                            transition: width 0.5s ease-in-out;
                        "></div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # ---------------- EMERGENCY ALERT ---------------- #

                if show_emergency_alert:
                    st.error("""
                    🚨 MEDICAL EMERGENCY DETECTED
                    Immediate medical attention is recommended.
                    Please contact emergency healthcare services or visit the nearest hospital.
                    """)

                # ---------------- RESPONSE BOX ---------------- #

                st.markdown(
                    f"""
                    <div class="medical-response">
                        <h2 style="color:#1565c0;
                        font-size:34px;
                        margin-bottom:20px;
                        font-weight:bold;
                        margin-top:0;">
                        🤖 AI Medical Intelligence Report
                        </h2>
                        <div class="response-text">
                            {clean_answer}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # ---------------- DOCTOR SUPPORT ---------------- #

                st.subheader(
                    "👨‍⚕ Recommended Medical Support"
                )

                if severity in ["critical_black", "severe_red"]:
                    st.error(
                        "Immediate specialist or emergency medical attention recommended."
                    )
                    st.link_button(
                        "🚑 Apollo Emergency",
                        "https://www.apollohospitals.com"
                    )

                elif severity == "medium_yellow":
                    st.warning(
                        "General physician consultation recommended."
                    )
                    st.link_button(
                        "🩺 Find Doctors",
                        "https://www.practo.com"
                    )

                else:
                    st.success(
                        "Basic home care guidance may help."
                    )

                # ---------------- DOWNLOAD REPORT ---------------- #

                st.download_button(
                    "📄 Download Medical Intelligence Report",
                    translated_answer,
                    file_name="medical_report.txt"
                )

            except Exception as e:
                st.error(f"Error: {e}")

    else:
        st.warning(
            "Please enter a medical question or upload a document."
        )

# ---------------- FOOTER ---------------- #

st.markdown(
    """
    <hr>
    <center>
    <h4>🏥 AI Medical Assistant Platform</h4>

    FastAPI • Gemini AI • Streamlit

    Healthcare Intelligence & Decision Support System
    </center>
    """,
    unsafe_allow_html=True
)