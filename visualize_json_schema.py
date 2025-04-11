import streamlit as st
import json

# Load the static JSON file
def load_static_json():
    file_path = "combined_outputs_10_files_20250411_024558.json"
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

# Display schema insights
def display_schema(schema):
    st.subheader("Extraction Functions Schema")
    for function in schema:
        with st.expander(f"Schema: {function['name']}", expanded=False):
            st.write(function["description"])
            st.json(function["parameters"])

# Display combined outputs with all fields
def display_outputs_summary(outputs):
    st.subheader("Combined Outputs Summary")
    st.markdown(f"**Total Cases:** {len(outputs)}")
    for idx, output in enumerate(outputs, start=1):
        case_url = output["url"]
        with st.expander(f"Case {idx}"):
            # Add a button icon to open the case URL in a popup
            st.markdown(
                f'<a href="{case_url}" target="_blank" style="text-decoration: none;">'
                f'<button style="background-color: #4CAF50; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer;">'
                f'🔗 Preview AAO Decision</button></a>',
                unsafe_allow_html=True,
            )
            st.markdown("### All Fields")
            st.json(output["json"])

# Main Streamlit app
def main():
    st.title("Features Extraction Overview")
    st.markdown("This app provides insights into the schema and data of the static JSON file.")

    # Load JSON data
    data = load_static_json()

    # Display schema insights
    if "extraction_functions_schema" in data:
        display_schema(data["extraction_functions_schema"])

    # Display combined outputs summary
    if "combined_outputs" in data:
        display_outputs_summary(data["combined_outputs"])
    else:
        st.warning("No combined outputs found in the JSON file.")

if __name__ == "__main__":
    main()
