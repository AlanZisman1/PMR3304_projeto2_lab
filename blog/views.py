from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post, Comment
from .forms import PostForm, CommentForm

# LISTAGEM
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'  # Importante: O template espera a variável 'posts'
    ordering = ['-created_at']

# DETALHES
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    # O DetailView busca automaticamente pelo PK na URL e gera o 404 se não achar

# CRIAÇÃO
class PostCreateView(CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content'] # Define os campos do formulário aqui
    # Ao salvar com sucesso, ele busca o get_absolute_url do Model para redirecionar

# EDIÇÃO
class PostUpdateView(UpdateView):
    model = Post
    template_name = 'blog/post_form.html' # Reutiliza o mesmo form de criação
    fields = ['title', 'content']

# REMOÇÃO
class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list') # Redireciona para a home após deletar

# ADICIONAR COMENTÁRIO
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user 
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    
    return render(request, 'blog/add_comment.html', {'form': form, 'post': post})