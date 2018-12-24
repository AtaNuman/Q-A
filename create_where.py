PREPS = {' at ',' in ', ' from ', ' through ', ' on ', ' to ', ' towards ',}

def create_where_question(sentence):
    #assuming location and preposition
    # print([(token.text, token.dep_, token.head.text,[child for child in token.children]) for token in sentence])
    
    return None
"""
    tagged_s = sentence.ents

    for tag in tagged_s:
        if tag.label_ in ["LOC", "GPE", "FAC"]:
            ind = sentence.find(tag.text)
            substring = sentence[ind-10:ind]
            for prep in preps:
                if(substring.find(prep) != -1):

            

    return None













    # print(sentence)
    # # print([(token.text, token.ent_type_, token.head.text,[child for child in token.children]) for token in sentence])
    
    location = list(filter(lambda ent: ent.label_ in ['LOC', 'GPE', 'FAC'], sentence.ents))[0]
    #print("Location:", location)

    root = list(filter(lambda token: 'ROOT' in token.dep_, sentence))[0]
    #print("Root:", root)

    subject = list(filter(lambda token: 'nsubj' in token.dep_, root.children))
    #print("Subjects:", subject)

    objects = list(filter(lambda token: 'pobj' in token.dep_, root.rights))
    #print("Objects:", objects)

    # print(root, subject, object)
    
    # # if root and subject and object:
    # #     fullObj = " ".join(list(map(lambda t: t.text, object[0].subtree)))

    # #     # don't create a question if the parses are unnecessarily long
    # #     too_long =  100
    # #     if (len(fullObj) > too_long):
    # #         return None

    # #     # "where" questions are iffy
    # #     q2 = "Where did " + subject[0].text + " " + root.text +"?"
    # #     print(q2)
    # #     return q2

import spacy
def test():
    nlp = spacy.load("en_core_web_sm")
    s1 = nlp('As an outspoken opponent of the expansion of slavery in the United States, [I]n his short autobiography written for the 1860 presidential campaign, Lincoln would describe his protest in the Illinois legislature as one that briefly defined his position on the slavery question, and so far as it goes, it was then the same that it is now.')
    s2 = nlp("During his term, he helped preserve the United States by leading the defeat of the secessionist Confederate States of America in the American Civil War.")
    # print([(token.text, token.dep_, token.head.text,[child for child in token.children]) for token in s1])
    #print("running")
    create_where_question(s1)
    create_where_question(s2)

test()
"""