import json

from gemini_initializer import GeminiInitializer

base_prompt = """
'''
You are a diet recommendation AI that provides personalized meal plans based on user health conditions and preferences.
The user will provide their health metrics and dietary preferences, and you will generate a detailed 7-days meal plan.
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
2.Based on the user's health goal and dietary preferences, generate a detailed 7-day meal plan. Don't suggest same food for all seven days.
* Don't recommend same food for cosicutive two days
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
STRICTLY NEED the output in JSON format include day as main key.
Example answer:
{
    "Day-1": {
        "Breakfast": {
            "Item": "Upma",
            "Serving Quantity": "1 cup"
        },
        "Morning Snack": {
            "Item": "Apple",
            "Serving Quantity": "1 medium"
        },
        "Lunch": {
            "Item": "2 Wheat Roti, Daal, Gobi matar sabzi, Carrot cucumber salad",
            "Serving Quantity": "2, 1 cup, 1 cup, 1 cup"
        },
        "Evening Snack": {
            "Item": "Roasted chana",
            "Serving Quantity": "1/2 cup"
        },
        "Dinner": {
            "Item": "2 Wheat Roti, Daal, Tofu",
            "Serving Quantity": "2, 1 cup, 100 gms"
        },
        "Pre-workout Snack": {
            "Item": "Papaya",
            "Serving Quantity": "1 cup"
        },
        "Post-workout Snack": {
            "Item": "Moong beans boiled",
            "Serving Quantity": "1/2 cup"
        }
    },
    "Day-2": {
        "Breakfast": {
            "Item": "Upma",
            "Serving Quantity": "1 cup"
        },
        "Morning Snack": {
            "Item": "Cashew Nuts",
            "Serving Quantity": "10 gms"
        },
        "Lunch": {
            "Item": "2 Wheat Roti, Daal, Gobi matar sabzi, Carrot cucumber salad",
            "Serving Quantity": "2, 1 cup, 1 cup, 1 cup"
        },
        "Evening Snack": {
            "Item": "Roasted chana",
            "Serving Quantity": "1/2 cup"
        },
        "Dinner": {
            "Item": "2 Wheat Roti, Daal, Tofu",
            "Serving Quantity": "2, 1 cup, 100 gms"
        },
        "Pre-workout Snack": {
            "Item": "Chia seeds",
            "Serving Quantity": "1 tbsp"
        },
        "Post-workout Snack": {
            "Item": "Moong beans boiled",
            "Serving Quantity": "1/2 cup"
        }
    },
    "Day-3": {
        "Breakfast": {
            "Item": "Upma",
            "Serving Quantity": "1 cup"
        },
        "Morning Snack": {
            "Item": "Almonds",
            "Serving Quantity": "10 gms"
        },
        "Lunch": {
            "Item": "2 Wheat Roti, Daal, Gobi matar sabzi, Carrot cucumber salad",
            "Serving Quantity": "2, 1 cup, 1 cup, 1 cup"
        },
        "Evening Snack": {
            "Item": "Roasted chana",
            "Serving Quantity": "1/2 cup"
        },
        "Dinner": {
            "Item": "2 Wheat Roti, Daal, Tofu",
            "Serving Quantity": "2, 1 cup, 100 gms"
        },
        "Pre-workout Snack": {
            "Item": "Pear",
            "Serving Quantity": "1 medium"
        },
        "Post-workout Snack": {
            "Item": "Moong beans boiled",
            "Serving Quantity": "1/2 cup"
        }
    },
    "Day-4": {
        "Breakfast": {
            "Item": "Upma",
            "Serving Quantity": "1 cup"
        },
        "Morning Snack": {
            "Item": "Apple",
            "Serving Quantity": "1 medium"
        },
        "Lunch": {
            "Item": "2 Wheat Roti, Daal, Gobi matar sabzi, Carrot cucumber salad",
            "Serving Quantity": "2, 1 cup, 1 cup, 1 cup"
        },
        "Evening Snack": {
            "Item": "Roasted chana",
            "Serving Quantity": "1/2 cup"
        },
        "Dinner": {
            "Item": "2 Wheat Roti, Daal, Tofu",
            "Serving Quantity": "2, 1 cup, 100 gms"
        },
        "Pre-workout Snack": {
            "Item": "Granola bar",
            "Serving Quantity": "1"
        },
        "Post-workout Snack": {
            "Item": "Moong beans boiled",
            "Serving Quantity": "1/2 cup"
        }
    },
    "Day-5": {
        "Breakfast": {
            "Item": "Upma",
            "Serving Quantity": "1 cup"
        },
        "Morning Snack": {
            "Item": "Cashew Nuts",
            "Serving Quantity": "10 gms"
        },
        "Lunch": {
            "Item": "2 Wheat Roti, Daal, Gobi matar sabzi, Carrot cucumber salad",
            "Serving Quantity": "2, 1 cup, 1 cup, 1 cup"
        },
        "Evening Snack": {
            "Item": "Roasted chana",
            "Serving Quantity": "1/2 cup"
        },
        "Dinner": {
            "Item": "2 Wheat Roti, Daal, Tofu",
            "Serving Quantity": "2, 1 cup, 100 gms"
        },
        "Pre-workout Snack": {
            "Item": "Apple",
            "Serving Quantity": "1 medium"
        },
        "Post-workout Snack": {
            "Item": "Moong beans boiled",
            "Serving Quantity": "1/2 cup"
        }
    },
    "Day-6": {
        "Breakfast": {
            "Item": "Upma",
            "Serving Quantity": "1 cup"
        },
        "Morning Snack": {
            "Item": "Almonds",
            "Serving Quantity": "10 gms"
        },
        "Lunch": {
            "Item": "2 Wheat Roti, Daal, Gobi matar sabzi, Carrot cucumber salad",
            "Serving Quantity": "2, 1 cup, 1 cup, 1 cup"
        },
        "Evening Snack": {
            "Item": "Roasted chana",
            "Serving Quantity": "1/2 cup"
        },
        "Dinner": {
            "Item": "2 Wheat Roti, Daal, Tofu",
            "Serving Quantity": "2, 1 cup, 100 gms"
        },
        "Pre-workout Snack": {
            "Item": "Cashew Nuts",
            "Serving Quantity": "10 gms"
        },
        "Post-workout Snack": {
            "Item": "Moong beans boiled",
            "Serving Quantity": "1/2 cup"
        }
    },
    "Day-7": {
        "Breakfast": {
            "Item": "Upma",
            "Serving Quantity": "1 cup"
        },
        "Morning Snack": {
            "Item": "Apple",
            "Serving Quantity": "1 medium"
        },
        "Lunch": {
            "Item": "2 Wheat Roti, Daal, Gobi matar sabzi, Carrot cucumber salad",
            "Serving Quantity": "2, 1 cup, 1 cup, 1 cup"
        },
        "Evening Snack": {
            "Item": "Roasted chana",
            "Serving Quantity": "1/2 cup"
        },
        "Dinner": {
            "Item": "2 Wheat Roti, Daal, Tofu",
            "Serving Quantity": "2, 1 cup, 100 gms"
        },
        "Pre-workout Snack": {
            "Item": "Almonds",
            "Serving Quantity": "10 gms"
        },
        "Post-workout Snack": {
            "Item": "Moong beans boiled",
            "Serving Quantity": "1/2 cup"
        }
    }
}
"""
template = '''


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
    prompt = base_prompt + template.format(user_prefer=user_prefer,kg_fetch_data=kg_fetch_data)
    # print(prompt)
    response = gemini.run_text_model(prompt, model_name="gemini-1.5-pro-latest", temperature=0.2)
    print(response)

    return response

def json_formater(bot_response, gemini=GeminiInitializer()):
    base_prompt = """
    You are a JSON formatter AI Bot. Your task is to format the given json_string as a complete, JSON-loadable object. Make sure the output is valid JSON.
    Example answer:
{
    "Day-1": {
        "Breakfast": {
            "Item": "Upma",
            "Serving Quantity": "1 cup"
        },
        "Morning Snack": {
            "Item": "Apple",
            "Serving Quantity": "1 medium"
        },
        "Lunch": {
            "Item": "2 Wheat Roti, Daal, Gobi matar sabzi, Carrot cucumber salad",
            "Serving Quantity": "2, 1 cup, 1 cup, 1 cup"
        },
        "Evening Snack": {
            "Item": "Roasted chana",
            "Serving Quantity": "1/2 cup"
        },
        "Dinner": {
            "Item": "2 Wheat Roti, Daal, Tofu",
            "Serving Quantity": "2, 1 cup, 100 gms"
        },
        "Pre-workout Snack": {
            "Item": "Papaya",
            "Serving Quantity": "1 cup"
        },
        "Post-workout Snack": {
            "Item": "Moong beans boiled",
            "Serving Quantity": "1/2 cup"
        }
    },
    "Day-2": {
        "Breakfast": {
            "Item": "Upma",
            "Serving Quantity": "1 cup"
        },
        "Morning Snack": {
            "Item": "Cashew Nuts",
            "Serving Quantity": "10 gms"
        },
        "Lunch": {
            "Item": "2 Wheat Roti, Daal, Gobi matar sabzi, Carrot cucumber salad",
            "Serving Quantity": "2, 1 cup, 1 cup, 1 cup"
        },
        "Evening Snack": {
            "Item": "Roasted chana",
            "Serving Quantity": "1/2 cup"
        },
        "Dinner": {
            "Item": "2 Wheat Roti, Daal, Tofu",
            "Serving Quantity": "2, 1 cup, 100 gms"
        },
        "Pre-workout Snack": {
            "Item": "Chia seeds",
            "Serving Quantity": "1 tbsp"
        },
        "Post-workout Snack": {
            "Item": "Moong beans boiled",
            "Serving Quantity": "1/2 cup"
        }
    },
    "Day-3": {
        "Breakfast": {
            "Item": "Upma",
            "Serving Quantity": "1 cup"
        },
        "Morning Snack": {
            "Item": "Almonds",
            "Serving Quantity": "10 gms"
        },
        "Lunch": {
            "Item": "2 Wheat Roti, Daal, Gobi matar sabzi, Carrot cucumber salad",
            "Serving Quantity": "2, 1 cup, 1 cup, 1 cup"
        },
        "Evening Snack": {
            "Item": "Roasted chana",
            "Serving Quantity": "1/2 cup"
        },
        "Dinner": {
            "Item": "2 Wheat Roti, Daal, Tofu",
            "Serving Quantity": "2, 1 cup, 100 gms"
        },
        "Pre-workout Snack": {
            "Item": "Pear",
            "Serving Quantity": "1 medium"
        },
        "Post-workout Snack": {
            "Item": "Moong beans boiled",
            "Serving Quantity": "1/2 cup"
        }
    },
    "Day-4": {
        "Breakfast": {
            "Item": "Upma",
            "Serving Quantity": "1 cup"
        },
        "Morning Snack": {
            "Item": "Apple",
            "Serving Quantity": "1 medium"
        },
        "Lunch": {
            "Item": "2 Wheat Roti, Daal, Gobi matar sabzi, Carrot cucumber salad",
            "Serving Quantity": "2, 1 cup, 1 cup, 1 cup"
        },
        "Evening Snack": {
            "Item": "Roasted chana",
            "Serving Quantity": "1/2 cup"
        },
        "Dinner": {
            "Item": "2 Wheat Roti, Daal, Tofu",
            "Serving Quantity": "2, 1 cup, 100 gms"
        },
        "Pre-workout Snack": {
            "Item": "Granola bar",
            "Serving Quantity": "1"
        },
        "Post-workout Snack": {
            "Item": "Moong beans boiled",
            "Serving Quantity": "1/2 cup"
        }
    },
    "Day-5": {
        "Breakfast": {
            "Item": "Upma",
            "Serving Quantity": "1 cup"
        },
        "Morning Snack": {
            "Item": "Cashew Nuts",
            "Serving Quantity": "10 gms"
        },
        "Lunch": {
            "Item": "2 Wheat Roti, Daal, Gobi matar sabzi, Carrot cucumber salad",
            "Serving Quantity": "2, 1 cup, 1 cup, 1 cup"
        },
        "Evening Snack": {
            "Item": "Roasted chana",
            "Serving Quantity": "1/2 cup"
        },
        "Dinner": {
            "Item": "2 Wheat Roti, Daal, Tofu",
            "Serving Quantity": "2, 1 cup, 100 gms"
        },
        "Pre-workout Snack": {
            "Item": "Apple",
            "Serving Quantity": "1 medium"
        },
        "Post-workout Snack": {
            "Item": "Moong beans boiled",
            "Serving Quantity": "1/2 cup"
        }
    },
    "Day-6": {
        "Breakfast": {
            "Item": "Upma",
            "Serving Quantity": "1 cup"
        },
        "Morning Snack": {
            "Item": "Almonds",
            "Serving Quantity": "10 gms"
        },
        "Lunch": {
            "Item": "2 Wheat Roti, Daal, Gobi matar sabzi, Carrot cucumber salad",
            "Serving Quantity": "2, 1 cup, 1 cup, 1 cup"
        },
        "Evening Snack": {
            "Item": "Roasted chana",
            "Serving Quantity": "1/2 cup"
        },
        "Dinner": {
            "Item": "2 Wheat Roti, Daal, Tofu",
            "Serving Quantity": "2, 1 cup, 100 gms"
        },
        "Pre-workout Snack": {
            "Item": "Cashew Nuts",
            "Serving Quantity": "10 gms"
        },
        "Post-workout Snack": {
            "Item": "Moong beans boiled",
            "Serving Quantity": "1/2 cup"
        }
    },
    "Day-7": {
        "Breakfast": {
            "Item": "Upma",
            "Serving Quantity": "1 cup"
        },
        "Morning Snack": {
            "Item": "Apple",
            "Serving Quantity": "1 medium"
        },
        "Lunch": {
            "Item": "2 Wheat Roti, Daal, Gobi matar sabzi, Carrot cucumber salad",
            "Serving Quantity": "2, 1 cup, 1 cup, 1 cup"
        },
        "Evening Snack": {
            "Item": "Roasted chana",
            "Serving Quantity": "1/2 cup"
        },
        "Dinner": {
            "Item": "2 Wheat Roti, Daal, Tofu",
            "Serving Quantity": "2, 1 cup, 100 gms"
        },
        "Pre-workout Snack": {
            "Item": "Almonds",
            "Serving Quantity": "10 gms"
        },
        "Post-workout Snack": {
            "Item": "Moong beans boiled",
            "Serving Quantity": "1/2 cup"
        }
    }
}"""
    template = """
    json_string: "{bot_response}"
    """
    prompt = base_prompt + template.format(bot_response=bot_response)
    # print(prompt)
    response = gemini.run_text_model(prompt, model_name="gemini-1.5-pro-latest", temperature=0.1)
    print(response)

    

