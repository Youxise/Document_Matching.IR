from Data import loadJudgements

# Calculate evaluation using judgements & models results
def evaluation(result, index):
    
    result = list(result.keys())
    selected = [int(x) for x in result]
    relevant = set([int(x) for x in loadJudgements("LISA.REL")[index]]) # getting the relevant docs from the file
    # Metrics : Precision - Recall - F1
    Precision = len(relevant.intersection(selected)) / len(selected) if len(selected) else 0
    P5 = len(relevant.intersection(selected[:5])) / 5
    P10 = len(relevant.intersection(selected[:10])) / 10
    Recall = len(relevant.intersection(selected)) / len(relevant) if len(relevant) else 0
    Fscore = (2 * Precision * Recall) / (Precision + Recall) if Precision + Recall else 0
    # PR curve
    if len(selected) > 10:
        ranks = selected[:10]
    else:
        ranks = selected + [-1] * (10 - len(selected))

    pi = []
    ri = []
    current_relevant = set()
        
    for i in range(len(ranks)):
        # if the item is relevant
        if ranks[i] in relevant:
            # add it to the set of currently relevant items
            current_relevant.add(ranks[i])
        # calculate precision at the current rank and append to the pi list
        pi.append(len(current_relevant) / (i + 1))
        # calculate recall at the current rank and append to the ri list
        ri.append(len(current_relevant) / len(relevant) if len(relevant) else 0)

    pj = []
    rj = [i / 10 for i in range(0, 11)]
    i = 0
    current = max(pi)
        
    for j in range(len(ranks) + 1):
        if ri[i] >= rj[j]:
            # if the current recall point is greater than the specified recall point rj, 
            # append the current precision value to pj
            pj.append(current)
        else:
            # if not, find the point where ri becomes greater than or equal to rj
            while i < len(ri) - 1 and ri[i] < rj[j]:
                i += 1
            # if i is less than 10, update the current precision to the maximum value in the remaining pi values
            if i < 10:
                current = max(pi[i:])
            else:
                # if not, set the current precision to 0
                current = 0
            # append the updated current precision value to pj
            pj.append(current)
    
    return {
            "Precision": round(Precision, 4),
            "P@5": round(P5, 4),
            "P@10": round(P10, 4),
            "Recall": round(Recall, 4),
            "F1 score": round(Fscore, 4),
        }, {"recall": rj, "precision": pj}