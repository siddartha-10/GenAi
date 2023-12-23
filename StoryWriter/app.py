from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = ChatGoogleGenerativeAI(model="gemini-pro-vision")


# Streamlit app
def main():
    st.title("Interactive Storytelling Platform")

    # User input
    starting_point = st.text_area("Input a starting point for the story:")
    uploaded_image = st.file_uploader("Upload a relevant image:", type=["jpg", "png", "jpeg"])

    if st.button("Generate Story"):
        if starting_point:
            # Generate story text using GPT-3
            story_text = generate_story(starting_point)

            # Display the generated story
            st.markdown("## Generated Story:")
            st.write(story_text)

            # Display the uploaded image
            if uploaded_image:
                st.markdown("## Uploaded Image:")
                st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)

        else:
            st.warning("Please provide a starting point for the story.")

# Function to generate story using GPT-3
def generate_story(starting_point):
    prompt = f"Once upon a time, {starting_point}."
    
    response = model.invoke(prompt)
    return response.content

if __name__ == "__main__":
    main()
