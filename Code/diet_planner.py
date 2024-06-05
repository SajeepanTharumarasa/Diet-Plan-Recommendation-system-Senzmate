import json

from gemini_initializer import GeminiInitializer

template = '''
You are an expert AI assistant designed to enhance resident care plans.

Input Text: {input_text}
Answer:
'''

def diet_planner(text, gemini=GeminiInitializer()):
    """
    Enhances resident care plan notes by correcting grammar, spelling, and suggesting paraphrases to improve clarity and conciseness.

    Args:
    - text (str): Input text containing a care plan for a resident.
    - gemini (GeminiInitializer): Instance of GeminiInitializer class.

    Returns:
    - str: Improved version of the input text.
    """
    print(text)
    prompt = template.format(input_text=text)
    print(prompt)
    response = gemini.run_text_model(prompt, model_name="gemini-1.5-pro-latest", temperature=0.2)
    print(response)

    return response

