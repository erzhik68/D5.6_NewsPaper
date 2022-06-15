# print(data.__dict__) чтоб узнать все варианты
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView  # импортируем класс, который говорит нам о том, что в этом представлении мы будем выводить список объектов из БД
from django.core.paginator import Paginator

from .models import Post
from .filters import PostFilter # импортируем фильтр
from .forms import PostForm # импортируем нашу форму

from datetime import datetime

class PostsList(LoginRequiredMixin, ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'posts.html'  # указываем имя шаблона, в котором будет лежать HTML, в нём будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'posts'  # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    ordering = ['-id']
    paginate_by = 3 # поставим постраничный вывод в один элемент
    # form_class = PostForm # добавляем форм класс, чтобы получать доступ к форме через метод POST

    # метод get_context_data нужен нам для того, чтобы мы могли передать переменные в шаблон. В возвращаемом словаре context будут храниться все переменные. Ключи этого словари и есть переменные, к которым мы сможем потом обратиться через шаблон
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # получили весь контекст из класса-родителя
        context['time_now'] = datetime.utcnow()  # добавим переменную текущей даты time_now
#        context['value1'] = None  # добавим ещё одну пустую переменную, чтобы на её примере посмотреть работу другого фильтра
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset()) # вписываем наш фильтр в контекст
#        context['form'] = PostForm()
        context['is_not_authors'] = not self.request.user.groups.filter(name = 'authors').exists() # добавили новую контекстную переменную is_not_authors
        return context

    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(request.POST) # создаём новую форму, забиваем в неё данные из POST-запроса
    #     if form.is_valid(): # если данные в форме ввели всё правильно, то сохраняем новый пост
    #         form.save()
    #     return super().get(request, *args, **kwargs)

class PostsSearch(ListView):
    model = Post
    template_name = 'newapp/search.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset()) # вписываем наш фильтр в контекст
        return context


# создаём представление, в котором будут детали конкретной отдельной новости
# class PostDetail(DetailView):
#     model = Post # модель всё та же, но мы хотим получать детали конкретной отдельной новости
#     template_name = 'post.html' # название шаблона будет post.html
#     context_object_name = 'post' # название поста

# дженерик для получения деталей о товаре
class PostDetailView(DetailView):
    template_name = 'newapp/post_detail.html'
    queryset = Post.objects.all()


# дженерик для создания поста. Указываем имя шаблона и класс формы.
class PostCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'newapp/post_create.html'
    form_class = PostForm
    permission_required = ('newapp.add_post',
                           'newapp.change_post',
                           'newapp.delete_post')

# дженерик для редактирования поста
class PostUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'newapp/post_create.html'
    form_class = PostForm
    permission_required = ('newapp.add_post',
                           'newapp.change_post',
                           'newapp.delete_post')

    # метод get_object мы используем вместо queryset, чтобы получить информацию о посте который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# дженерик для удаления поста
class PostDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'newapp/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/posts/'
    permission_required = ('newapp.add_post',
                           'newapp.change_post',
                           'newapp.delete_post')