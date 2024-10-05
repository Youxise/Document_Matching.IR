# Check query validity
def isValidQuery(query_words):
    if query_words[0] in ['and','or']:   # AND/OR cannot be at the beginning: false
        return False
    for i in range(len(query_words)):
        # if the current word is AND/OR
        if query_words[i] in ['and','or']:
            if i == len(query_words)-1:  # if it's the last one: false
                return False
            elif query_words[i+1] in ['and','or']: # if the next one is AND/OR: false
                return False
        # if the current word is NOT
        if query_words[i] == 'not':
            if i == len(query_words)-1:  # if it's the last one: false
                return False
            elif query_words[i+1] in ['and','or','not']: # if the next one is AND/OR/NOT: false
                return False
        # if the current word is a term
        if query_words[i] not in ['and','or','not']:
            if i == len(query_words)-1:  # if it's the last one: true
                return True
            elif query_words[i+1] not in ['and','or']: # if the next one is not AND/OR: false
                return False
    return True

# Apply Boolean Model
def Boolean(descriptor, query):
    liste = {}
    if isValidQuery(query): # valid query
        for doc in descriptor: # iterating through docs
            current_operator = "or"
            result = False
            negate = False # not operator
            for term in query: # iterating through query terms
                if term in ["and", "or"]:
                    current_operator = term
                    negate = False
                elif term == "not":
                    negate = True
                else: # term
                    if negate:
                        term_doc = term not in descriptor[doc].keys() 
                    else:
                        term_doc = term in descriptor[doc].keys()
                    # calculating result of the current operation
                    if current_operator == "and":
                        result = result and term_doc
                    elif current_operator == "or":
                        result = result or term_doc
                    negate = False
            if str(result) == "False":
                continue
            liste[int(doc)+1] = result
            
        # displaying relevant docs
        if liste == {}:
            return "No relevant docs.", None
        result_txt = "Doc \t Relevance\n"
        for key, value in liste.items():
            result_txt += f"{key} \t YES\n"
    else:
        result_txt = "Error: Unvalid query."
    return result_txt, liste