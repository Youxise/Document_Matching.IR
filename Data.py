import re

# Load LISA collection and extract its documents
def loadCollection(file_path):
    
    with open(file_path, 'r', encoding='utf-8') as file:
        collection = file.read()
    
    # split documents based on the asterisk pattern
    documents = re.split(r'\*{40,}', collection.lower())
    # filter out empty strings and remove leading/trailing whitespaces
    documents = [doc.strip() for doc in documents if doc.strip()]
    # removing "document [number]" from each document
    documents = [re.sub(r'^document\s+\d+\s*', '', doc) for doc in documents]
    # removing "\n"
    for i, doc in enumerate(documents, 1):
        documents[i-1] = re.sub(r"[\n]", " ", doc)
            
    return documents

# Load LISA queries 
def loadQueries(queries_file):
    with open(queries_file, 'r') as file:
        # extract queries with "|" as a separator
        queries = [line.strip().split('|', 1) for line in file]
    return queries

# Load LISA judgements
def loadJudgements(file_path):
    # dict to store relevant references for each query
    relevant_refs_by_query = {}

    with open(file_path, 'r') as file:
        current_query_number = None
        current_relevant_refs = []
        relevant_refs_line = False

        for line in file:
            line = line.strip() # remove leading and trailing whitespaces

            if line.startswith("Query"):
                # extract the query number from the line
                current_query_number = int(line.split()[1])

                # init an empty list for the relevant references for the current query
                relevant_refs_by_query[current_query_number] = []

            elif "Relevant Refs" in line:
                # set a flag to indicate that the next lines will contain relevant references
                relevant_refs_line = True

            # check if the line is not empty and we are in the relevant_refs_line section
            elif line.strip() and relevant_refs_line:
                # split the line into a list of relevant references
                current_relevant_refs = line.split()

                # append each relevant reference to the list for the current query
                for val in current_relevant_refs[:-1]:
                    relevant_refs_by_query[current_query_number].append(val)

                # reset flag
                relevant_refs_line = False

    return relevant_refs_by_query

