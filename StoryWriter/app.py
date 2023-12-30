import os
import streamlit as st
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
# Load environment variables from .env file
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model_gemini = ChatGoogleGenerativeAI(model="gemini-pro")


def model(genre,no_of_characters,location,characters_prompt,hook_prompt,climax_prompt):
    # here we are creating a template for the prompt
    main_c = """
    Crafting a compelling short film necessitates a concise and straightforward premise, a key ingredient for success when storytelling within the constraints of a limited timeframe. The best short films often feature a main character with a specific goal or a tight deadline, such as two friends embarking on a bike ride, a woman seeking new friendship, or a grieving son delivering a eulogy. With time being a precious commodity, short films cannot afford to delve extensively into character backstories. Instead, filmmakers must discern the essential information required to engage the audience in the hero's journey. 
    Details like an ex-husband may prove extraneous and dilute the impact of the narrative.Moreover, judiciously selecting the number of characters is pivotal. 
    Each character, whether a protagonist, supporting role, or minor part, should serve a purpose directly tied to the central goal. 
    If a character's exclusion doesn't impede the main character's progression, 
    it might be prudent to omit them. Many successful short films unfold within a singular location, not only to streamline the story but also to mitigate budgetary constraints, 
    particularly for independent filmmakers. "Sam Did It," a renowned 10-minute short set entirely in a morgue operating room, exemplifies how a confined space can intensify the storytelling experience.
     A useful exercise during brainstorming involves formulating a premise and identifying a single location, prompting creators to contemplate whether the entire narrative can unfold within those confines. 
    This approach not only sharpens the focus but also aligns with budget considerations for those contemplating a self-produced project.
    
    """

    template = main_c +"""
    write a short film story in {genre} genre with {no_of_characters} characters in {location} location
    Consider being economical with characters and backstory There are {characters_prompt} characters and their behaviours. This is the hook {hook_prompt} 
    and this is the climax {climax_prompt}
    """

    # here we are creating a prompt using the template and the input variables
    prompt = PromptTemplate(input_variables=["genre","no_of_characters","location","characters_prompt","hook_prompt","climax_prompt"],template=template)

    # here we are generating the blog
    response = model_gemini.invoke(prompt.format(genre=genre,no_of_characters=no_of_characters,location=location,characters_prompt=characters_prompt,hook_prompt=hook_prompt,climax_prompt=climax_prompt))
    print(response)
    return response.content

def short_film_story_generator(genre):
    st.title("Short Film Story Generator")

    # Prompt for being economical with characters and backstory
    no_of_characters = st.text_input("How many character do you want? (leave empty for default of 4 characters):")
    if not no_of_characters:
        # Default characters if the user leaves it empty
        no_of_characters = "The story follows four characters who..."
    # Prompt for minimal locations
    location = st.text_input("Think about keeping the locations to a minimum. Specify a key location for your short film (leave empty for random location):")
    if not location:
        # Default location if the user leaves it empty
        location = "You can use any location you want"

    # Prompt for interesting characters
    characters_prompt = st.text_input("Describe interesting traits or quirks of the main characters:")
    if not characters_prompt:
        characters_prompt = "You can use any interesting traits or quirks you want"

    # Prompt for the hook
    hook_prompt = st.text_input("Create a hook for your short film:")
    if not hook_prompt:
        # Default hook if the user leaves it empty
        hook_prompt = "You can use any hook you want"


    # Prompt for the climax
    climax_prompt = st.text_input("Develop a great climax for your short film:")
    if not climax_prompt:
        climax_prompt = "You can use climax you want but should match with the genre"


    if st.button("Generate Story"):
        response = model(genre,no_of_characters,location,characters_prompt,hook_prompt,climax_prompt)

        # Extract the AI's response and display it
        ai_response = response
        st.write(f"{ai_response}")

if __name__ == "__main__":
    genres = ["Sci-Fi", "Drama", "Comedy", "Thriller", "Mystery", "Fantasy", "Horror", "Romance", "Action", "Adventure"]
    
    # Create a dropdown menu for genres
    user_genre = st.sidebar.selectbox("Select the genre:", genres, index=genres.index("Sci-Fi"))

    short_film_story_generator(user_genre)
