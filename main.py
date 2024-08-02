# Questionnaire-driven Dialogue: Utilizing Large Language Models for Hallucination-free Conversational AI in Elderly Well-being Monitoring
# Ruzanna Baghdasaryan -- s3068021 -- r.s.baghdasaryan@umail.leidenuniv.nl
# Bacherlor Thesis -- BSc Data Science & Artificial Intelligence 2024

import textwrap
import openai
import re
from config import API_KEY
from datetime import date
from questionnaire import read_questionnaire
from small_talk import generate_small_talk
from evaluate_answer import evaluate_answer
from save_results import save_result

def main():
    # Filename of questionnaire
    file = 'vragenlijst.txt'

    # Read the questions and answers
    questions, answers = read_questionnaire(file)

    results = []
    # Set system prompt
    chat_log = [{"role": "system", "content": "Je bent Ted, een vriendelijke chatbot die reageert op de antwoorden van een vragenlijst die de gebruiker geeft. Je maakt vriendelijk een praatje met de gebruiker tussen vragen door."}]

    welcome_message = textwrap.fill("Hallo, Ik ben Ted. Ik ga vandaag een vragenlijst met u afnemen om te kijken hoe het gaat met u. Voel u vrij om eerlijk en open te antwoorden. Er zijn geen goede of foute antwoorden; we willen gewoon een zo goed mogelijk beeld krijgen van hoe het met u gaat. Bij elke vraag vraag ik u om een open antwoord te geven zonder dat u zich beperkt voelt door de vooraf gegeven antwoordopties. Laten we beginnen met de eerste vraag.", width=120)
    print(welcome_message)
    chat_log.append({"role": "assistant", "content": welcome_message})

    # Loop through the questions and answers
    for i, question in enumerate(questions):
        choices = []
        wrapped_question = textwrap.fill(f"Vraag {i+1}: {question}", width=120)
        print(wrapped_question)
        for j, answer in enumerate(answers[i]):
            wrapped_answer = textwrap.fill(f"  {chr(97 + j)}. {answer}", width=90, subsequent_indent='    ')
            print(wrapped_answer)
            choices.append(answer)
        print() 
        chat_log.append({"role": "assistant", "content": f"{question}\n" + "\n".join(answers[i])})
        user_message = input()
        print() 
        if i < 5:
            evaluate_answer(user_message, question, choices, results)
        if i == 5:
            score = 0
            numbers = re.findall(r'\d+', user_message)
            if numbers:
                score = int(numbers[0])
            results.append(score)
        if user_message.lower() == "klaar":
            break
        else:     
            chat_log.append({"role": "user", "content": user_message})
            if i < 5:
                generate_small_talk(user_message, chat_log)
            else: 
                # End of the questionnaire after 6 questions
                chat_log.append({"role": "user", "content": f"Geef een afsluitende reactie op {user_message} sluit het gesprek af."})
                response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=chat_log
                )
                final_response = response.choices[0].message.content
                print(final_response)
                break

    save_result(results, chat_log)

if __name__ == "__main__":
    main()
