import nltk
from nltk import word_tokenize, pos_tag

nltk.download('punkt_tab', quiet=True)
nltk.download('averaged_perceptron_tagger_eng', quiet=True)
"""
input: question, answer
output: statement
"""
class Statement:
    def __init__(self):
        return
    
    def entity_qa_state(self,question, answer):
        # for entity questions
        # Tokenize the question and perform part-of-speech tagging
        tokens = word_tokenize(question)
        tags = pos_tag(tokens)

        # Identify the WH-word (What, Where)
        wh_word = None
        for i in range(len(tags)):
            word = tags[i][0]
            tag = tags[i][1]
            if tag in ('WP', 'WRB', 'WDT', 'JJ'):  # WH-words tags
                wh_word = word
                if i+1 <= len(tags) and tags[i+1][1]=='NN':
                    wh_word = wh_word + ' ' + tags[i+1][0]
                break
            
        
        if wh_word:
            # Replace WH-word with the answer

            statement = question.replace(wh_word, str(answer))
            statement = statement.replace('?', '.')

            return statement

        # else, add answer to question
        return f"{question} {answer}".strip()

    def construct_statement(self,question_type, question, answer):
        # for entity question, combine answer and question
        if question_type == "entity":
            return self.entity_qa_state(question, answer)
        # else, no need to change
        return question





if __name__ == "__main__":
    qa_state = Statement()

    # test001
    question = "Who is the director of Pulp Fiction?"
    answer = "Quentin Tarantino"
    question_type = "entity"
    state = qa_state.construct_statement(question_type, question, answer)
    print(state)

    # test002
    question = "Which country has the most population in the world?"
    answer = "China"
    question_type = "entity"
    state = qa_state.construct_statement(question_type, question, answer)
    print(state)