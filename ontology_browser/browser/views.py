from django.shortcuts import render, redirect
from django.http import JsonResponse
from .mongodb_utils import get_ontology_collection, search_ontology, get_all_tasks, get_task_by_id, save_review
from .forms import SearchForm, ReviewForm

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
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            save_review(
                task_id,
                form.cleaned_data['status'],
                form.cleaned_data['comment']
            )
            return redirect('task_detail', task_id=task_id)
    else:
        # Pre-fill form with existing review if it exists
        initial_data = {
            'status': task.get('review_status', ''),
            'comment': task.get('review_comment', '')
        }
        form = ReviewForm(initial=initial_data)
    
    return render(request, 'browser/task_detail.html', {
        'task': task,
        'review_form': form
    })