import streamlit as st
import google.generativeai as genai
import os
st.markdown("""
<style>
/* Page background and layout */
body {
    background-color: #f3fdf7;
    font-family: 'Segoe UI', sans-serif;
}

/* Header Animation */
h1 {
    color: #4CAF50;
    font-size: 2.8em;
    text-align: center;
    animation: fadeIn 2s ease-in-out;
    margin-bottom: 30px;
}

/* Primary Button Styling */
button[kind="primary"] {
    background-color: #4CAF50 !important;
    color: white !important;
    font-weight: 600;
    border-radius: 12px;
    padding: 10px 20px;
    transition: all 0.3s ease;
}

button[kind="primary"]:hover {
    background-color: #388e3c !important;
    transform: scale(1.05);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

/* Input box */
input, select, textarea {
    border-radius: 8px !important;
    border: 1px solid #cfcfcf !important;
    padding: 10px !important;
    font-size: 1em !important;
}

/* Spinner customization */
.css-1cpxqw2 {
    color: #4CAF50 !important;
}

/* Animation */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Divider and section headers */
hr {
    border-top: 2px dashed #ccc;
    margin: 20px 0;
}
</style>
""", unsafe_allow_html=True)

API_KEY = "im removing this for my safety" # <<< PASTE YOUR API KEY HERE

try:
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error(f"Failed to configure Google Generative AI. Error: {e}")
    st.info("Please ensure your API Key is correct and try again.")
    st.stop() 


model = genai.GenerativeModel('gemini-2.0-flash')
st.set_page_config(page_title="Personalized Diet Recommender", layout="centered")

# Centered project name
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>NutriGene</h1>", unsafe_allow_html=True)


# --- Streamlit Application UI ---

st.set_page_config(page_title="Personalized Diet Recommender", layout="centered")

# st.title(" Personalized Diet Recommender")
st.markdown("Enter your details and diet preferences to get a customized diet plan!")

# Input fields for user data
st.header("Your Information")
col1, col2 = st.columns(2)

with col1:
    height_cm = st.number_input("Height (cm)", min_value=50.0, max_value=300.0, value=170.0, step=1.0)
with col2:
    weight_kg = st.number_input("Weight (kg)", min_value=10.0, max_value=500.0, value=70.0, step=0.5)

st.header("Diet Preferences")
diet_goal = st.selectbox(
    "What is your main diet goal or preference?",
    (
        "General Healthy Eating",
        "Weight Loss",
        "Muscle Gain",
        "Keto Diet",
        "Vegetarian",
        "Vegan",
        "Low Carb",
        "High Protein",
        "Diabetic Friendly",
        "Other (please specify below)"
    )
)

if diet_goal == "Other (please specify below)":
    custom_diet_preference = st.text_input("Please specify your custom diet preference:")
else:
    custom_diet_preference = ""

# --- Generate Diet Button ---
if st.button("Generate Diet Plan ✨", type="primary"):
    if not API_KEY or API_KEY == "YOUR_API_KEY_HERE":
        st.error("Please replace 'YOUR_API_KEY_HERE' with your actual Google Generative AI API Key in the code.")
    elif not height_cm or not weight_kg:
        st.warning("Please enter both your height and weight.")
    else:
        # Calculate BMI for additional context in the prompt
        height_m = height_cm / 100
        bmi = weight_kg / (height_m ** 2)
        st.info(f"Your calculated BMI: **{bmi:.2f}**")

        # Construct the prompt for the AI model
        prompt = f"""
        Generate a detailed 7-day diet plan for an individual with the following characteristics:
        - Height: {height_cm} cm
        - Weight: {weight_kg} kg
        - BMI: {bmi:.2f}

        Their primary diet goal/preference is: {diet_goal}
        """
        if custom_diet_preference:
            prompt += f"Specific custom preference: {custom_diet_preference}\n"

        prompt += """
        Please provide a balanced and realistic meal plan for breakfast, lunch, dinner, and 1-2 snacks per day.
        Include diverse food options and consider nutritional balance.
        Format the output clearly, perhaps day by day, with meal types.
        Focus on healthy, whole foods. Do not include calorie counts unless explicitly asked.
        """

        st.spinner("Generating your personalized diet plan... This might take a moment. ⏳")
        try:
            # Make the API call to the Generative AI model
            response = model.generate_content(prompt)
            # Display the generated diet plan
            st.success("Diet Plan Generated!")
            st.markdown("---")
            st.write(response.text)
            st.markdown("---")
            st.info("Remember, this is an AI-generated suggestion and should not replace professional medical or nutritional advice. Consult with a healthcare professional before making significant changes to your diet.")

        except Exception as e:
            st.error(f"An error occurred while generating the diet plan: {e}")
            st.warning("Please check your internet connection and API key. If the issue persists, the model might be experiencing temporary issues.")

