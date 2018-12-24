import spacy

INVALID_IDX = -999

def aux_exists(doc):
    for token in doc:
        if "aux" in token.dep_:
            return token
    return None


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
def add_do(subj_num,tense):
    do_phrase = ""
    if (tense == "past"):
        do_phrase = "did"
    elif (tense == "present"):
        if (subj_num == "singular"):
            do_phrase = "does"
        elif (subj_num == "plural"):
            do_phrase = "do"
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
def can_make_why_question(doc):
    l = len(doc)
    for index,token in enumerate(doc):
        if "because" == token.text:
            return index
        if "due" == token.text and index < l-1 and "to" == doc[index+1].text:
            return index - 1
    return INVALID_IDX

def create_why_question(doc):
    #print ("received why clause: "+" ".join([token.text for token in doc]))
    question = "Why "
    aux = aux_exists(doc)
    root  = [token for token in doc if token.head == token][0]
    #print (root.text,root.dep_)
    subject = list(root.lefts)[0]
    subj_num = ""
    if (None != aux):
        #do something
        question += aux.text + " " 
    else:
        if needs_do(root):
            if (len(list(subject.subtree)) > 1):
                subj_num = "plural"
            elif (len(list(subject.subtree)) == 1):
                subj_num = subj_get_num(subject)
            else:
                subj_num = "singular"
            tense = verb_get_tense(root)
            do_word = add_do(subj_num,tense)
            question += do_word + " "
        else:
            question += root.text + " "
    subj_words =  " ".join([subj_word.text for subj_word in subject.subtree]) 
    if not('NNP' == list(subject.subtree)[0].pos_ or 'NNPS' == list(subject.subtree)[0].pos_):
        subj_words = subj_words[0].lower() + subj_words[1:]
    question += subj_words + " "
    if (None != aux):
        question += root.text + " "
    else:
        if (needs_do(root)):
            #print (root.text+ " needs do")
            question += root.lemma_ + " "
    root_pos = INVALID_IDX
    root_pos = list(root.subtree).index(root)
    if (INVALID_IDX != root_pos):
        because_idx = can_make_why_question(list(root.subtree))
        subtree = list(root.subtree)[root_pos+1:because_idx]
        #print ("SUBTREE: ")
        #print (subtree)
        question += " ".join([elem.text for elem in subtree])
    question += "?"
    #print (question)
    return question
    """        
    root = [token for token in doc if token.head == token][0]
    print (root.text)
    for descendant in root.subtree:
        print (descendant.text,descendant.dep_)
    print ("##")
    for descendant in root.rights:
        print (descendant.text,descendant.dep_)
        for child in descendant.children:
            print ("==>",child.text,child.dep_,[e.text for e in child.subtree])
    subject = list(root.lefts)[0]
    for descendant in subject.subtree:
        assert subject is descendant or subject.is_ancestor(descendant)
        print(descendant.text, descendant.dep_, descendant.n_lefts,
              descendant.n_rights,
              [ancestor.text for ancestor in descendant.ancestors])f
    """
nlp = spacy.load('en_core_web_sm')
#doc = nlp(u"Credit and mortgage account holders must submit their requests")
#question = create_why_question(doc)
#print (question)
#doc = nlp(u"English and German are classified as Germanic Languages")
#question = create_why_question(doc)
#print (question)

