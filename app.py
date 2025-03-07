
import streamlit as st
import base64
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_community.tools import DuckDuckGoSearchRun

def encode_image(image_file):
    """Encode an uploaded image to base64."""
    return base64.b64encode(image_file.read()).decode('utf-8')

def get_image_description(image_data):
    """Use GPT-4o to describe the image."""
    model = ChatOpenAI(model="gpt-4o")
    message = HumanMessage(
        content=[
            {"type": "text", "text": "Identify the historical place in this image. Provide its name, location, and a brief historical context."},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
        ]
    )
    response = model.invoke([message])
    return response.content

def web_search(query):
    """Perform web search using DuckDuckGo."""
    search = DuckDuckGoSearchRun()
    return search.run(query)

def create_historical_place_app():
    """Create Streamlit app for historical place identification and research."""
    st.title("Historical Place Identifier and Research Assistant")

    uploaded_file = st.file_uploader("Upload an image of a historical place", type=['png', 'jpg', 'jpeg'])

    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

        image_data = encode_image(uploaded_file)

        try:
            place_description = get_image_description(image_data)
            st.subheader("Image Analysis")
            st.write(place_description)

            default_place_name = place_description.split('\n')[0].strip()
            place_name = st.text_input("Confirm or edit the place name:", value=default_place_name)

            user_query = st.text_area("Ask any specific question about this historical place:")

            if st.button("Submit Question"):
                if user_query.strip():
                    search_results = web_search(place_name)

                    st.subheader("Research Findings")
                    st.write(search_results)

                    model = ChatOpenAI(model="gpt-4o")
                    context_message = HumanMessage(
                        content=f"""Provide a detailed answer to the question '{user_query}' about {place_name}, 
                        using the information from these search results: {search_results}. Include relevant sources."""
                    )
                    context_response = model.invoke([context_message])

                    st.subheader("Detailed Response")
                    st.write(context_response.content)
                else:
                    st.warning("Please enter a specific question.")

        except Exception as e:
            st.error(f"An error occurred: {e}")

def main():
    st.sidebar.header("Configuration")
    openai_api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")

    if openai_api_key:
        os.environ["OPENAI_API_KEY"] = openai_api_key
        create_historical_place_app()
    else:
        st.warning("Please enter your OpenAI API Key")

if __name__ == "__main__":
    main()
