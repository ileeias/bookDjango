from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from .models import *


def main_view(request):
    # request -> Запрос, который приходит от браузера
    # request.method -> Указывает каким методом был отправлен запрос(GET, POST)
    # print(request.method)  # GET

    # books = Book.objects.all()  # Возвращает все записи из таблицы Book(QuerySet)
    # print(books)
    # books = Book.objects.filter(name='Алхимик')  # Возвращает записи из таблицы Book по условию name='Алхимик'(QuerySet)
    # print(books)
    # books = Book.objects.get(id=1)  # Возвращает только одну запись из таблицы Book по условию id=1(Object)
    #                                 # (Ошибка, если их несколько)
    # print(books)

    books = Book.objects.filter(is_popular=True)  # Возвращает все книги с is_popular=True
    authors = Author.objects.all()

    # for i in range(len(books)):
    #     books[i].name = books[i].name.upper()

    context = {
        'books': books,
        'word': 'HELLO!!!',
        'authors': authors
    }
    # context -> dict. Данные, которые отправляем от вью в темплейт
    return render(request, 'main_template.html', context=context)
    # render -> Функция Django, которая прорисовывает темлейт
    # render(<request>, '<template_name>', context=<context>)

def genres_list(request):
    genres = Genre.objects.all()
    context = {
        'genres': genres,
        'word': 'ALL GENRES!'
    }
    return render(request, 'genres_list_template.html', context=context)

def authors_list(request):
    authors = Author.objects.all()
    context = {
        'authors': authors,
        'word': 'ALL AUTHORS!'
    }
    return render(request, 'authors_list_template.html', context=context)

def text_list(request):
    text = Textfount.objects.all()
    context = {
        'text': text,
        'word': 'ALL text!'
    }
    return render(request, 'text_list_template.html', context=context)

# напомнить как сделать update, create, delete, detail
def book_detail_view(request, book_id):
    try:
        book_object = Book.objects.get(id=book_id)
        context = {
            'book': book_object
        }
        return render(request, 'book_detail.html', context=context)
    except ObjectDoesNotExist:
        context = {}
        return render(request, 'book_detail.html', context=context)

def book_create_view(request):
    if request.method == 'GET':
        # GET -> Вернуть "бланк" html
        authors = Author.objects.all()
        genres = Genre.objects.all()
        context = {
            'authors': authors,
            'genres': genres
        }
        return render(request, 'book_create.html', context=context)
    elif request.method == 'POST':
        name = request.POST.get('book_name')

        author = request.POST.get('book_author')
        author = Author.objects.get(id=author)
        # Находим автора в SQL по принятому id

        genre = request.POST.get('book_genre')
        genre = Genre.objects.get(id=genre)
        # Находим жанра в SQL по принятому id

        year = int(request.POST.get('book_year'))

        is_popular = request.POST.get('book_is_popular')
        if is_popular == 'on':
            is_popular = True
        else:
            is_popular = False

        book = Book(
            name=name,
            author=author,
            genre=genre,
            year=year,
            is_popular=is_popular
        )  # Создаем книгу в виде объекта
        book.save()  # Сохраняет объект в базе данных

        context = {
            'book': book
        }
        return render(request, 'book_detail.html', context=context)

def author_create_view(request):
    if request.method == 'GET':
        authors = Author.objects.all()
        context = {
            'authors': authors
        }
        return render(request, 'author_create.html', context=context)
    elif request.method == 'POST':
        surname = request.POST.get('author_surname')
        name = request.POST.get('author_name')
        bio = request.POST.get('author_bio')

        author = Author(
            surname=surname,
            name=name,
            bio=bio
        )
        author.save()
        authors=Author.objects.all()
        context = {
            'authors': authors,
            'word': 'Все Авторы.'
        }
        return render(request, 'authors_list_template.html', context=context)

def book_delete_view(request, book_id):
    if request.method == 'POST':
        from django.shortcuts import redirect
        book = Book.objects.get(id=book_id)
        book.delete()  # delete() -> Удаляет объект из Базы Данных
        return redirect(main_view)

def book_update_view(request, book_id):
    if request.method == 'GET':
        book = Book.objects.get(id=book_id)
        authors = Author.objects.all()
        genres = Genre.objects.all()
        context = {
            'book': book,
            'authors': authors,
            'genres': genres
        }
        return render(request, 'book_update.html', context=context)

    elif request.method == 'POST':
        name = request.POST.get('book_name')

        author = request.POST.get('book_author')
        author = Author.objects.get(id=author)

        genre = request.POST.get('book_genre')
        genre = Genre.objects.get(id=genre)

        year = int(request.POST.get('book_year'))

        is_popular = request.POST.get('book_is_popular')
        if is_popular == 'on':
            is_popular = True
        else:
            is_popular = False

        book = Book.objects.get(id=book_id)
        book.name = name  # Обновляем имя
        book.author = author  # Обновляем автора
        book.genre = genre  # Обновляем жанр
        book.year = year  # Обновляем год
        book.is_popular = is_popular  # Обновляем популярность
        book.save()

        from django.shortcuts import redirect
        return redirect(book_detail_view, book_id=book_id)
def author_detail_view(request, author_id):
    try:
        author_object = Author.objects.get(id=author_id)
        context = {
            'author': author_object
        }
        return render(request, 'author_detail.html', context=context)
    except ObjectDoesNotExist:
        context = {}
        return render(request, 'author_detail.html', context=context)
def author_delete_view(request, author_id):
    if request.method == 'POST':
        from django.shortcuts import redirect
        author = Author.objects.get(id=author_id)
        author.delete()  # delete() -> Удаляет объект из Базы Данных
        return redirect(main_view)

def author_update_view(request, author_id):
    if request.method == 'GET':
        author = Author.objects.get(id=author_id)
        authors = Author.objects.all()
        context = {
            'authors': authors,
            'author': author
        }
        return render(request, 'author_update.html', context=context)

    elif request.method == 'POST':
        surname = request.POST.get('author_surname')
        name = request.POST.get('author_name')
        bio = request.POST.get('author_bio')

        author = Author.objects.get(id=author_id)
        author.surname = surname
        author.name = name
        author.bio = bio
        author.save()
        from django.shortcuts import redirect
        return redirect(author_detail_view, author_id=author_id)