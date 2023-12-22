from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = ChatGoogleGenerativeAI(model="gemini-pro")

def gemini_model(input_text,no_of_words,blog_style):
    # here we are creating a template for the prompt
    template = """
    Write a blog on the topic of {input_text} for {blog_style} audience. 
    The blog should be {no_of_words} words long.
    """

    # here we are creating a prompt using the template and the input variables
    prompt = PromptTemplate(input_variables=["input_text","blog_style","no_of_words"],template=template)

    # here we are generating the blog
    response = model.invoke(prompt.format(input_text=input_text,blog_style=blog_style,no_of_words=no_of_words))
    print(response)
    return response.content


st.set_page_config(page_title="Blog Generator", initial_sidebar_state="collapsed", layout="centered")

# Header
st.title("📝 Generate Blog")

# Input Section
input_text = st.text_input("🔍 Enter the topic of the blog you want to generate")

# Creating 2 columns for additional 2 fields
col1, col2 = st.columns([2, 2])

# Number of words input
with col1:
    no_of_words = st.text_input("📏 Number of Words", value="500")

# Blog style selection
with col2:
    blog_style = st.selectbox("📝 Writing the blog for", ("Researchers or Professionals", "General Audience"), index=0)

# Generate Button
submit_button = st.button("Generate Blog 🚀")

# Display the generated blog on button click
if submit_button:
    st.success("📖 **Generated Blog:**")
    generated_blog = gemini_model(input_text, no_of_words, blog_style)
    st.write(generated_blog)
