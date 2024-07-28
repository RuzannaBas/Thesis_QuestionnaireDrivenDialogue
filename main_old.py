import openai
import textwrap

# Set API KEY for openAI
with open(r"C:\Users\rsbag\Documents\Universiteit\Data Science & AI\Year 3\Scriptie\API_KEY.txt", "r") as file:
    API_KEY = file.read()
openai.api_key = API_KEY

def read_questionnaire(file):
    with open(file, 'r', encoding='utf-8') as file:
        content = file.read().strip()
    
    # Divide the content into sections separated by two new lines.
    blocks = content.split('\n\n')
    
    questions = []
    answers = []

    for block in blocks:
        lines = block.split('\n')
        question = lines[0].strip()
        answer_options = [line.strip() for line in lines[1:]]
        questions.append(question)
        answers.append(answer_options)
    
    return questions, answers

def remove_questions(text):
    """Remove sentences that are questions."""
    sentences = text.split('.')
    non_question_sentences = [s for s in sentences if not s.strip().endswith('?')]
    return '. '.join(non_question_sentences).strip()

def generate_small_talk(previous_answer, chat_log, next_question):
    """Generate small talk based on the previous answer and guide the conversation towards the next question."""
    
    # Define a flag to determine when to proceed to the next question
    proceed_to_next_question = False

    while not proceed_to_next_question:
        # Generate small talk or follow-up question
        response = openai.chat.completions.create(  
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Je bent een chatbot die small talk genereert op basis van de reacties van de gebruiker. Probeer de conversatie op een natuurlijke manier naar de volgende vraag te leiden."},
                {"role": "user", "content": f"Genereer een stukje small talk of een vervolgvraag over het volgende antwoord: {previous_answer}"}
            ]
        )
        small_talk = response.choices[0].message.content

        # Print and log the small talk
        cleaned_response = textwrap.fill(f"{small_talk}", width=120)
        print("Ted:", cleaned_response.strip("\n").strip())
        chat_log.append({"role": "assistant", "content": cleaned_response})

        # Get user response
        user_message = input()
        chat_log.append({"role": "user", "content": user_message})

        # Check if the small talk has reached a point where we can move to the next question
        response_check = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Je bent een chatbot die de conversatie begeleidt. Evalueer de gebruikersreactie en bepaal of het tijd is om door te gaan naar de volgende vraag."},
                {"role": "user", "content": f"Beoordeel de volgende gebruikersreactie en bepaal of het gepast is om naar de volgende vraag te gaan: {next_question}"}
            ]
        )
        evaluation = response_check.choices[0].message.content

        # If the evaluation indicates it's time to proceed, exit the loop
        if "ja" in evaluation.lower() or "yes" in evaluation.lower():
            proceed_to_next_question = True

    return


# Filename
file = 'vragenlijst.txt'

# Read the questions and answers
questions, answers = read_questionnaire(file)

# Set system prompt
chat_log = [{"role": "system", "content": "Je bent Ted. Je reageert op de antwoorden van een vragenlijst die de gebruiker geeft. Je maakt vriendelijk een praatje met de gebruiker tussen vragen door en geeft geen suggesties voor de volgende vraag. Er zijn in totaal zes vragen, geef geen afrondende opmerking totdat alle zes vragen zijn beantwoord."}]

welcome_message = textwrap.fill("Hallo, Ik ben Ted. Ik ga vandaag een vragenlijst met u afnemen om te kijken hoe het gaat met u. Voel u vrij om eerlijk en open te antwoorden. Er zijn geen goede of foute antwoorden; we willen gewoon een zo goed mogelijk beeld krijgen van hoe het met u gaat. Bij elke vraag vraag ik u om een open antwoord te geven zonder dat u zich beperkt voelt door de vooraf gegeven antwoordopties. Laten we beginnen met de eerste vraag.", width=120)
print(welcome_message)
chat_log.append({"role": "assistant", "content": f"{welcome_message}"})

# Loop through the questions and answers
for i, question in enumerate(questions):
    if i == 6:
        break
    # Wrap the question text so it looks neat
    wrapped_question = textwrap.fill(f"Vraag {i+1}: {question}", width=120)
    print(wrapped_question)
    
    for j, answer in enumerate(answers[i]):
        # Wrap the answers
        wrapped_answer = textwrap.fill(f"  {chr(97 + j)}. {answer}", width=90, subsequent_indent='    ')
        print(wrapped_answer)
    print() 
    # Append question and answers to the chat log as an assistant message
    chat_log.append({"role": "assistant", "content": f"{question}\n" + "\n".join(answers[i])})
    user_message = input()
    if user_message.lower() == "klaar":
        break
    else:     
        chat_log.append({"role": "user", "content": user_message})
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=chat_log
        )
        generate_small_talk(user_message, chat_log, questions[i+1])
        # assistant_response = response.choices[0].message.content
        # cleaned_response = textwrap.fill(f"{remove_questions(assistant_response)}", width=120)
        # print("Ted:", cleaned_response.strip("\n").strip())
        # chat_log.append({"role": "assistant", "content": cleaned_response})

# End of the questionnaire after 6 questions
print("Ted: Bedankt voor het beantwoorden van de vragen. Heb je verder nog iets te bespreken?")
