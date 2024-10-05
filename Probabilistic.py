from collections import defaultdict, OrderedDict
import math

# Remove weights from Descriptor
def freqByDoc(descriptor):
    new_dc = defaultdict(dict)
    for doc in descriptor:
        for term in descriptor[doc].keys():
            new_dc[doc][term] = int(next(iter(descriptor[doc][term])))
    return new_dc

# Apply BM25 model using K & B
def BM25(descriptor2, inverse, K, B, query):
        
    if len(query):
        # init
        liste = {}
        avdl = N = 0

        descriptor = freqByDoc(descriptor2)
        for doc in descriptor:
            avdl += sum(descriptor[doc].values()) # avdl = collection length 
            N += 1 # N = number of docs
        avdl = avdl / N
        for doc in descriptor:     # iterating through docs
            RSV = 0 # init RSV
            dl = sum(descriptor[doc].values())  # dl = doc length
            dCTE = K * ((1 - B) + B * (dl / avdl))
            for term in query:
            # if doc contains term
                if term in descriptor[doc].keys():
                    freq = descriptor[doc][term] # frequency
                else:
                    continue # RSVi = 0
            # if collection contains term    
                if term in inverse.keys():   
                    Ni = len(inverse[term]) # appearence
                else:
                    Ni = 0
                RSV += (freq / (dCTE + freq)) * math.log10((N - Ni + 0.5)/(Ni + 0.5))
            if RSV == 0:
                continue
            liste[int(doc)+1] = round(RSV, 4)

        # displaying relevant docs in order
        if liste == {}:
            return "No relevant docs.", None
        liste = OrderedDict(sorted(liste.items(), key=lambda x: x[1], reverse=True))
        result_txt = "Doc \t Relevance\n"
        for key, value in liste.items():
            result_txt += f"{key} \t {value}\n"
    else:
        liste = None
        result_txt = "Error: empty query."
    return result_txt, liste