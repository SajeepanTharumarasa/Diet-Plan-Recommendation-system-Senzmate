import json

from gemini_initializer import GeminiInitializer

template = '''
You are a diet recommendation AI that provides personalized meal plans based on user health conditions and preferences.
The user will provide their health metrics and dietary preferences, and you will generate a detailed 1-day meal plan.
The meal plan should include breakfast, lunch, dinner, morning snacks, evening snacks, post-workout snacks, and pre-workout snacks with respective serving quantities.
Each meal should be tailored to the user's specific health goals, whether it is weight loss or weight gain, and should consider their health conditions and dietary preferences.

User Input:

Dietary Preferences:

Preferred Cuisine: [Preferred Cuisine, e.g., South Indian, North Indian, or Maharashtrian]
Preferred Food Type: [Preferred Food Type, e.g., Veg or Non-Veg]
Health Condition: [Health Condition, e.g., Diabetes, Cholesterol, or Thyroid]
Goal: [Goal, e.g., Weight Gain or Weight Loss]

Task:

1.Analyze the provided health metrics to determine if the user should aim for weight loss or weight gain.
2.Based on the user's health goal and dietary preferences, generate a detailed 1-day meal plan.
3.Ensure that the meal plan includes appropriate recommendations for breakfast, lunch, dinner, morning snacks, evening snacks, post-workout snacks, and pre-workout snacks
with respective serving quantities.
4.Retrieve details from the knowledge graph to ensure the meals are tailored to the user's health conditions and dietary preferences.
5.Present the meal plan in a clear and organized manner.

Additional Information:

Ensure that the meals are nutritionally balanced and appropriate for the user's health conditions.
Make use of ingredients and dishes typical of the user's preferred cuisine.
Provide variations in the meals to keep the diet interesting and diverse.
Optimize the results with the most appropriate diet plan. 

If you cannot find any information on the entities and relationships above, return the string ‘N/A’.
DO NOT create any fictitious data.
DO NOT duplicate entities.
DO NOT miss out on any information.
DO NOT impute any missing values.
STRICTLY NEED the output in JSON format.

user_preferences:{user_prefer}
KG_details: {kg_fetch_data}
Answer:

'''

def gemini_bot(user_prefer, kg_fetch_data, gemini=GeminiInitializer()):
    """
    Enhances resident care plan notes by correcting grammar, spelling, and suggesting paraphrases to improve clarity and conciseness.

    Args:
    - text (str): Input text containing a care plan for a resident.
    - gemini (GeminiInitializer): Instance of GeminiInitializer class.

    Returns:
    - str: Improved version of the input text.
    """
    prompt = template.format(user_prefer=user_prefer,kg_fetch_data=kg_fetch_data)
    print(prompt)
    response = gemini.run_text_model(prompt, model_name="gemini-1.5-pro-latest", temperature=0.2)
    print(response)

    return response

    

