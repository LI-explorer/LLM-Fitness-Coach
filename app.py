import streamlit as st
from google import genai
import json

st.set_page_config(page_title="AI Fit Coach", page_icon="💪")
api_key = st.sidebar.text_input("Enter Google API Key", type="password")

if api_key:
    client = genai.Client(api_key=api_key)
    
    st.title("🏃‍♂️ AI Personal Fitness Coach")
    st.markdown("Achieve your goals with AI-driven insights.")

    # 2. User Info Section (Input)
    with st.expander("Step 1: Your Profile"):
        col1, col2 = st.columns(2)
        age = col1.number_input("Age", 18, 100, 25)
        gender = col2.selectbox("Gender", ["Male", "Female", "Other"])
        weight = col1.number_input("Weight (kg)", 30.0, 200.0, 70.0)
        height = col2.number_input("Height (cm)", 100, 250, 175)
        goal = st.selectbox("Your Goal", ["Weight Loss", "Muscle Gain", "Endurance", "General Health"])

    # 3. Generating the Plan
    if st.button("Generate My Fitness & Menu Plan"):
        # We wrap the user data into a JSON-like prompt for better LLM understanding
        user_context = {
            "age": age, "gender": gender, "weight": weight, 
            "height": height, "goal": goal
        }
        
        prompt = f"""
        You are an expert Fitness Coach and Nutritionist. 
        User Profile: {json.dumps(user_context)}
        
        Please provide:
        1. A brief fitness strategy.
        2. A sample daily menu (Breakfast, Lunch, Dinner, Snack).
        3. Estimated daily calorie target.
        Format the output using clear Markdown headings.
        """
        
        with st.spinner("Analyzing your profile..."):
            response = client.models.generate_content(
                model="gemini-2.0-flash", contents=prompt
            )
            st.success("Analysis Complete!")
            st.markdown(response.text)

    st.divider()

    # 4. Daily Intake Evaluation (Feedback)
    st.subheader("🥗 Log Your Meal")
    meal_desc = st.text_area("What did you eat today? (e.g., 'A bowl of salad and 200g grilled chicken')")
    
    if st.button("Evaluate My Meal"):
        eval_prompt = f"""
        Based on a {goal} goal for a {weight}kg {gender}, evaluate this meal: "{meal_desc}".
        Tell me if it's 'Good', 'Neutral', or 'Poor' for the goal. 
        Give a rough calorie estimate and a suggestion for improvement.
        """
        with st.spinner("Checking nutrition..."):
            eval_response = client.models.generate_content(
                model="gemini-2.0-flash", contents=eval_prompt
            )
            st.info(eval_response.text)

else:
    st.warning("Please enter your Google API Key in the sidebar to start.")
