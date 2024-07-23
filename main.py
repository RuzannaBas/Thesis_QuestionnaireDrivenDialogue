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

# Filename
file = 'vragenlijst.txt'

# Read the questions and answers
questions, answers = read_questionnaire(file)

# Set system prompt
chat_log = [{"role": "system", "content": "Je bent Ted. Je reageert op de antwoorden van een vragenlijst die de gebruiker geeft. Je maakt vriendelijk een praatje met de gebruiker tussen vragen door en geeft geen suggesties voor de volgende vraag. Er zijn in totaal 6 vragen, geef geen afrondende opmerking totdat alle 6 vragen zijn beantwoord."}]

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
        assistant_response = response.choices[0].message.content
        cleaned_response = remove_questions(assistant_response)
        print("Ted:", cleaned_response.strip("\n").strip())
        chat_log.append({"role": "assistant", "content": cleaned_response})

# End of the questionnaire after 6 questions
print("Ted: Bedankt voor het beantwoorden van de vragen. Heb je verder nog iets te bespreken?")