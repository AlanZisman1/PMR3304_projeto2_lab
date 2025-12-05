from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from .models import Post
from .forms import PostForm

# Listagem
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog/post_list.html', {'posts': posts})

# Detalhes
def post_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        raise Http404("Post não encontrado")
    return render(request, 'blog/post_detail.html', {'post': post})

# CRIAÇÃO (Com Form)
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid(): # O Django verifica se os campos estão ok
            form.save()
            return redirect('post_list')
    else:
        form = PostForm() # Cria um formulário vazio
    return render(request, 'blog/post_form.html', {'form': form})

# EDIÇÃO (Com Form)
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        # Passamos 'instance=post' para o Django saber QUAL post atualizar
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        # Preenche o formulário com os dados existentes do post
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form})

# Remoção
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})