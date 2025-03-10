import streamlit as st
import matplotlib.pyplot as plt
import random

# Custom CSS for Styling
st.markdown(
    """
    <style>
        body {
            background-color: #f4f4f4;  /* Light gray background */
        }
        .stApp {
            background-color: #f4f4f4;
        }
        .stButton > button {
            width: 100%;
            border-radius: 10px;
            background-color: #FF4B4B;
            color: white;
            font-weight: bold;
            padding: 10px;
        }
        .stButton > button:hover {
            background-color: #D43F3F;
        }
        .stMarkdown h2 {
            color: #4CAF50;
        }
        .info-box {
            padding: 15px;
            border-radius: 10px;
            background-color: #FFEEA9;
            color: black;
            font-weight: bold;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title
st.title("💪 BMI, Meal Plan & Personalized Workout Guide")

# User Inputs
gender = st.selectbox("Select your gender:", ["Male", "Female"])
age = st.slider("Select your age:", 5, 100, 25)
weight = st.number_input("Enter your weight (kg):", min_value=1.0, format="%.2f")
height = st.number_input("Enter your height (cm):", min_value=50.0, format="%.2f")

activity_levels = {
    "Sedentary (little to no exercise)": 1.2,
    "Light activity (1-3 days/week)": 1.375,
    "Moderate activity (3-5 days/week)": 1.55,
    "Very active (6-7 days/week)": 1.725,
    "Super active (twice/day intense training)": 1.9,
}
activity = st.selectbox("Select your activity level:", list(activity_levels.keys()))

goal = st.radio("Select your goal:", ["Lose Weight", "Maintain Weight", "Gain Muscle"])

# BMR Calculation
def calculate_bmr(weight, height, age, gender):
    if gender == "Male":
        return 10 * weight + 6.25 * height - 5 * age + 5
    else:
        return 10 * weight + 6.25 * height - 5 * age - 161

# Macronutrient Calculation
def get_macros(calories):
    return round((calories * 0.3) / 4, 1), round((calories * 0.5) / 4, 1), round((calories * 0.2) / 9, 1)

# Water Intake Calculation
def get_water_intake(weight, activity):
    base_water = weight * 0.033  
    return round(base_water + (0.5 if "Very active" in activity or "Super active" in activity else 0), 2)

# Exercise Plan Generator
def get_exercise_plan(goal):
    exercise_plans = {
        "Lose Weight": [
            ("Cardio (Running) - 30 mins", "Burns ~300 kcal"),
            ("HIIT Workout - 25 mins", "Burns ~350 kcal"),
            ("Jump Rope - 20 mins", "Burns ~250 kcal"),
        ],
        "Maintain Weight": [
            ("Full Body Strength - 45 mins", "Burns ~250 kcal"),
            ("Cycling - 30 mins", "Burns ~200 kcal"),
            ("Pilates - 30 mins", "Burns ~180 kcal"),
        ],
        "Gain Muscle": [
            ("Strength Training - 1 hour", "Burns ~350 kcal"),
            ("Resistance Bands - 40 mins", "Burns ~200 kcal"),
            ("Bodyweight Exercises - 30 mins", "Burns ~180 kcal"),
        ],
    }
    return random.sample(exercise_plans[goal], 2)

# Meal Plan Generator
def get_meal_plan(calories):
    meals = {
        "Breakfast": [
            ("Oatmeal & Peanut Butter", 350),
            ("Scrambled Eggs & Toast", 400),
            ("Greek Yogurt & Granola", 300),
        ],
        "Lunch": [
            ("Grilled Chicken & Quinoa", 600),
            ("Veggie Stir-Fry & Tofu", 500),
            ("Salmon with Sweet Potatoes", 650),
        ],
        "Dinner": [
            ("Steak & Roasted Veggies", 700),
            ("Pasta with Lean Meat Sauce", 650),
            ("Baked Fish with Salad", 600),
        ],
        "Snacks": [
            ("Nuts & Dried Fruits", 200),
            ("Protein Shake", 250),
            ("Hummus & Veggies", 180),
        ]
    }
    return {meal: random.choice(options) for meal, options in meals.items()}

# Calculate BMI, BMR, TDEE
if st.button("Calculate Results"):
    if height > 0:
        bmi = weight / ((height / 100) ** 2)
        bmr = calculate_bmr(weight, height, age, gender)
        tdee = bmr * activity_levels[activity]

        # Adjust Calories Based on Goal
        daily_calories = tdee - 500 if goal == "Lose Weight" else tdee + 300 if goal == "Gain Muscle" else tdee

        # Macronutrients
        protein, carbs, fats = get_macros(daily_calories)

        # Water Intake
        water_intake = get_water_intake(weight, activity)

        # Exercise Plan
        workout_plan = get_exercise_plan(goal)

        st.success(f"📊 Your BMI: {bmi:.2f}")
        st.info(f"🔥 Daily Caloric Target: {daily_calories:.0f} kcal")
        st.subheader("🍽️ Macronutrient Breakdown")
        st.write(f"**Protein:** {protein}g  |  **Carbs:** {carbs}g  |  **Fats:** {fats}g")

        st.subheader("💧 Hydration Recommendation")
        st.write(f"Drink at least **{water_intake}L** of water per day.")

        # Meal Plan
        meal_plan = get_meal_plan(daily_calories)
        st.subheader("🍎 Personalized Meal Plan")
        for meal, (dish, cals) in meal_plan.items():
            st.write(f"**{meal}:** {dish} ({cals} kcal)")

        # Workout Plan
        st.subheader("🏋 Personalized Exercise Plan")
        for exercise, calories in workout_plan:
            st.write(f"**{exercise}** - {calories}")

        # BMI Chart
        fig, ax = plt.subplots(figsize=(8, 4))
        categories = ["Underweight", "Normal", "Overweight", "Obese"]
        bmi_values = [18.5, 24.9, 29.9, 40]
        colors = ["blue", "green", "orange", "red"]
        ax.bar(categories, bmi_values, color=colors, alpha=0.6)
        ax.axhline(bmi, color="black", linestyle="dashed", linewidth=2, label=f"Your BMI: {bmi:.2f}")
        ax.set_ylabel("BMI Value")
        ax.set_title("BMI Categories")
        ax.legend()
        st.pyplot(fig)

    else:
        st.error("⚠ Height must be greater than 0.")
