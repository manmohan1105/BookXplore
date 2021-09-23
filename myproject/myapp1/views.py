import requests
from django.shortcuts import render ,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .form import CreateUserForm,BookSearch
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import requests
from django.http import HttpResponseRedirect

from .models import History ,savedbook
def index(request):
    
    return render(request,'index.html',{'name':'naman'})


def counter(request):
    text=request.GET['fname']
    return render(request,'index.html',{'name':text})  


def register(request):
    form =CreateUserForm()
    if request.method=='POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
           form.save()
           user=form.cleaned_data.get('username')
           messages.success(request,'Account created for '+ user)
           return redirect('loginpage')   
    context={'form':form}
    return render(request,'register.html',context)      


def loginpage(request):

    context={}
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'username or password incorrect')  
            return render(request,'login.html',context)   

    return render(request,'login.html',context)    
@login_required(login_url='loginpage')
def home(request):
    context={}
    form=BookSearch()

    data= History.objects.all().filter(user=request.user)

    rec=[]
    cnt=0
    for i in data:
            rec.append(i.isbn)
            cnt+=1
            if cnt==2:
                break
    rec.append("Life Goal")        
    recbooks = []
    if rec:
            
            for i in rec:
                 url="https://www.googleapis.com/books/v1/volumes?q="+i
                 r = requests.get(url)
                 if r.status_code != 200:
                       continue
                       
                 data = r.json()
                 if not 'items' in data:
                      continue
                 fetched_books = data['items']
                
                 for book in fetched_books:
                     book_dict = {
                     'id':book['id'],
                     'title': book['volumeInfo']['title'],
                     'image': book['volumeInfo']['imageLinks']['thumbnail'] if 'imageLinks' in book['volumeInfo'] else "",
                     'authors': ", ".join(book['volumeInfo']['authors']) if 'authors' in book['volumeInfo'] else "",
                     'publisher': book['volumeInfo']['publisher'] if 'publisher' in book['volumeInfo'] else "",
                     'info': book['volumeInfo']['infoLink'],
                     'popularity': book['volumeInfo']['ratingsCount'] if 'ratingsCount' in book['volumeInfo'] else 0}
                     recbooks.append(book_dict)

                 def sort_by_pop(e):
                     return e['popularity']

            recbooks.sort(reverse=True, key=sort_by_pop)


    
    if request.method=='POST':
        form=BookSearch(request.POST)
        

        if form.is_valid() :
          
          search=form.cleaned_data['search']
          
          p=History()
          p.user=request.user
          p.isbn=search
          p.save()
          url="https://www.googleapis.com/books/v1/volumes?q="+str(search)
          r = requests.get(url)
          if r.status_code != 200:
             return render(request,'home.html',{'form':form})
          data = r.json()
          if not 'items' in data:
              return render(request,'home.html',{'form':form})
          

          fetched_books = data['items']
          books = []
          for book in fetched_books:
            book_dict = {
              'id':book['id'],
              'title': book['volumeInfo']['title'],
              'image': book['volumeInfo']['imageLinks']['thumbnail'] if 'imageLinks' in book['volumeInfo'] else "",
              'authors': ", ".join(book['volumeInfo']['authors']) if 'authors' in book['volumeInfo'] else "",
              'publisher': book['volumeInfo']['publisher'] if 'publisher' in book['volumeInfo'] else "",
              'info': book['volumeInfo']['infoLink'],
              'popularity': book['volumeInfo']['ratingsCount'] if 'ratingsCount' in book['volumeInfo'] else 0}
            books.append(book_dict)

          def sort_by_pop(e):
               return e['popularity']

          books.sort(reverse=True, key=sort_by_pop)

          return render(request, 'books.html', {'books': books})
        else:
              return redirect('home')
        # all_entries = Entry.objects.all()



    return render(request,'home.html',{'books':recbooks,'form':form})    


def saved(request,user_id):
    print(user_id)
    p=savedbook()
    p.user=request.user
    p.bookid=user_id
    p.save()
    return redirect(request.META['HTTP_REFERER'])
    # return redirect('loginpage')
    # context={}
    # book=request.POST.get("binfo")
    # print(book,book.info)   
def logoutuser(request):
    logout(request)
    context={}
    return redirect('loginpage')
def showhistory(request):
    data= History.objects.all().filter(user=request.user)
    # print(data)
    # d=[]
    # for h in data:
    #     d.append(h.isbn)  
    
    # print(data)
    return render(request,'history.html',{ 'd':data})    

# Create your views here.
def usersavedbook(request):
    data= savedbook.objects.all().filter(user=request.user)
    d=[]
    for d1 in data:
        d.append(d1.bookid)
    url="https://www.googleapis.com/books/v1/volumes/"  
    data1=[]
    for d1 in d:
        furl=url+d1
        r = requests.get(furl)
        if r.status_code != 200:
             continue
        data2 = r.json() 
        data1.append(data2)
    data1={'items':data1}


    fetched_books = data1['items']
    books = []
    for book in fetched_books:
            book_dict = {
              'id':book['id'],
              'title': book['volumeInfo']['title'],
              'image': book['volumeInfo']['imageLinks']['thumbnail'] if 'imageLinks' in book['volumeInfo'] else "",
              'authors': ", ".join(book['volumeInfo']['authors']) if 'authors' in book['volumeInfo'] else "",
              'publisher': book['volumeInfo']['publisher'] if 'publisher' in book['volumeInfo'] else "",
              'info': book['volumeInfo']['infoLink'],
              'popularity': book['volumeInfo']['ratingsCount'] if 'ratingsCount' in book['volumeInfo'] else 0}
            books.append(book_dict)

    def sort_by_pop(e):
               return e['popularity']

    books.sort(reverse=True, key=sort_by_pop)

    return render(request, 'saved.html', {'books': books})
def deletehistory(request,historyid):
        data= History.objects.all().filter(id=historyid)
        data.delete()
        return redirect('showhistory')
def deletebook(request,bookid):
        data= savedbook.objects.all().filter(bookid=bookid)
        data.delete()
        return redirect('usersavedbook')




