from django.shortcuts import render, redirect, get_object_or_404
from .forms import DocumentForm
from .models import Document
from .utils import reverse_index,boolean_search,clean_text


def add_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST)
        if form.is_valid():
            document = form.save()
            reverse_index(document.question, document.answer, document.id)
            return redirect('add_document')
    else:
        form = DocumentForm()
    return render(request, 'myapp/add_document.html', {'form': form})


def list_questions(request):
    documents = Document.objects.all()
    return render(request, 'myapp/list_questions.html', {'documents': documents})


def search_documents(request):
    query = request.GET.get('q', '')
    algorithm = request.GET.get('algorithm', 'boolean')

    if algorithm == 'boolean':
        documents = boolean_search(query)
    else:
        documents = Document.objects.filter(question__icontains='1') | Document.objects.filter(answer__icontains='1')
    
    tokens = clean_text(query).split()
    
    return render(request, 'myapp/search_results.html', {
        'documents': documents,
        'query': query,
        'algorithm': algorithm,
        'tokens': tokens,
    })


def delete_document(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    if request.method == 'POST':
        document.delete()
        return redirect('list_questions')
    return render(request, 'myapp/list_questions.html', {'documents': Document.objects.all()})
