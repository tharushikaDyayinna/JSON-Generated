import streamlit as st
import google.generativeai as genai
import json

# --- Configure your Gemini API key ---
# NOTE: Replace with your actual key or use st.secrets in a real deployment
GOOGLE_API_KEY = "AIzaSyDH1gjDkBreFvDT3KcRb2TFJ1pApas-laI"  
genai.configure(api_key=GOOGLE_API_KEY)

# --- Load Gemini model ---
# Using gemma-3-12b-it as per original code
model = genai.GenerativeModel('models/gemma-3-12b-it')

# --- Streamlit UI ---
st.set_page_config(page_title="Form JSON Generator", page_icon="📝", layout="centered")
st.title("Smart System Form JSON Generator")
st.markdown("Enter your system creation requirement below, and this app will generate a **complete, detailed JSON structure** automatically using Gemini.")

user_input = st.text_area("✏️ Enter your system creation requirement (e.g., 'A form for inventory tracking with fields for Item Name (text), Quantity (number), Unit Price (number), and a calculated Total Price.'):", "", height=150)

if st.button("🚀 Generate JSON"):
    if user_input.strip():
        
        # --- UPDATED JSON STRUCTURE EXAMPLE WITH FULL FIELD SCHEMA ---
        json_structure_example = """{
            "formData": {
                "entType": "Real Smart",
                "formCat": "Register",
                "newformName": "InventoryForm", 
                "frequency": "any",
                "editable": 1,
                "deletable": 1,
                "newRec": 1,
                "parentID": 0
            },
            "fieldsData": [
                {
                    "data_name": "ItemName",
                    "data_type": "text",
                    "sorting_value": "1",
                    "identifier": 0,
                    "options_from": "",
                    "fetch_function": "",
                    "calculation": "",
                    "defaultVal": "",
                    "features": "",
                    "inherit": 0,
                    "attributes": "required",
                    "entityMethod": "",
                    "entityOrLevel": "",
                    "mapping": [],
                    "keyMember": 0,
                    "sumClass": "",
                    "data_info": "",
                    "help_text": "Name of the item.",
                    "sum_func": "",
                    "countIf": "",
                    "decimals": "0"
                },
                {
                    "data_name": "Quantity",
                    "data_type": "number",
                    "sorting_value": "2",
                    "identifier": 0,
                    "options_from": "",
                    "fetch_function": "",
                    "calculation": "",
                    "defaultVal": "",
                    "features": "",
                    "inherit": 0,
                    "attributes": "required",
                    "entityMethod": "",
                    "entityOrLevel": "",
                    "mapping": [],
                    "keyMember": 0,
                    "sumClass": "",
                    "data_info": "",
                    "help_text": "Number of units.",
                    "sum_func": "",
                    "countIf": "",
                    "decimals": "0"
                },
                {
                    "data_name": "TotalValue",
                    "data_type": "calculation",
                    "sorting_value": "3",
                    "identifier": 0,
                    "options_from": "",
                    "fetch_function": "",
                    "calculation": "{InventoryForm.Quantity} * {InventoryForm.UnitPrice}",
                    "defaultVal": "",
                    "features": "",
                    "inherit": 0,
                    "attributes": "readonly",
                    "entityMethod": "",
                    "entityOrLevel": "",
                    "mapping": [],
                    "keyMember": 0,
                    "sumClass": "",
                    "data_info": "",
                    "help_text": "Calculated total value of inventory items.",
                    "sum_func": "",
                    "countIf": "",
                    "decimals": "2"
                }
            ]
        }"""
        
        # --- PROMPT INSTRUCTION IS UPDATED TO ENSURE ADHERENCE TO NEW SCHEMA ---
        prompt = f"""Generate a complete JSON object for the following system creation requirement.
        
        **CRITICAL INSTRUCTION**: Every object generated within the "fieldsData" array MUST strictly adhere to the full structure provided in the JSON Structure Example, including all keys like 'sorting_value', 'identifier', 'options_from', etc., even if their values are empty strings or 0. Populate the values based on the requirement.
        
        Requirement: {user_input}
        
        JSON Structure Example (Use this exact schema for every field):
        {json_structure_example}

        **Important Note:** When the data_type is "calculation", ensure the formula uses the exact {{FormName}}.{{FieldName}} format. Use the form name specified in formData.newformName for calculations (e.g., 'InventoryForm').
        
        Generated JSON:
        """
        
        try:
            # Generate content from the model
            response = model.generate_content(prompt)
            generated_json_text = response.text
            
            # Attempt to parse and re-format the JSON for clean display (optional but recommended)
            try:
                # Clean up the output by stripping markdown blocks if present
                if generated_json_text.strip().startswith('```json'):
                    generated_json_text = generated_json_text.replace('```json', '').replace('```', '').strip()
                
                # Validate and re-format the JSON
                parsed_json = json.loads(generated_json_text)
                formatted_json = json.dumps(parsed_json, indent=4)
                
            except json.JSONDecodeError:
                # If parsing fails, use the raw response text
                formatted_json = generated_json_text
                st.error("Warning: The generated content is not perfectly valid JSON, displaying raw text.")


            # Display the JSON
            st.subheader("Generated JSON Output")
            st.code(formatted_json, language="json")

            # Add Download Button
            st.download_button(
                label="Download JSON",
                data=formatted_json,
                file_name="generated_form.json",
                mime="application/json"
            )
            
        except Exception as e:
            st.error(f"An error occurred during API call: {e}")

    else:
        st.warning("Please enter a requirement before clicking Generate.")
