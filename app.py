from dotenv import load_dotenv

load_dotenv() #Load all the env variables from .env

import streamlit as st 
import os
from PIL import Image
import google.generativeai as genai 

os.getenv("GEMINI_API_KEY")
genai.configure(api_key = os.getenv("GEMINI_API_KEY"))

#function to load Gemini-Pro-Vision



def get_gemini_response(input,image,prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response  = model.generate_content([input,image[0],prompt])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


def main():
    st.set_page_config(page_title="Play with Invoice")

    st.header("Multilanguage Invoice Extrator using Gemini AI")
    input = st.text_input("Ask Question : ",key="input")
    uploaded_file = st.file_uploader("Choose an image of the invoice...",type=["jpg","jpeg","png"])
    image=""
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image,caption="Uploaded Image",use_column_width = True)
        submit = st.button("Generate answers")
        input_prompt = """
        You are an expert in understanding invoices. We will upload a image as invoice
        and you will have the answer the question based on the uploaded images and 
        questions asked
        """
        if submit:
            image_data = input_image_setup(uploaded_file)
            response = get_gemini_response(input_prompt,image_data,input)
            st.subheader("The Response is")
            st.write(response)

if __name__ == '__main__':
    main()
