import streamlit as st
from google import genai
import json

st.set_page_config(page_title="AI Fit Coach", page_icon="💪")
api_key = st.secrets.get("GOOGLE_API_KEY")

# --- DEBUG SECTION ---
# This helps us see if the secret is actually loading
if "GOOGLE_API_KEY" in st.secrets:
    raw_key = st.secrets["GOOGLE_API_KEY"]
    st.sidebar.success(f"✅ Secret found in Streamlit!")
    st.sidebar.write(f"Key length: {len(raw_key)}")
    st.sidebar.write(f"Key starts with: {raw_key[:4]}")
    
    # Check for common invisible character errors
    if raw_key.startswith(" ") or raw_key.endswith(" "):
        st.sidebar.error("⚠️ Warning: Your key has leading or trailing spaces!")
else:
    st.sidebar.error("❌ GOOGLE_API_KEY not found in Secrets!")
    st.stop()

# Initialize the client using the secret
api_key = st.secrets["GOOGLE_API_KEY"]
client = genai.Client(api_key=api_key)
# --- END DEBUG SECTION ---

if not api_key:
    st.error("Missing API Key! Please set GOOGLE_API_KEY in Streamlit Secrets.")
    st.stop() # This stops the app from running further and crashing

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
                model="gemini-2.5-flash", contents=prompt
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
                model="gemini-2.5-flash", contents=eval_prompt
            )
            st.info(eval_response.text)

else:
    st.warning("Please enter your Google API Key in the sidebar to start.")
