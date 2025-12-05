from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from .models import Post

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

# Criação
def post_create(request):
    if request.method == 'POST':
        # Pegando dados direto do dicionário POST
        titulo = request.POST.get('title')
        conteudo = request.POST.get('content')
        # Criando o objeto sem validação
        Post.objects.create(title=titulo, content=conteudo)
        return redirect('post_list')
    return render(request, 'blog/post_form.html')

# Edição
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()
        return redirect('post_detail', pk=post.pk)
    return render(request, 'blog/post_form.html', {'post': post})

# Remoção
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})