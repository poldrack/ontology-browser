from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse
from .forms import SearchForm, ReviewForm, ConceptSearchForm
from .mongodb_utils import (
    get_task_collection,
    search_tasks,
    get_task_by_id,
    save_review,
    get_all_tasks,
    get_all_concepts,
    search_concepts,
    get_concept_by_id,
    save_concept_review
)

# Create your views here.

def test_connection(request):
    try:
        collection = get_task_collection()
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
        results = search_tasks(query, type_filter)
    
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

def concept_list(request):
    """View for listing all concepts"""
    concepts = get_all_concepts()
    return render(request, 'browser/concept_list.html', {
        'concepts': concepts
    })

def concept_search(request, concept_id=None):
    """View for searching concepts"""
    form = ConceptSearchForm(request.GET)
    results = []
    query = ''
    
    if concept_id:
        # If searching by ID, use that as the query
        query = concept_id
        results = search_concepts(concept_id)
    elif form.is_valid():
        query = form.cleaned_data.get('query', '')
        results = search_concepts(query)
    
    return render(request, 'browser/concept_search.html', {
        'form': form,
        'results': results,
        'query': query
    })

def concept_detail(request, concept_id):
    """View for displaying concept details"""
    concept = get_concept_by_id(concept_id)
    if concept is None:
        raise Http404("Concept not found")
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            save_concept_review(
                concept_id,
                form.cleaned_data['status'],
                form.cleaned_data['comment']
            )
            return redirect('concept_detail', concept_id=concept_id)
    else:
        # Pre-fill form with existing review if it exists
        initial_data = {
            'status': concept.get('review_status', ''),
            'comment': concept.get('review_comment', '')
        }
        form = ReviewForm(initial=initial_data)
    
    return render(request, 'browser/concept_detail.html', {
        'concept': concept,
        'review_form': form
    })

def home(request):
    """View for the home page"""
    return render(request, 'browser/home.html')