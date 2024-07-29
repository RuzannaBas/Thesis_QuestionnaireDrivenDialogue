# import openai

# def evaluate_answer(user_message, answers):

import openai
def assign_score(choice):
    match choice:
        case 1:
            return 5
        case 2:
            return 4
        case 3:
            return 3
        case 4:
            return 2
        case 5:
            return 1

def evaluate_answer(user_response, question, choices, results):
    """
    Given a user response and a list of choices, this function returns the best matching choice using GPT-3.5 Turbo.
    """
    # Construct the input text for GPT-3.5 Turbo
    input_text = f"User response: {user_response}\nQuestion:{question}\nChoices:\n"
    for i, choice in enumerate(choices, start=1):
        input_text += f"{i}. {choice}\n"
    
    input_text += "\nWelke keuze past het meest bij de gegeven reactie?"

    # Call GPT-3.5 Turbo
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Je bent een assistent die een antwoord verbindt met het meest bijpassende meerkeuze antwoord. Reageer alleen met de letter dat bij het antwoord hoort."},
            {"role": "user", "content": input_text}
        ],
        temperature=1
    )

    # Extract the choice from the response
    result = response.choices[0].message.content.strip()

    # Return the chosen option text
    for i, choice in enumerate(choices, start=1):
        if str(i) in result or choice in result:
            score = assign_score(i)
            results.append(score)


