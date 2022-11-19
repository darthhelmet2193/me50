from django.shortcuts import render, redirect
from . import util
from django.urls import reverse
from django.http import HttpResponseRedirect
import random
from markdown2 import Markdown 

markdowner = Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def show_entries(request, entry):

    if request.method == "POST":
        markdown_str = util.get_entry(entry)
        return render(request, "encyclopedia/edit_page.html", {
            "previous_entry_content": util.get_entry(entry),
            "edit_title": entry
        })

    if entry not in util.list_entries():
        return render(request, "encyclopedia/error.html", {
            "error_message": "404. Page not found.",
        })
    else:
        markdown_str = util.get_entry(entry)

        return render(request, "encyclopedia/wiki_pages.html", {
            "page_name": markdowner.convert(markdown_str),
            "entry":entry,
        })

def search(request):
    if request.method == "POST":
        search_q = request.POST["q"]
        
        if not search_q:
            return HttpResponseRedirect(reverse("index"))

        recommended_r = []
        
        for entries in util.list_entries():
            if search_q.lower() == entries.lower():
                return HttpResponseRedirect(f"wiki/{entries}")

            if entries.lower().find(search_q.lower()) >= 0:
                recommended_r.append(entries)

        if recommended_r:
            return render(request, "encyclopedia/search.html", {
                "entries": recommended_r
            })
        else:
            return render(request, "encyclopedia/error.html", {
                "error_message": "No results found.",
            })
    


def create_new_page(request):
    
    if request.method == "POST":

        new_page_title = request.POST["title"]

        new_page_content = request.POST["new_entry"]
        
        if not new_page_title:
            return HttpResponseRedirect(reverse("new_page"))
            
        if not new_page_content:
            return HttpResponseRedirect(reverse("new_page"))

        for entries in util.list_entries():
            if entries.lower() == new_page_title.lower():
                return render(request, "encyclopedia/error.html", {
                    "error_message": "Page Already Exists!"
                })
        
        util.save_entry(new_page_title, new_page_content)

        render(request, "encyclopedia/wiki_pages.html", {
            "page_name": util.get_entry(new_page_title),
            "entry": new_page_content,
        })

        return HttpResponseRedirect(f"wiki/{new_page_title}")

        #return show_entries(request, new_page_title)

        #for items in util.list_entries():
        #    if items.lower() == new_page_title.lower():
        #        return render(request, "encyclopedia/wiki_pages.html", {
        #            "page_name": util.get_entry(items),
        #            "entry": items
        #        })
    return render(request, "encyclopedia/new_page.html")

def edit_page(request):

    if request.method == "POST":

        edit_name = request.POST["hidden_value"]
        edit_content = util.get_entry(edit_name)

        

        return render(request, "encyclopedia/edit_page.html", {
            "previous_entry_content": edit_content,
            "edit_title": edit_name  
        })

def save_edit(request):

    if request.method == "POST":

        edit_to_save = request.POST["edit_entry"]
        current_entry = request.POST["current_entry_name"]
        
        util.save_entry(current_entry, edit_to_save)
        
        return HttpResponseRedirect(f"wiki/{current_entry}")

def random_page(request):

    random_entry = random.choice(util.list_entries())

    return HttpResponseRedirect(f"wiki/{random_entry}")
