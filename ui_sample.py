import streamlit as st
import openai
import pandas as pd

# Securely access the OpenAI API key using st.secrets
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
openai.api_key = OPENAI_API_KEY


def ask_question(prompt):
    completion = openai.chat.completions.create(
        model="gpt-3.5-turbo-0125",  # You can replace this with your preferred model
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )
    return completion.choices[0].message.content


def recommend_hosting_with_ai(dialog, data_csv):
    # Read the CSV data into a string format suitable for the prompt
    hosting_data = pd.read_csv(data_csv)
    hosting_data_string = hosting_data.to_string(index=False)

    # Construct the prompt
    prompt = (f"Based on the following user answers:\n{dialog}\n\n"
              f"And the following hosting service data:\n{hosting_data_string}\n\n"
              "Suggest the best hosting service and return the name, link, and explanation in JSON format.")

    # Call the OpenAI API
    completion = openai.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[{"role": "user", "content": prompt}]
    )

    return completion.choices[0].message.content


def main():
    st.title("Hosting Service Advisor")  # Set a title for your app

    # Load hosting data from CSV
    file_path = 'data.csv'  # Update this with the path to your CSV file

    # Define the questions you're going to ask the user
    # Questions to ask the user
    questions = [
        "What is your monthly budget for web hosting?",
        "How much traffic do you expect your website to have? (e.g., low, medium, high)",
        "What is the primary purpose of your website? (e.g., blog, e-commerce, portfolio)",
        "How would you rate your technical expertise with web hosting and website management? (e.g., beginner, intermediate, advanced)",
        "How important is 24/7 customer support to you?",
        "Do you need WordPress Friendly Hosting Provider?",
        "Are you looking for a hosting service that provides high performance and speed?",
        "Do you anticipate needing to upgrade your hosting plan as your website grows?",
        "Do you have a preference for where your server is located geographically?",
        "Are there any additional features you’re looking for, such as free domain registration, email hosting, or SSL certificates?",
        "Have you used any web hosting services before? If so, what did you like or dislike about them?"
    ]
    dialog = ""  # Initialize an empty string to hold the dialog (not used anymore)

    st.write("Welcome to the Hosting Service Advisor!")  # Display a welcome message

    # Create input boxes for each question
    for question in questions:
        # Streamlit provides various input methods; text_input is used here for simplicity
        user_answer = st.text_input(question, key=question)
        if user_answer:  # Check if the user has provided an answer
            dialog += f"Q: {question}\nA: {user_answer}\n"  # This line is not used anymore

    if st.button('Get Hosting Recommendation'):  # Add a button to trigger recommendation
        if dialog:  # Ensure there's a dialog to process (not strictly necessary anymore)
            recommended_hosting = recommend_hosting_with_ai(dialog, file_path)
            st.text_area("Recommended Hosting Service", value=recommended_hosting, height=300)

# The below line ensures that when you run the script, it calls the main() function
if __name__ == "__main__":
    main()
