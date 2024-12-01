import re
from .models import Term, TermDocument, Document


def clean_text(text):
    # Replace punctuation with whitespace
    text = re.sub(r'[.,!?;:]', ' ', text)
    # Replace multiple consecutive white spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    #convert to lowercase
    text = text.lower()
    return text.strip()


def reverse_index(question_text, answer_text, document_id):
    term_ids = set()
    
    # Clean and tokenize the question text
    question_text = clean_text(question_text)
    question_tokens = question_text.split()

    for token in question_tokens:
        term, created = Term.objects.get_or_create(term=token)
        term_ids.add(term.id)
    
    # Clean and tokenize the answer text
    answer_text = clean_text(answer_text)
    answer_tokens = answer_text.split()

    for token in answer_tokens:
        term, created = Term.objects.get_or_create(term=token)
        term_ids.add(term.id)
    
    # Add entries to the TermDocument table
    for term_id in term_ids:
        TermDocument.objects.create(term_id=term_id, document_id=document_id)



def boolean_search(query):
    # Step 1: Clean and tokenize the query
    cleaned_query = clean_text(query)
    tokens = cleaned_query.split()

    if not tokens:
        return Document.objects.none()  # Return no documents if query is empty

    # Step 2: Fetch document IDs from reverse index
    document_sets = []
    for token in tokens:
        try:
            term = Term.objects.get(term=token)
            term_documents = TermDocument.objects.filter(term=term)
            document_ids = set(term_documents.values_list('document_id', flat=True))
            document_sets.append(document_ids)
        except Term.DoesNotExist:
            return Document.objects.none()  # If any token is not found, no documents can match

    # Step 3: Find common document IDs containing all tokens
    if document_sets:
        common_document_ids = set.intersection(*document_sets)
    else:
        common_document_ids = set()

    # Step 4: Retrieve and return documents
    return Document.objects.filter(id__in=common_document_ids)
