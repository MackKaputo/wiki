from django.shortcuts import render
from django.http import HttpResponse
from . import util
import markdown2
from django.shortcuts import redirect
import re 
from django import forms
import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

#The entry function:
def entry(request, title):
    #check if title exists:
    if request.method == "GET":

        if title in util.list_entries():
            #Get the entry, convert to html and pass it to template:
            myentry = util.get_entry(title)
            content = markdown2.markdown(myentry)
            return render(request, "encyclopedia/entry.html", {
                "content": content,
                "title" : title
            })
        else:
            return HttpResponse("<h1>The requested page was not found</h1>") 


def search(request):
    if request.method == 'POST':
        q = request.POST.get('q')
        entrylist = util.list_entries()
    #Check if query (q) is in the list:
        if q in entrylist:
            #Redirect to the entry page requested:
            return redirect("encyclopedia:entry", title = q)
        elif q not in entrylist:
                pattern = q
                result = []
                for entry in entrylist:
                    check = re.search(pattern, entry)
                    if check:
                        result.append(entry)
                return render(request, "encyclopedia/search.html",{
                    "result" : result
            })

class NewPage(forms.Form):
    entry_title = forms.CharField(label = "Title")
    entry_content = forms.CharField(widget = forms.Textarea, label = "Content")

def newpage(request):
    if request.method == 'POST':
        form = NewPage(request.POST)
        if form.is_valid():
            title = form.cleaned_data["entry_title"]
            content = form.cleaned_data["entry_content"]
            if title in util.list_entries():
                return HttpResponse("<h1> Error: The encyclopedia" 
                " entry already exists</h1>")
            else:
                util.save_entry(title, content)
                return redirect("encyclopedia:entry", title = title,)
        else:
            return render(request, "encyclopedia/newpage.html",{
                "form":form
            })
    
    return render(request,"encyclopedia/newpage.html",{
        "form":NewPage()
    })
       

def edit(request, title):
    
    if request.method =="GET":
        initial_title = title
        initial_content = util.get_entry(initial_title)
        form = NewPage(initial={'entry_title':initial_title,
            'entry_content':initial_content})  
        return render(request,"encyclopedia/edit.html",{
            "title":initial_title,
            "form":form
        })
    elif request.method =="POST":
        form = NewPage(request.POST)
        if form.is_valid():
            title1 = form.cleaned_data["entry_title"]
            content = form.cleaned_data["entry_content"]
            util.save_entry(title1, content)
            return redirect("encyclopedia:entry", title = title1)

def randompage(request):
    random_entry = random.choice(util.list_entries())
    return redirect("encyclopedia:entry", title= random_entry)
