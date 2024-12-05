from django.shortcuts import render, redirect,get_object_or_404
from .models import BlogPost,Comment
from .forms import BlogPostForm
from .forms import CommentForm

def post_list(request):
    posts = BlogPost.objects.all()
    return render(request, 'post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = BlogPost.objects.get(pk=pk)
    comments = post.comment_set.all()
    return render(request, 'post_detail.html', {'post': post, 'comments': comments})

def create_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = BlogPostForm()
    return render(request, 'create_post.html', {'form': form})

def edit_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'edit_post.html', {'form': form})


def add_comment(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if post is None:
        print("Aucun article trouvé.") 
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)  # Redirige avec pk
    else:
        form = CommentForm()
    return render(request, 'add_comment.html', {'form': form})



def edit_comment(request, post_pk, comment_pk):
    post = get_object_or_404(BlogPost, pk=post_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'edit_comment.html', {'form': form, 'post': post, 'comment': comment})


def delete_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    post.delete()
    return redirect('post_list')


def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)

