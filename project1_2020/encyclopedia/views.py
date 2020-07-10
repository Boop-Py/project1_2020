from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django import forms
from django.http import Http404
from . import util
from markdown2 import *
import random
import re

class New_Content_Form(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Content")
     
def todolist(request):
    return render(request, "encyclopedia/todolist.html") 
 
 
 ##make search function work on all pages. redirect to /search + make a search function?
 
 
def index(request):   
    if request.method == "POST":
        # retrieve data from the form
        search_form_result = request.POST
        entry_title = search_form_result.get("query")
        # check if that is the name of an entry
        content = util.get_entry(entry_title)
        if content is not None:  
            # redirect to that page if it is an exact match
            return HttpResponseRedirect(entry_title)          
        elif content is None:  
            # if not a match, search for substring in all of the titles
            all = util.list_entries()
            r = re.compile('.*(%s).*'%entry_title)
            # presents a list of all titles with that substring
            matches = list(filter(r.match, all))          
            return render(request, "encyclopedia/index.html", {
                "matches": matches
                })       
        else:
            return render(request, "encyclopedia/index.html", {
                "matches": util.list_entries()  
                })
    # list of all markdown files on the homepage
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
        })
 
def randomise(request):
    if request.method == "GET":
        #takes a random choice from all of the entries and redirects to it
        randomised_choice = random.choice(util.list_entries())
        return HttpResponseRedirect(randomised_choice)
    else:
        return render(request, "encyclopedia/index.html")        
 
def result(request, title): 
    content = util.get_entry(title)
    # check if 
    if content:
        # convert markdown content to html
        markdown = Markdown()
        html = markdown.convert(content)
        # if entry exists, displates content and titles
        return render(request, "encyclopedia/result.html", {  
        "content": html,
        "title": title
        })
    else:
        # raises error message if not found
        raise Http404("Query does not exist. Please try again.")
 
def add(request):
    if request.method == "POST":
        # retrieves form content
        form = New_Content_Form(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            # check title does not already exist. shows error message if it does.
            exists = util.get_entry(title)
            if exists is None: 
                # saves entry as a md file
                util.save_entry(title, content) 
                # redirect to new page
                return HttpResponseRedirect(title)
            else:
                return render(request, "encyclopedia/add.html", {
                    "form": New_Content_Form(), 
                    "message": "Page already exists."
                    })                
        else:     
            return render(request, "encyclopedia/add.html", {
                "form": form
                }) 
    return render(request, "encyclopedia/add.html", {
        "form": New_Content_Form()
        })   
   
def edit(request, title):
    if request.method == "POST":
        edit_form_result = request.POST
        edited_content = edit_form_result.get("edit_content")
        print(title)
        print(edited_content)
        util.save_entry(title, edited_content)
        return HttpResponseRedirect(title) 
 
        
        ##save_entry
        ##redirect to page
    else: 
        form_content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
        "title": title,
        "form_content": form_content
        })   


    


