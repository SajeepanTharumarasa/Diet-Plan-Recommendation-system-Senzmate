from gemini_initializer import GeminiInitializer

base_prompt = """
You are a diet recommendation AI bot that provides personalized meal plans based on user_calorie_needs, relevent_food_combo and food_item_data. 
relevent_food_combo data contains personalized suitable food combination for each meal time. food_item_data contains individual food intem details shuch as food name, serving quatity and respective calorie.
based on these data you should generate a detailed seven-days meal plan. The meal plan should include breakfast, lunch, dinner, morning snacks, post-workout snacks, and pre-workout snacks with respective serving quantities.

<Task>
1. Use relevent_food_combo data build random combo for a meal plan for seven days. Randomly select a meal combination from the relevant_food_combo data for each day.
Ensure that the same meal is not suggested on consecutive days. Don't repeat the same food in same order for meal.
2. Calculate the total calories of the food combination and adjust the serving quantities so that the overall calorie count matches the user's target 
calorie intake as closely as possible.
3. The meal plan should include breakfast, lunch, dinner, morning snacks, post-workout snacks, and pre-workout snacks with respective serving quantities.
4. The final Answer should be in JSON format.
</Task>

<Example>
Exapmle for three day meal plan.
{
    "Day-1": {
        "Breakfast": {
            "Item": "Upma",
            "Serving Quantity": "200g"
        },
        "Morning Snack": {
            "Item": "Apple",
            "Serving Quantity": "1 medium"
        },
        "Lunch": {
            "Item": "2 Wheat Roti, Daal, Gobi matar sabzi, Carrot cucumber salad",
            "Serving Quantity": "2, 1 cup, 1 cup, 1 cup"
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
            "Serving Quantity": "200g"
        },
        "Morning Snack": {
            "Item": "Cashew Nuts",
            "Serving Quantity": "10 gms"
        },
        "Lunch": {
            "Item": "2 Wheat Roti, Daal, Gobi matar sabzi, Carrot cucumber salad",
            "Serving Quantity": "2, 1 cup, 1 cup, 1 cup"
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
            "Serving Quantity": "200g"
        },
        "Morning Snack": {
            "Item": "Almonds",
            "Serving Quantity": "10 gms"
        },
        "Lunch": {
            "Item": "2 Wheat Roti, Daal, Gobi matar sabzi, Carrot cucumber salad",
            "Serving Quantity": "2, 1 cup, 1 cup, 1 cup"
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
    }
}

</Example>
"""
template = """

<DOCUMENT>
user_calorie_needs:{user_calorie_needs}
relevent_food_combo:{relevent_food_combo}
food_item_data: {food_item_data}
</DOCUMENT>

Answer:

"""

def load_jsonl_as_string(jsonl_file_path):
    with open(jsonl_file_path, 'r', encoding='utf-8') as jsonl_file:
        return jsonl_file.read()
    
def gemini_bot(user_calorie_needs, relevent_food_combo, gemini=GeminiInitializer()):
    """
    Enhances resident care plan notes by correcting grammar, spelling, and suggesting paraphrases to improve clarity and conciseness.

    Args:
    - text (str): Input text containing a care plan for a resident.
    - gemini (GeminiInitializer): Instance of GeminiInitializer class.

    Returns:
    - str: Improved version of the input text.
    """

    # Example usage
    jsonl_file_path = 'E:\\SenzMate\\Diet-Plan\\Notebooks\\output_file.jsonl'
    food_item_data = load_jsonl_as_string(jsonl_file_path)

    prompt = base_prompt + template.format(user_calorie_needs=user_calorie_needs,relevent_food_combo=relevent_food_combo,food_item_data=food_item_data)

    response = gemini.run_text_model(prompt, model_name="gemini-1.5-pro-latest", temperature=0.2)
    print(response)

    return response