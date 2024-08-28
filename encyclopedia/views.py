from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from . import util
import markdown2
import random

def index(request):
    entries = util.list_entries()
    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })

def entry(request, title):
    entry_content = util.get_entry(title)
    if entry_content is None:
        return HttpResponseNotFound("Page not found.")
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": markdown2.markdown(entry_content)
    })

def search(request):
    query = request.GET.get('q', '')
    entries = util.list_entries()
    if util.get_entry(query):
        return redirect('entry', title=query)
    results = [entry for entry in entries if query.lower() in entry.lower()]
    return render(request, "encyclopedia/search.html", {
        "query": query,
        "results": results
    })

def create(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        if util.get_entry(title):
            return render(request, "encyclopedia/create.html", {
                "error": "Entry already exists."
            })
        util.save_entry(title, content)
        return redirect('entry', title=title)
    return render(request, "encyclopedia/create.html")

def edit(request, title):
    if request.method == "POST":
        content = request.POST['content']
        util.save_entry(title, content)
        return redirect('entry', title=title)
    entry_content = util.get_entry(title)
    if entry_content is None:
        return HttpResponseNotFound("Page not found.")
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": entry_content
    })

def random_page(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return redirect('entry', title=random_entry)
