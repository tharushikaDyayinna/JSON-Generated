import streamlit as st
import google.generativeai as genai
import json

# --- Configure your Gemini API key ---
GOOGLE_API_KEY = "AIzaSyDH1gjDkBreFvDT3KcRb2TFJ1pApas-laI"  
genai.configure(api_key=GOOGLE_API_KEY)

# --- Load Gemini model ---
model = genai.GenerativeModel('models/gemma-3-12b-it')

# --- Streamlit UI ---
st.set_page_config(page_title="Form JSON Generator", page_icon="🧠", layout="centered")
st.title("Smart System Form JSON Generator")
st.markdown("Enter your system creation requirement below, and this app will generate a JSON structure automatically using Gemini.")

user_input = st.text_area("✏️ Enter your system creation requirement:", "", height=150)

if st.button("🚀 Generate JSON"):
    if user_input.strip():
        json_structure_example = """{
            "formData": {
                "entType": "Real Smart",
                "formCat": "Register",
                "newformName": "Form 1",
                "frequency": "any",
                "editable": 1,
                "deletable": 1,
                "newRec": 1,
                "parentID": 0
            },
            "fieldsData": [
                {"data_name": "EmployeeName", "data_type": "text", "attributes": "required"},
                {"data_name": "EmployeeID", "data_type": "sequence", "prefix": "E", "digits": "3"},
                {"data_name": "TotalValue", "data_type": "calculation", "calculation": "{Employee}.{Salary} * {Employee}.{DaysWorked}"}
            ]
        }"""

        prompt = f"""Generate a JSON object for the following system creation requirement:
Requirement: {user_input}
JSON Structure Example:
{json_structure_example}

**Important Note:** When the data_type is "calculation", ensure the formula uses {{formname}}.{{fieldname}} format.

Generated JSON:
"""
        response = model.generate_content(prompt)
        st.subheader("✅ Generated JSON Output")
        st.code(response.text, language="json")
    else:
        st.warning("Please enter a requirement before clicking Generate.")
