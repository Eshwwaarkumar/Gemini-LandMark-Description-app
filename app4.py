import streamlit as st
import base64
import google.generativeai as genai

def encode_image(image_file):
    """Encode an uploaded image to base64."""
    return base64.b64encode(image_file.read()).decode('utf-8')

def get_image_description(image_data, gemini_api_key):
    """Use Gemini Pro Vision to describe the image."""
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')
    img_data = base64.b64decode(image_data)
    img = {"mime_type": "image/jpeg", "data": img_data}
    response = model.generate_content([
        "Identify the historical place in this image. Provide its name, location, and a brief historical context.",
        img
    ])
    return response.text

def create_historical_place_app():
    """Create Streamlit app for historical place identification and research."""
    st.title("Historical Place Identifier and Research Assistant")

    uploaded_file = st.file_uploader("Upload an image of a historical place", type=['png', 'jpg', 'jpeg'])

    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

        image_data = encode_image(uploaded_file)

        try:
            place_description = get_image_description(image_data, st.session_state.gemini_api_key)
            st.subheader("Image Analysis")
            st.write(place_description)
            lines = place_description.split('\n')
            extracted_name = "Name Not Found"
            extracted_address = "Address Not Found"
            for line in lines:
                line = line.strip()
                if line.startswith("*   **Name:**"):
                    extracted_name = line.split("**Name:**")[1].strip().replace("**", "").strip()
                elif line.startswith("*   **Location:**"):
                    extracted_address = line.split("Location:**")[1].strip().replace("**", "").strip()

            # default_place_name = place_description.split('\n')[2].strip()
            # print(f"this '{default_place_name}'")
            # default_place_address = place_description.split('\n')[3].strip()
            # print(f"this '{default_place_address}'")
            # extracted_name = default_place_name.split("Name:**")[1].strip().replace("**", "").strip()
            print(f"this '{extracted_name}'")
            # extracted_address = default_place_address.split("Location:**")[1].strip().replace("**", "").strip()
            print(f"this '{extracted_address}'")

            place_name = st.text_input("Confirm or edit the place name:", value=extracted_name)

            user_query = st.text_area("Ask any specific question about this historical place:")

            if st.button("Submit Question"):
                if user_query.strip():
                    genai.configure(api_key=st.session_state.gemini_api_key)
                    model = genai.GenerativeModel('gemini-2.0-flash')
                    response = model.generate_content(
                        f"""Provide a detailed answer to the question '{user_query}' about {extracted_name} at {extracted_address}. Include relevant sources."""
                    )
                    st.subheader("Detailed Response")
                    st.write(response.text)
                else:
                    st.warning("Please enter a specific question.")

            st.sidebar.subheader("Nearby Information")
            if st.sidebar.button("Hotels Nearby"):
                genai.configure(api_key=st.session_state.gemini_api_key)
                model = genai.GenerativeModel('gemini-2.0-flash')
                response = model.generate_content(
                    f"What are some hotels near {extracted_name} at {extracted_address}?"
                )
                st.subheader("Hotels Nearby")
                st.write(response.text)

            if st.sidebar.button("Viewpoints"):
                genai.configure(api_key=st.session_state.gemini_api_key)
                model = genai.GenerativeModel('gemini-2.0-flash')
                response = model.generate_content(
                    f"What are some good viewpoints of {extracted_name} at {extracted_address}?"
                )
                st.subheader("Viewpoints")
                st.write(response.text)

            if st.sidebar.button("Nearby Attractions"):
                genai.configure(api_key=st.session_state.gemini_api_key)
                model = genai.GenerativeModel('gemini-2.0-flash')
                response = model.generate_content(
                    f"What are some nearby attractions near {extracted_name} at {extracted_address}?"
                )
                st.subheader("Nearby Attractions")
                st.write(response.text)

            st.sidebar.subheader("Historical Details")
            if st.sidebar.button("Significance"):
                genai.configure(api_key=st.session_state.gemini_api_key)
                model = genai.GenerativeModel('gemini-2.0-flash')
                response = model.generate_content(
                    f"What is the historical significance of {extracted_name} at {extracted_address}?"
                )
                st.subheader("Significance")
                st.write(response.text)

            if st.sidebar.button("Architectural Features"):
                genai.configure(api_key=st.session_state.gemini_api_key)
                model = genai.GenerativeModel('gemini-2.0-flash')
                response = model.generate_content(
                    f"What are the notable architectural features of {extracted_name} at {extracted_address}?"
                )
                st.subheader("Architectural Features")
                st.write(response.text)

            if st.sidebar.button("Interesting Facts"):
                genai.configure(api_key=st.session_state.gemini_api_key)
                model = genai.GenerativeModel('gemini-2.0-flash')
                response = model.generate_content(
                    f"What are some interesting facts about {extracted_name} at {extracted_address}?"
                )
                st.subheader("Interesting Facts")
                st.write(response.text)

            st.sidebar.subheader("-----------------")
            if st.sidebar.button("Restrictions"):
                genai.configure(api_key=st.session_state.gemini_api_key)
                model = genai.GenerativeModel('gemini-2.0-flash')
                response = model.generate_content(
                    f"What are restrictions at {extracted_name} at {extracted_address}?"
                )
                st.subheader("Restrictions")
                st.write(response.text)

        except Exception as e:
            st.error(f"An error occurred: {e}")

def main():
    st.sidebar.header("Configuration")
    #gemini_api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
    gemini_api_key = "AIzaSyD7Njw8pb6v_EsUii9mg9E_UqoQUywb9ns"
    if gemini_api_key:
        st.session_state.gemini_api_key = gemini_api_key
        create_historical_place_app()
    else:
        st.warning("Please enter your Gemini API Key")

if __name__ == "__main__":
    main()