from django.shortcuts import render
from django.http import JsonResponse
from .mongodb_utils import get_ontology_collection, search_ontology, get_all_tasks, get_task_by_id
from .forms import SearchForm

# Create your views here.

def test_connection(request):
    try:
        collection = get_ontology_collection()
        # Get the first document to test connection
        doc = collection.find_one()
        return JsonResponse({
            'status': 'success',
            'message': 'Connected to MongoDB successfully',
            'sample_doc': str(doc)
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })

def search_view(request):
    form = SearchForm(request.GET)
    results = []
    query = ''
    
    if form.is_valid():
        query = form.cleaned_data.get('query', '')
        type_filter = form.cleaned_data.get('type_filter', 'all')
        results = search_ontology(query, type_filter)
    
    return render(request, 'browser/search.html', {
        'form': form,
        'results': results,
        'query': query
    })


def task_list(request):
    tasks = get_all_tasks()
    return render(request, 'browser/task_list.html', {
        'tasks': tasks
    })

def task_detail(request, task_id):
    task = get_task_by_id(task_id)
    if task is None:
        raise Http404("Task not found")
    return render(request, 'browser/task_detail.html', {
        'task': task
    })