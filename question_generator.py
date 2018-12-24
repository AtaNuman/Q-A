#!/usr/bin/env python3
# coding: utf-8
import spacy
import language_check

#Standard constants across the language
modal_verbs = ["can", "could", "may", "might", "must", "shall", "should", "will", "would"]
to_be_conjugations = ["are", "is", "was", "were"]
to_have_conjugations = ["has", "have", "had", "\'ve"]
location_words = ["here","there","everywhere"]
cause_words = ["because","due to"]

#Other constants for the program
INVALID_IDX = -999

def get_root(tokens):
    for token in tokens:
        if 'ROOT' == token.dep_:
            return token
    return None

def get_main_verb(tokens):
    for token in tokens:
        if 'VERB' == token.pos_:
            return token
    return None

def make_why_question(doc):
    questions = []
    doc = get_why_clause(doc)
    if None == doc:
        return questions 
    remain_pos = INVALID_IDX
    text   = [token.text for token in doc]
    doc = nlp(' '.join(text))
    text   = [token.text for token in doc]
    tokens = [token for token in doc]
    for token in tokens:
        print (token,token.dep_) 
    for (idx,token) in enumerate(tokens):
        if 'ROOT' == token.dep_:
            remain_pos = idx + 1
            break 
    question = "Why "
    subject = ""
    det = " "
    subj_num = ""
    tense = ""
    adjs = ""
    needsdo = True
    for word in text:
        if word in to_be_conjugations:
            question += word + " "
            needsdo = False
            break
    root = get_root(tokens)
    if root:
        for child in root.children:
            if 'nsubj' in child.dep_:
                #print("got subject")
                subj_num = subj_get_num(child)            
                subject = child.text
                subj_args = [c.text for c in child.children]
                adjs += get_adjs([c for c in child.children])
                print ("ADJECTIVES")
                print (adjs)
                print ("ADJECTIVES")
                if subj_has_det(subj_args):
                    #print ("got Determiner")
                    det = " the "
        if (needsdo):
            #print ("needs do")
            tense = verb_get_tense(root)
            #print (type(tense)) 
            question += add_do(subj_num,tense,root)
            question += det + adjs + subject + " " +root.lemma_
            print ("~~~~~~~~~~~~~~~`")
            print ("root: "+root.text)
            print ("subject: "+subject)
            print ("question: "+question)
            print ("~~~~~~~~~~~~~~~`")
        else:
            #              is        the     cat
            #print ("is a 'to be' verb")
            question += det + subject + " " + root.text
        #Now just append the remaining part of the sentence.
        if INVALID_IDX != remain_pos:
            #print (remain_pos)
            question += ' '
            question += ' '.join(text[remain_pos:])
        question += " ?"
    questions.append(question)
    print ("\n\n")
    #print (question)
    return questions    
        
         
def get_why_clause(doc):
    pos = can_make_why_question(doc)
    if (INVALID_IDX == pos):
        return None
    else:
        return doc[:pos]

def can_make_why_question(doc):
    l = len(doc)
    for index,token in enumerate(doc):
        if "because" == token.text:
            return index
        if "due" == token.text and index < l-1 and "to" == doc[index+1]:
            return index - 1
    return INVALID_IDX
            

#"to have" questions
def to_have(tokens):
    for have_form in to_have_conjugations:
        if have_form in tokens:
            question = "Is it that " + " ".join(tokens)
            question.rstrip(". ")
            question += " ?"
            return question

#Form a question by:
#   step 1) Removing the auxiliary verb from the sentence (unless the verb is "to be")
#   step 2) Adding the auxiliary verb to the beginning of the sentence
#   step 3) If the auxiliary verb is form of "to be", add "it that" after the verb
def auxiliary_yes_no(aux_verbs,tokens):
    questions = []
    for aux in aux_verbs:
        if aux in tokens:
            # step 1
            q_phrase = [token for token in tokens if token != aux or aux in to_be_conjugations]
            question = ' '.join(q_phrase)
            #print(question)
            q = question.rstrip(" ")
            q = question.rstrip(".")
            # step 2
            question = aux.capitalize()
            # step 3
            if aux in to_be_conjugations:
                question += " " + "it that" 
            question += " " + q + "?"
            questions.append(question)
    return questions

#Create a yes/no question
#We need auxiliary verbs for forming yes/no questions
#"to be", "to have" and modal verbs are the broad classes
def yes_no_question(doc):
    tokens = [token.text for token in doc]
    question = ""
    questions = []
    questions1 = auxiliary_yes_no(modal_verbs,tokens)
    questions2 = auxiliary_yes_no(to_be_conjugations,tokens)
    questions = questions1 + questions2
    to_have_qn = to_have(tokens)
    if to_have_qn:
        questions.append(to_have_qn)
    #questions = delNeg(questions)
    return questions

#If the token is a conjugation of "to be", we don't need a form of "to do"
#For all other verbs, it is required for "Where" and "Why" questions
def needs_do(token):
    #print (token.lemma_)
    if token.pos_ == "VERB" and token.lemma_ != "be":
        return True
    return False

# forms do(es) + (the) + subject and return the formed string
#Test cases:
#The cat is under the table
#The cat jumped out of the window (yikes!)
#The cats are under the table
#The cats were under the table
#The cats live here
#The cats went to the kitchen 
def add_do(subj_num,tense,root_token):
    do_phrase = ""
    if (tense == "past"):
        do_phrase += "did"
    elif (tense == "present"):
        if (subj_num == "singular"):
            do_phrase += "does"
        elif (subj_num == "plural"):
            do_phrase += "do"
    return do_phrase
#returns singular or plural
def subj_get_num(token):
    subj_num = ""
    if token.tag_ == 'NNS' or token.tag_ == 'NNPS':
        subj_num = "plural"
    elif token.tag_ == 'NN' or token.tag_ == 'NNP':
        subj_num = "singular"
    return subj_num 

def verb_get_tense(token):
    tense = ""
    if (token.pos_ == "VERB"):
        if token.tag_ in ["VBD","VBN"]:
            tense = "past"
        elif token.tag_ in ["VBG","VB","VBP","VBZ"]:
            tense = "present"
    return tense

def subj_has_det(subj_args):
    if "a" in subj_args or "A" in subj_args:
        return True
    if "the" in subj_args or "The" in subj_args:
        return True
    return False

def get_adjs(subj_args):
    adjs = ""
    dets = ["a","A","the","The"]
    for det in subj_args:
        subj_args.remove(det)
    for adjective in subj_args:
        if adjective.text != ',':
            adjs += adjective.text+","
    adjs = adjs.rstrip(",")
    if adjs != "":
        adjs += " "
    return adjs

def has_location_word(words):
    for loc in location_words:
        if loc in map(str.lower,words):
            return True
    return False


def where_question(doc,dep_parse):
    questions = []
    question  = ""
    subject = ""
    det = " "
    subj_num = ""
    tense = ""
    adjs = ""
    #print (dep_parse)
    words = [token.text for token in doc]
    if 'prep' in dep_parse or has_location_word(words):
        #print ("PREP present")
        question = "Where "
        for token in doc:
            if token.dep_ == 'ROOT':
                #print ("ROOT found")
                #print ("Children: ")
                #print ([child for child in token.children])
                for child in token.children:
                    if child.dep_ == 'nsubj':
                        #print("got subject")
                        subj_num = subj_get_num(child)            
                        subject = child.text
                        subj_args = [c.text for c in child.children]
                        adjs += get_adjs([c for c in child.children])
                        if subj_has_det(subj_args):
                            #print ("got Determiner")
                            det = " the "
                if (needs_do(token)):
                    #print ("needs do")
                    tense = verb_get_tense(token)
                    #print (type(tense)) 
                    question += add_do(subj_num,tense,token)
                    question += det + adjs + subject + " " +token.lemma_
                else:
                    #              is        the     cat
                    #print ("is a 'to be' verb")
                    question += token.text + det + subject
                question += " ?"
    #print ("Question formed: " + question)
    questions.append(question)
    return questions
import nltk
#create a question for a given sentence 
def create_questions(doc):
    nlp = spacy.load('en_core_web_sm')
    with open("project_data/set3_a4.txt", encoding="utf8") as f:
        wiki_text = f.read()
        sentences = nltk.sent_tokenize(wiki_text)

        # create many questions
        # nlp = spacy.load('en_core_web_sm')
        # questions = []
    for sentence in sentences:
        doc = nlp(sentence)
        print(yes_no_question(doc))


    """
    questions = make_why_question(doc)
    #Form yes/no questions
    #questions += yes_no_question(doc)
    """
    dep_parse = []
    for token in doc: 
        dep_parse.append(token.dep_)
    #questions += where_question(doc,dep_parse)
    count = dep_parse.count('nsubj')
    for x in range(count):
        question = ""
        countN = 0
        for token in doc:
            #if the current token is the subject, form 'wh' type questions
            #print (token.tag_)
            if (token.dep_ == 'nsubj'):
                if(countN != x):
                    if question_type(token) != None:
                        question += question_type(token) + " "
                    else:
                        question = "Fake question"
                else: 
                   question += token.text + " "
                countN += 1
            else:
                question += token.text + " "
        question = question.rstrip(". ")
        question += "?"
        questions.append(question)
    print (questions)
    print ("\n\n\n\n")
    """
    return questions
    """

def delNeg(questions):
    newQ = []
    tool = language_check.LanguageTool('en-US')
    for question in questions:
        matches = tool.check(question)
        if(len(matches) != 0):
            questions.remove(question)
            continue
        if('not ' in question):
            ind = question.find('not', 0,len(question))
            newQ.append(question[:ind]+question[ind+4:])
    questions += newQ
    return(questions)

def question_type(token):
    if (token.tag_ == 'NNP'):
        return "Who"
    elif (token.tag_ == 'NN'):
        return "What"


nlp = spacy.load('en_core_web_sm')

#doc = nlp(u"Elmo lives in his own section of Sesame Street called Elmo's world")
#sentences = ["The cat is under the table","The cat jumped out of the window","The cats are under the table","The cats were under the table","The cats went to the kitchen"]
#sentences += ["The poor,smelly cat ran towards Phoebe","The cat lives here","The cats live 20 kilometers from here"]
#for sent in sentences:
#    doc = nlp(sent)
#    print (doc)
#    questions = create_questions(doc)
    #print (questions)

#doc = nlp(u"The cats live here")
#For reference
#for token in doc:
#    print(token.text, token.dep_, token.head.text,[child for child in token.children])


# text = "Could Fred not believe that Sally was the culprit  ?"
# tool = language_check.LanguageTool('en-US')
# matches = tool.check(text)
# print(matches)


#Test cases for where questions:
#The cat is under the table
#The cat jumped out of the window (yikes!)
#The cats are under the table
#The cats were under the table
#The cats live here
#The cats went to the kitchen (to ask mommy for food, not make dinner, obviously!)
