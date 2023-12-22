import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.llms import CTransformers

# Load the model
def llama_model(input_text,no_of_words,blog_style):
    # here we are loading the model
    llm = CTransformers(
        model = "/Users/siddartha/Desktop/OpenSource_LLM's/llama-2-7b-chat.ggmlv3.q8_0.bin",
        model_type = "llama",
        config = ({
            "max_new_tokens": 200,
            "temperature": 0.1,
        })
    )

    # here we are creating a template for the prompt
    template = """
    Write a blog on the topic of {input_text} for {blog_style} audience. 
    The blog should be {no_of_words} words long.
    """

    # here we are creating a prompt using the template and the input variables
    prompt = PromptTemplate(input_variables=["input_text","blog_style","no_of_words"],template=template)

    # here we are generating the blog
    response = llm(prompt.format(input_text=input_text,blog_style=blog_style,no_of_words=no_of_words))
    print(response)
    return response


st.set_page_config(page_title="Generate Blog",initial_sidebar_state="collapsed",layout="centered")

st.header("Generate Blog")

input_text = st.text_input("Enter the topic of the blog you want to generate")

## creating 2 columns for additional 2 fields
col1, col2 = st.columns([5,5])
with col1:
    no_of_words = st.text_input("Enter the number of words you want to generate")

with col2:
    blog_style = st.selectbox("Writing the blog for ",("Researchers or Professionals","General Audience"),index=0)

submit_button = st.button("Generate Blog")


if submit_button:
    st.write(llama_model(input_text,no_of_words,blog_style))


