import streamlit as st
import google.generativeai as genai
import json
#import os
#from dotenv import load_dotenv

#load_dotenv()

#GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
#genai.configure(api_key=GOOGLE_API_KEY)


GOOGLE_API_KEY = "AIzaSyDH1gjDkBreFvDT3KcRb2TFJ1pApas-laI"  
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-2.5-flash-preview-09-2025')

st.set_page_config(page_title="Form JSON Generator", page_icon="", layout="centered")
st.title("Smart System Form JSON Generator")
#st.markdown("Enter your system creation requirement below, and this app will generate a **complete, detailed JSON structure**.")

user_input = st.text_area("Enter your system creation requirement :", "", height=150)

if st.button("Generate JSON"):
    if user_input.strip():
        
        # The calculation field now uses the complex cross-form fetching syntax as the example.
        json_structure_example = """{
            "formData": {
                "entType": "T Department",
                "formCat": "T Form",
                "newformName": "Invoice", 
                "frequency": "any",
                "editable": 1,
                "deletable": 1,
                "newRec": 1,
                "parentID": 0
            },
            "fieldsData": [
                {
                    "data_name": "InvoiceID",
                    "data_type": "sequence",
                    "sorting_value": "1",
                    "identifier": 0,
                    "options_from": "",
                    "fetch_function": "",
                    "calculation": "",
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
                    "help_text": "",
                    "sum_func": "",
                    "countIf": "",
                    "decimals": "0",
                    "prefix": "INV",
                    "sufix": "",
                    "digits": "5",
                    "replacer": "0",
                    "start_with": "1"
                },
                {
                    "data_name": "CustomerName",
                    "data_type": "options",
                    "sorting_value": "2",
                    "identifier": 0,
                    "options_from": "CustomerEntity",
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
                    "help_text": "",
                    "sum_func": "",
                    "countIf": "",
                    "decimals": "",
                    "formName": "Customers"
                },
                {
                    "data_name": "InvoiceDate",
                    "data_type": "date",
                    "sorting_value": "3",
                    "identifier": 0,
                    "options_from": "",
                    "fetch_function": "",
                    "calculation": "",
                    "defaultVal": "TODAY",
                    "features": "",
                    "inherit": 0,
                    "attributes": "required",
                    "entityMethod": "",
                    "entityOrLevel": "",
                    "mapping": [],
                    "keyMember": 0,
                    "sumClass": "",
                    "data_info": "",
                    "help_text": "",
                    "sum_func": "",
                    "countIf": "",
                    "decimals": ""
                },
                {
                    "data_name": "ProductID",
                    "data_type": "options",
                    "sorting_value": "4",
                    "identifier": 0,
                    "options_from": "ProductsEntity",
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
                    "help_text": "",
                    "sum_func": "",
                    "countIf": "",
                    "decimals": "",
                    "formName": "Products"
                },
                {
                    "data_name": "Quantity",
                    "data_type": "number",
                    "sorting_value": "5",
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
                    "help_text": "",
                    "sum_func": "",
                    "countIf": "",
                    "decimals": "0"
                },
                {
                    "data_name": "UnitPrice",
                    "data_type": "number",
                    "sorting_value": "6",
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
                    "help_text": "",
                    "sum_func": "",
                    "countIf": "",
                    "decimals": "2"
                },
                {
                    "data_name": "LineTotal",
                    "data_type": "calculation",
                    "sorting_value": "7",
                    "identifier": 0,
                    "options_from": "",
                    "fetch_function": "",
                    "calculation": "{GoodsReceived^QuantityReceived^GoodsReceived.GRNLineID,RequestForm.CurrentLine,=} * {PurchaseOrder^UnitPrice^PurchaseOrder.POLineID,RequestForm.CurrentLine,=}",
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
                    "help_text": "",
                    "sum_func": "",
                    "countIf": "",
                    "decimals": "2"
                }
            ]
        }"""
        
        # --- CORRECTED PROMPT INSTRUCTION ---
        prompt = f"""Generate a complete JSON object for the following system creation requirement.

        **CRITICAL INSTRUCTION**: Every object generated within the "fieldsData" array MUST strictly adhere to the full structure provided in the JSON Structure Example, including all keys.
        **MANDATORY**: The value for the `help_text` key MUST ALWAYS be an empty string (`""`) for ALL fields.
        **SPECIAL INSTRUCTION FOR OPTIONS**: For any field with data_type: "options", you **MUST** include the "formName" key to specify the source form.

        **SPECIAL INSTRUCTION FOR FETCH_FUNCTION**: If the user asks to fetch or look up data from another form into a static field, use the `fetch_function` key with the following syntax:
        `fm^fd^rf1,tf1,lo1 and rf2,tf2,lo2 ^ Entity Level Type`
        Where fm=form name, fd=field name of value needed, rfx=reference field in current form, tfx=target field in fm, lox=logic (EQUAL, GREATER, LESS, etc.).

        **IMPORTANT INSTRUCTION FOR CALCULATION**: Calculations must use one of the following two formats. Use the complex format when a value needs to be fetched from another form within the calculation.

        1. Simple internal reference: **{{FormName.FieldName}}** (e.g., {{Invoice.Quantity}} * {{Invoice.Price}})
        
        2. Complex cross-form reference (to fetch values and calculate): **{{SourceForm^SourceField^MappingField,CurrentValue,Operator}}** - **The expression must use double braces and match the LineTotal example format** (e.g., {{{{GoodsReceived^QuantityReceived^GoodsReceived.GRNLineID,RequestForm.CurrentLine,=}}}} * {{{{PurchaseOrder^UnitPrice^PurchaseOrder.POLineID,RequestForm.CurrentLine,=}}}}).
        
        Requirement: {user_input}
        
        JSON Structure Example (Use this exact schema for every field and match the structure of fields like 'sequence', 'options', and 'calculation'):
        {json_structure_example}

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

            # Download
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
