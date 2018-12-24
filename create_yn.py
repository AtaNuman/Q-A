def create_yn_question(sentence):
    root = list(filter(lambda token: 'ROOT' in token.dep_, sentence))[0]
    subject = list(filter(lambda token: 'nsubj' in token.dep_, root.children))
    object = list(filter(lambda token: 'dobj' in token.dep_ and token.pos_ != "PRON", root.children))
    
    if root and subject and object:
        fullSubj = " ".join(list(map(lambda t: t.text, subject[0].subtree)))
        fullObj = " ".join(list(map(lambda t: t.text, object[0].subtree)))

        # don't create a question if the parses are unnecessarily long
        too_long =  100
        if (len(fullObj) > too_long or
            len(fullSubj) > too_long):
            return None

        # "did" questions only make sense when the subject is not a pronoun
        if len(list(filter(lambda token: 'PRON' in token.pos_, subject[0].subtree))) == 0: #subject[0].pos_ != "PRON":
            q0 = "Did " + fullSubj + " " + root.lemma_ + " " + fullObj.strip() +"?"
            # print(q0)
            return q0

        return None