import openai
import textwrap

def generate_small_talk(previous_answer, chat_log, next_question):
    """Generate small talk based on the previous answer and guide the conversation towards the next question."""
    proceed_to_next_question = False
    small_talk_counter = 0
    max_small_talk_rounds = 1
    reaction_basis = previous_answer
    
    chat_log.append({"role": "user", "content": f"Genereer een stukje small talk over het volgende antwoord: {reaction_basis}"})
    while not proceed_to_next_question:
        # Generate small talk
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=chat_log
        )
        small_talk = response.choices[0].message.content
        cleaned_response = textwrap.fill(small_talk, width=120)
        print()
        print("Ted:", cleaned_response.strip("\n").strip())
        print()
        chat_log.append({"role": "assistant", "content": cleaned_response})
        
        if "volgende vraag" in cleaned_response:
            break
        # User input
        user_message = input()
        reaction_basis = user_message
        chat_log.append({"role": "user", "content": user_message})
        
        small_talk_counter += 1
        
        # Check if it's time to move to the next question
        if small_talk_counter > max_small_talk_rounds:
            proceed_to_next_question = True
            chat_log.append({"role": "user", "content": f"Geef een afsluitende reactie op {user_message} en zeg dat je door gaat naar de volgende vraag maar stel zelf geen vraag"})
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=chat_log
            )
            final_response = response.choices[0].message.content
            cleaned_final_response = textwrap.fill(final_response, width=120)
            print("Ted:", cleaned_final_response.strip("\n").strip())
            print()
            chat_log.append({"role": "assistant", "content": cleaned_final_response})
            
