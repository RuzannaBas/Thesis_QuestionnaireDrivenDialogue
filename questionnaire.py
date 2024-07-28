# questionnaire.py
def read_questionnaire(file):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    
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
