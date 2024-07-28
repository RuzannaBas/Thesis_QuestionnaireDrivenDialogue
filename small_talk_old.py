import openai
import textwrap

def generate_small_talk(previous_answer, chat_log, next_question):
    """Generate small talk based on the previous answer and guide the conversation towards the next question."""
    
    proceed_to_next_question = False
    small_talk_counter = 0
    max_small_talk_rounds = 3  # Limit the number of small talk rounds

    while not proceed_to_next_question and small_talk_counter < max_small_talk_rounds:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"Je bent een chatbot die small talk genereert op basis van de reacties van de gebruiker. "},
                {"role": "user", "content": f"Genereer een stukje small talk over het volgende antwoord: {previous_answer}"}
            ]
        )
        small_talk = response.choices[0].message.content
        cleaned_response = textwrap.fill(small_talk, width=120)
        print("Ted:", cleaned_response.strip("\n").strip())
        chat_log.append({"role": "assistant", "content": cleaned_response})

        user_message = input()
        chat_log.append({"role": "user", "content": user_message})

        response_check = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Je bent een chatbot die de conversatie begeleidt. Evalueer de gebruikersreactie en bepaal of het tijd is om door te gaan naar de volgende vraag."},
                {"role": "user", "content": f"Beoordeel de volgende gebruikersreactie en bepaal of het gepast is om naar de volgende vraag te gaan: {next_question}"}
            ]
        )
        evaluation = response_check.choices[0].message.content
        if "ja" in evaluation.lower() or "yes" in evaluation.lower():
            proceed_to_next_question = True

        small_talk_counter += 1

    if not proceed_to_next_question:
        # Forcing to proceed after max small talk rounds
        print("Ted: Laten we verder gaan met de volgende vraag.")
        chat_log.append({"role": "assistant", "content": "Laten we verder gaan met de volgende vraag."})

    return
