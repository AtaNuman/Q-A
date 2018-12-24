def create_what_question(sentence):
    root = list(filter(lambda token: 'ROOT' in token.dep_, sentence))[0]
    object = list(filter(lambda token: 'dobj' in token.dep_ and token.pos_ != "PRON", root.children))
    
    if root and object:
        fullObj = " ".join(list(map(lambda t: t.text, object[0].subtree)))

        # don't create a question if the parses are unnecessarily long
        too_long =  100
        if (len(fullObj) > too_long):
            return None

        # "what" questions pretty much always work
        q1 = "What " + root.text + " " + fullObj.strip() +"?"
        # print(q1)
        return q1