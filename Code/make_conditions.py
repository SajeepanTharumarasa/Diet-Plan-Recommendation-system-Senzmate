
def make_conditioner(gender, age, bmi, glucose, height_cm, weight_kg, tc, tg, hdl, ldl, tc_hdl, hba1c):
  
    diabetes_status = evaluate_diabetes(float(glucose), hba1c, age, gender)
    cholesterol_status = is_cholesterol_normal(tc, ldl, hdl, tg, tc_hdl, gender)

    if diabetes_status and not cholesterol_status:
        dieses = "Diabetes"
    elif diabetes_status and cholesterol_status:
        dieses ="Cholesterol"
    elif cholesterol_status and not diabetes_status:
        dieses = "Cholesterol"
    else:
        dieses = None

    # bmi = calculate_bmi(weight_kg, height_cm)
    diet_recommendation = weight_recommendation(bmi)



    activity_level = 'moderately_active'

    if diet_recommendation == "Weight Loss":
        weight_change_per_week = 0.7 # pounds
    elif diet_recommendation == "Weight Gain":
        weight_change_per_week = 0.5
    else:
        weight_change_per_week =0

    daily_calories_needed = calculate_caloric_needs(weight_kg, height_cm, age, gender, activity_level, diet_recommendation, weight_change_per_week)
    print(daily_calories_needed)
    if daily_calories_needed <1300:
        daily_need_calori = 1200
    elif daily_calories_needed >1300 and daily_calories_needed<1700:
        daily_need_calori = 1600
    elif daily_calories_needed>1701 and daily_calories_needed<2100:
        daily_need_calori = 2000
    elif daily_calories_needed>2101:
        daily_need_calori = 2400
    
    print("daily_calories_needed",daily_calories_needed)
    return daily_need_calori, diet_recommendation, dieses,daily_calories_needed


def calculate_caloric_needs(weight, height, age, gender, activity_level, goal='Maintain', weight_change_per_week=0):
    # BMR calculation based on gender
    if gender == 'male':
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    
    # Activity multiplier
    activity_multipliers = {
        'sedentary': 1.2,
        'lightly_active': 1.375,
        'moderately_active': 1.55,
        'very_active': 1.725,
        'super_active': 1.9
    }
    
    tdee = bmr * activity_multipliers.get(activity_level, 1.2)  # Default to sedentary if no match
    
    # Caloric adjustment for weight change goal
    calorie_adjustment = weight_change_per_week * 500  # weight_change_per_week in pounds
    
    if goal == 'Weight Loss':
        daily_calories = tdee - calorie_adjustment
    elif goal == 'Weight Gain':
        daily_calories = tdee + calorie_adjustment
    else:
        daily_calories = tdee  # Maintain weight
    
    return daily_calories

def calculate_bmi(weight_kg, height_cm):
    # Convert height from cm to meters
    height_m = height_cm / 100
    
    # Calculate BMI
    bmi = weight_kg / (height_m ** 2)
    
    return round(bmi, 2)

def weight_recommendation(bmi):
    # Define BMI categories based on standard guidelines
    bmi_categories = {
        "underweight": (0, 18.5),
        "normal": (18.5, 24.9),
        "overweight": (25, 29.9),
        "obesity": (30, 39.9),
        "severe_obesity": (40, float('inf'))
    }
    # Determine the BMI category
    if bmi <18.5:
        category = "Weight Gain"
        return category
    elif bmi < 24.9:
        # maintain the same weight
        category = "Weight Loss"
        return category
    elif bmi <29.9:
        category = "Weight Loss"
        return category
    elif bmi < 39.9:
        category = "Weight Loss"
        return category
    else:
        category = "Weight Loss"
    
    return category

def evaluate_diabetes(glucose, hba1c, age, gender):
    # Evaluate fasting glucose levels
    if glucose < 100:
        glucose_status = 'Normal'
    elif 100 <= glucose < 126:
        glucose_status = 'Prediabetes'
    else:
        glucose_status = 'Diabetes'
    
    # Evaluate HbA1c levels
    if hba1c < 5.7:
        hba1c_status = 'Normal'
    elif 5.7 <= hba1c < 6.5:
        hba1c_status = 'Prediabetes'
    else:
        hba1c_status = 'Diabetes'
    
    # Determine overall diabetes status
    if glucose_status == 'Diabetes' or hba1c_status == 'Diabetes':
        diabetes_status = True #'Diabetes'
    elif glucose_status == 'Prediabetes' or hba1c_status == 'Prediabetes':
        diabetes_status = True #'Prediabetes'
    else:
        diabetes_status = False #'Normal'
    
   

    return diabetes_status

def is_cholesterol_normal(tc, ldl, hdl, tg, tc_hdl_ratio, gender):
    # Total Cholesterol (Tc) Normal Range
    if not (tc < 200):
        return True
    
    # Low-Density Lipoprotein (LDL) Normal Range
    if not (ldl < 100):
        return True
    
    # High-Density Lipoprotein (HDL) Normal Range
    if gender == 'male':
        if not (hdl >= 40):
            return True
    elif gender == 'female':
        if not (hdl >= 50):
            return True
    
    # Triglycerides (Tg) Normal Range
    if not (tg < 150):
        return True
    
    # Total Cholesterol/HDL Ratio (Tc/Hdl) Normal Range
    if not (tc_hdl_ratio < 4):
        return True
    
    return False
