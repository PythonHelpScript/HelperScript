import os
import re
import random
import string

print(os.getcwd())
os.chdir("/****/****/")
print(os.getcwd())

def get_questions():

    question_data = get_questions_data()
    questions = []

    index = -1
    for line in question_data:
        first_line_regex = re.compile("Question")
        if first_line_regex.search(line):
            index += 1
            questions.append(line)
        else:
            questions[index] += line

    print("{} questions".format(len(questions)))
    
    return questions


def get_questions_data():
    with open('Q++++.txt', mode='r', encoding='utf-8') as question_file:
        question_data = question_file.readlines()
    return question_data


def get_answers():
    with open('A++++.txt', mode='r', encoding='utf-8') as answer_file:
        raw_answers = answer_file.readlines()
    
    answers = []
    clean_answer_regex = re.compile("\\n")
    for raw_answer in raw_answers:
        answer = clean_answer_regex.sub("", raw_answer)
        answers.append(answer)

    print("{} answers".format(len(answers)))

    return answers


def get_possible_answers(question):
    answer_choice_regex = re.compile("[A-Z]\.")
    resulting_choices = answer_choice_regex.findall(question)

    choices = []
    remove_period_regex = re.compile("\.")
    for choice in resulting_choices:
        choices.append(remove_period_regex.sub("", choice))       

    return choices


def get_explanations():
    with open('E++++.txt', mode='r', encoding='utf-8') as explanation_file:
        raw_explanations = explanation_file.readlines()

    explanations = []

    index = -1
    for line in raw_explanations:
        first_line_regex = re.compile("Explanation")
        if first_line_regex.search(line):
            index += 1
            explanations.append(line)
        else:
            explanations[index] += line

    print("{} explanations".format(len(explanations)))

    return explanations


def save_incorrect_answers(question, answer, explanation):
    
    with open('mq.txt', mode='a', encoding='utf-8') as question_file:
        question_file.write(question)
        
    with open('ma.txt', mode='a', encoding='utf-8') as answer_file:
        answer_file.write(answer)
        answer_file.write("\n")

    with open('mqa.txt', mode='a', encoding='utf-8') as qa_file:
        qa_file.write(question)
        qa_file.write("Answer: {}".format(answer))
        qa_file.write("\n\n") 
        qa_file.write(explanation)
        qa_file.write("\n\n") 


def find_missing(questions, explanations):

    check = []

    qs_to_save = []
    ex_to_save = []

    no_newline_regex = re.compile("\n")
    for question in questions:
        qs_to_save.append(no_newline_regex.sub("", question))

    for explanation in explanations:
        ex_to_save.append(no_newline_regex.sub("", explanation))

    with open('check_questions.txt', mode='a', encoding='utf-8') as question_file:
        for line in qs_to_save:
            question_file.write(line)
            question_file.write("\n")
        
    with open('check_explanations.txt', mode='a', encoding='utf-8') as explanation_file:
        for line in ex_to_save:
            explanation_file.write(line)
            explanation_file.write("\n")

    question_regex = re.compile("QUESTION \d+?")
    for i in range(0,len(questions)):
        q_result = question_regex.search(questions[i]).group()
        e_result = question_regex.search(explanations[i]).group()
        if q_result == e_result:
            check.append("QUESTION {} OK".format(i+1))
        else:
            check.append("ERROR")
            print("Error at location {}".format(i+1))

    print("x")

def start():

    questions = get_questions()
    answers = get_answers()
    explanations = get_explanations()

    print("{} questions".format(len(questions)))
    print("{} answers".format(len(answers)))
    print("{} explanations".format(len(explanations)))

    correct_answers = 0
    incorrect_answers = 0

    while True:
        print("")
        try:
            number_of_questions = int(input("How many questions will you do? (Maximum is {}): ".format(len(questions))))
            break
        except:
            print("That's not a number.")

    print("\n")
    question_number_list = range(1,(len(questions) + 1))
    randomized_question_numbers = random.sample(question_number_list, number_of_questions)

    for question_number in range(1,(number_of_questions + 1)):

        question_index = randomized_question_numbers[question_number - 1]

        question = questions[question_index - 1]
        answer = answers[question_index - 1]
        explanation = explanations[question_index - 1]

        possible_answers = get_possible_answers(question)

        regex_range = "["
        for possible_answer in possible_answers:
            regex_range += possible_answer.lower() + possible_answer.upper()
        regex_range += "]+"
        answer_check_regex = re.compile(regex_range) #"[A-Za-z]+")

        print("Question {} of {}".format(question_number, number_of_questions))
        print(question)

        while True:
            
            chosen_answer = input("Enter your answer: ")

            if answer_check_regex.search(chosen_answer):
                break
            else:
               print("Please enter one (or more) of the possible choices")


        if chosen_answer.upper() == answer:
            correct_answers += 1
            print("")
            print("Correct")
            print("")
        else:
            incorrect_answers += 1
            print("")
            print("Incorrect")
            print("The correct answer is {}".format(answer))
            print("")
            print(explanation)
            print("")
            save_incorrect_answers(question, answer, explanation)

    print("You got {} answers right and {} answers wrong.".format(correct_answers, incorrect_answers))
    print("")

start()
