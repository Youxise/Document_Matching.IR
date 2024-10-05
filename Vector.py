from collections import defaultdict, OrderedDict
import numpy as np

# Apply Vector Support models using: Scalar Product, Cosine and Jaccard measures
def VSM(descriptor, inverse, weights, measure, query2):
        liste = {}
        query = []
        # removing non-existent terms in collection from query
        for word in query2:
            if word not in inverse.keys():
                continue
            query.append(word)
        query = set(query) # removing repetition
        # iterating through docs
        for doc in descriptor:
            w = np.array(weights[int(doc)]) # doc weights
            words = list(descriptor[doc].keys()) # doc words
            words_enc = np.array([1 if word in query else 0 for word in words]) # query weights
            prod0 = np.dot(w, words_enc)
            prod1 = np.sum(np.power(w, 2))
            prod2 = len(query)
        # SCALAR PRODUCT #
            if measure == 0:
                RSV = prod0
        # COSINE #
            elif measure == 1:
                if prod2 == 0: # avoiding div / 0
                    continue
                else:
                    RSV = prod0 / (np.sqrt(prod1) * np.sqrt(prod2)) 
        # JACCARD #
            else:
                if (prod1 + prod2) - prod0 == 0: # avoiding div / 0
                    continue
                else:
                    RSV = prod0 / (prod1 + prod2 - prod0)
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

        return result_txt, liste