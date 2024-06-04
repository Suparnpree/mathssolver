from PIL import Image
import re
import base64
from google.generativeai.types.generation_types import StopCandidateException
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import streamlit as st
from streamlit.errors import DuplicateWidgetID
api = 'AIzaSyDikOI5RAYv7Hh_vUNgTUv_SKx5_RJOGh4'

def encode_and_convert_image(image_path):
    # Read the image file as binary
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read())
        decoded_image = base64.b64decode(encoded_image)
        image_buffer = BytesIO(decoded_image)
        return image_buffer


def gemini(image,input=""):
    if image != None:
        model = ChatGoogleGenerativeAI(model="gemini-pro-vision", google_api_key=api)
        img = Image.open(image)
        # img = encode_and_convert_image(im)
        temp = f"""You are a teacher. You should clear my all maths doubt by just seeing the image 
    
            so here is my doubt.
            {input} and {img}
        """


        try:
            prompt = HumanMessage(
                content=[
                    {
                        "type": "text",
                        "text": temp,
                    },
                    {
                        "type": "image_url",
                        "image_url": img,
                    },
                ]
            )

            # Call the Langchain model to generate a roast
            response = model.invoke([prompt])
        except StopCandidateException as e:
            e_str = str(e)
            text_pattern = r'text:\s*"([^"]*)"'

            # Find all matches using the regular expression
            matches = re.findall(text_pattern, e_str)

            # Print the extracted text
            for match in matches:
                return match
    else:
        model = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=api)
        # img = encode_and_convert_image(im)
        temp = f"""You are a teacher. You should clear my all maths doubt. 

            so here is my doubt.
            {input}
        """

        try:
            prompt = HumanMessage(
                content=[
                    {
                        "type": "text",
                        "text": temp,
                    },
                ]
            )

            # Call the Langchain model to generate a roast
            response = model.invoke([prompt])

        except StopCandidateException as e:
            e_str = str(e)
            text_pattern = r'text:\s*"([^"]*)"'

            # Find all matches using the regular expression
            matches = re.findall(text_pattern, e_str)

            # Print the extracted text
            for match in matches:
                return match
    return response.content
def main():
    # Title and description
    st.title("Gemini Maths Solver")
    st.write("Welcome to the Gemini Maths Solver! Upload an image of a math problem or type your question below.")

    # Initialize session state for messages
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display past messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    try:
        # Layout for image upload and text input at the bottom
        with st.form(key="input_form"):
            col1, col2 = st.columns([2, 3])
            with col1:
                image = st.file_uploader("Upload an image (optional):", type=["jpg", "jpeg", "png"])
            with col2:
                prompt = st.text_input("Enter your doubt:")

            # Submit button
            submit_button = st.form_submit_button(label="Submit")

        # Process the user input
        if submit_button and prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                response = gemini(
                    input=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                    image=image
                )
                st.markdown(response)

            st.session_state.messages.append({"role": "assistant", "content": response})

    except Exception as e:
        st.error(f"An error occurred: {e}")
main()