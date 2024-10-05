import nltk
import math

# Tokenization with Regex & Split
def Tokenization(docs, number):
    terms = []
    stopW = nltk.corpus.stopwords.words('english')
    punctuation = ['.', ',', '!', '?', ':', ';']
    for doc in docs:
        # Tokenization with RegEX
        if number == 1:
            ExpReg = nltk.RegexpTokenizer('(?:[A-Za-z]\.)+|[A-Za-z]+[\-@]\d+(?:\.\d+)?|\d+[A-Za-z]+|\d+(?:[\.\,]\d+)?%?|\w+(?:[\-/]\w+)*')
            terms.append([terme for terme in ExpReg.tokenize(doc) if terme.lower() not in stopW])
        # Tokenization with Split
        else:
            Texte = doc.split()
            terms.append([term for term in Texte if term.lower() not in stopW])
    return terms

# Normalization with Porter & Lancaster
def Normalization(docs, number):
    Lancaster = nltk.LancasterStemmer()
    Porter = nltk.PorterStemmer()
    terms = []
    for doc in docs:
        # Porter
        if number == 1:
                terms.append([Porter.stem(terme) for terme in doc])
        # Lancaster
        else:
                terms.append([Lancaster.stem(terme) for terme in doc])
    return terms

# Calculating frequency for each term
def indexing(docs):
    terms = []
    dicts = {}
    for doc in docs:
        dicts = nltk.FreqDist(doc)
        terms.append(dicts)
    return terms

# Descriptor dictionary (Doc - Term - Frequency)
def Descriptor(docs, n1, n2):
    
    result = indexing(Normalization(Tokenization(docs, n1), n2))
    descriptor = {} 
    # iterating through documents
    for doc_number, doc in enumerate(result):
        doc_tokens = {}
        # iterating through the tokens in the document
        for token, frequency in doc.items():
            doc_tokens[token] = frequency
        # getting a doc descriptor
        descriptor[str(doc_number)] = doc_tokens
    return descriptor

# Inverse dictionary (Term - Doc - Frequency)
def Inverse(docs, n1, n2):
    
    result = indexing(Normalization(Tokenization(docs, n1), n2))
    inverse = {}
    # iterating through documents
    for doc_number, doc in enumerate(result):
        # iterating through the tokens in the document
        for token, frequency in doc.items():
            if token not in inverse:
                inverse[token] = {}  # Create an empty dictionary for the token if it doesn't exist
            freq_doc = {}
            freq_doc[str(doc_number)] = frequency
            inverse[token].update(freq_doc)
    return inverse

# Calculate weights for each document terms
def weightsCompute(desc, inv):
    
    # init variables
    weights = [[] for _ in range(len(desc))]
    j = 0
    for doc in desc:       # iterating through docs
        freqMax = max(desc[doc].values()) # frequence max of a document
        # iterating through terms
        for term in desc[doc]:
            freq = desc[doc][term] # frequence of the term
            # calculating Ndoc
            if term in inv.keys():   
                Ni = len(inv[term])
            else:
                Ni = 0
            # calculating weight
            weights[j].append(round((freq / freqMax) * math.log10((len(desc)/Ni)+1), 4))
        j += 1     
    return weights

# Update Descriptor & Inverse with weights (add)
def update(descriptor, inverse, weights):
    desc = descriptor.copy()
    inv = inverse.copy()
    for doc_number, doc in enumerate(desc):      # iterating through docs
        j = 0
        for term in desc[doc]:   # iterating through terms
            if j == len(desc[doc]):
                break
            freq = desc[doc][term] # frequence of the term
            desc[doc][term] = {str(freq): weights[doc_number][j]}
            inv[term][doc] = {str(freq): weights[doc_number][j]}
            j += 1    
    return desc, inv

# Display a given document number content 
def descriptorSearch(doc, desc, inv):
    doc_adapted = str(int(doc)-1)
    if doc_adapted in desc.keys():
        j = 0
        result_txt = "N \t Doc \t Term \t\t\t Frequence \t\t Weight\n"
        for item in desc[doc_adapted]:
            j += 1
            for value in desc[doc_adapted][item]:
                itemstring = f"{j} \t {int(doc_adapted)+1} \t {item} \t\t\t {value} \t\t {desc[doc_adapted][item][value]}\n"
                result_txt += itemstring
    else:
        result_txt = inverseSearch(doc, 1, inv)
        
    return result_txt

# Display a given term appearence, frequency and weight
def inverseSearch(search_term, stemmingOP, inv):
    # normalizing query
    if stemmingOP == 1:
        # Porter
        search_term = nltk.PorterStemmer().stem(search_term)
    else:
        # Lancaster
        search_term = nltk.LancasterStemmer().stem(search_term)
        
    if search_term in inv.keys():
        j = 0
        result_txt = "N \t Term \t Doc \t Freq \t Weight\n"
        # iterate through search term dictionary
        for doc in inv[search_term]: # docs
                j += 1
                for value in inv[search_term][doc]: # frequency               
                    itemstring = f"{j} \t {search_term} \t {int(doc)+1} \t {value} \t {inv[search_term][doc][value]}\n"
                    result_txt += itemstring
    else:
        result_txt = (f"No inverse search results found for {search_term}")
        
    return result_txt