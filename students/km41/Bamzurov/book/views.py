
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from course.forms import SignUpForm
from book.models import Book, Group
from django.forms import ModelForm
from django.http import Http404
from django.db import connection, transaction, IntegrityError
import pdb;

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'book/signup.html', {'form': form})

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'author', 'pub_date']


@login_required(login_url='/book/login/')
def book_list(request, template_name='book/lib.html'):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM BOOKS")
        table = dictfetchall(cursor)
    #book = Book.objects.all()
    data = {}
    data['object_list'] = table
    data['user'] = request.user
    receiveForm = request.POST or None
    if receiveForm:
        try:
            addBooksToGroup(receiveForm)
        except IntegrityError:
            data['error'] = 'SELECT ALL FIELDS'
            return render(request, template_name, data)

                #raise Http404('book_list not')
    return render(request, template_name, data)

@transaction.atomic
def addBooksToGroup(receiveForm):
    for i in Book.objects.all():
        a = receiveForm.get('group_'+str(i.id))
        if a:
            selectedGroup = Group.objects.get(name=a)
            selectedBook = Book.objects.get(pk=i.id)
            selectedGroup.books.add(selectedBook)  
        else:
            raise IntegrityError('int')



def liber(request, pk):
    book = get_object_or_404(Book, pk=pk)
    data = {}
    data['object'] = book
    return render(request, 'book/liber.html', data)

class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ['name']

@login_required
def home(request, template_name='book/home.html'):
    group = Group.objects.filter(owner=request.user)
    data = {}
    data['object'] = group
    return render(request, template_name, data)

@login_required
def createGroup(request, template_name='book/createGroup.html'):
    form = request.POST or None
    if form:
        cursor = connection.cursor()
        cursor.callproc('groupPackage.groupCreateProc', [form['name'], request.user.id])
        #group = form.save(commit=False)
        #group.owner = request.user
        #group.save()
        return redirect('home')
    return render(request, template_name, {'form': GroupForm()})

@login_required
def groupBooks(request, pk, template_name='book/group.html'):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM BOOKS, BOOKGROUPVIEW WHERE BOOKS.ID = BOOKGROUPVIEW.BOOK_ID AND GROUP_ID = %s" % pk)
        table = dictfetchall(cursor)
    group = Group.objects.get(pk=pk)
    books = group.books.all()
    data = {}
    data['object'] = table
    data['group'] = pk
    return render(request, template_name, data)

@login_required
def deleteBookFromGroup(request, book_id, group_id):
    book = get_object_or_404(Book, pk=book_id)
    group = get_object_or_404(Group, pk=group_id)
    #pdb.set_trace()
    if request.method=='POST':
        with connection.cursor() as cursor:
            cursor.callproc('bookGroupPackage.deleteBookFromGroupPROC', [int(book_id), int(group_id)])
    #except(KeyError, Book.DoesNotExist, Group.DoesNotExist):
    #    return render(request, 'book/home.html')
        return redirect('home')
    return render(request, 'book/home.html')

@login_required
def deleteGroup(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    if request.method=='POST':
        with connection.cursor() as cursor:
            cursor.callproc('groupPackage.groupdeleteproc', [int(group_id)])
        return redirect('home')
    return render(request, 'book/home.html')

@login_required
def editGroup(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    if request.method=='POST':
        new_name = request.POST.get('newEdit', group.name)
        #pdb.set_trace()
        with connection.cursor() as cursor:
            cursor.callproc('groupPackage.groupeditproc', [int(group_id), new_name])
        return redirect('home')
    return render(request, 'book/home.html')




