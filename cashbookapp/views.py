from pickle import TRUE
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CashbookForm, CommentForm, HashtagForm
from django.utils import timezone
from .models import Cashbook, Comment, Tag
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required


# Create your views here.

def main(request):
    return render(request, 'main.html')

def write(request, cashbook = None):
    if request.method == 'POST':
        form = CashbookForm(request.POST, request.FILES, instance=cashbook)
        if form.is_valid():
            cashbook = form.save(commit=False)
            cashbook.pub_date = timezone.now()
            cashbook.save()
            #post=form.save_m2m()
            #post.save()
            #태그 처리
            content = request.POST.get('posting_content')
            c_list = content.split(' ')

            for c in c_list:
                if '#' in c:
                    tag = Tag()
                    tag.tag_content = c
                    tag.save()

                    cashbook_ = Cashbook.objects.get(pk=cashbook.pk)
                    cashbook_.tagging.add(tag)
            return redirect('main')
        else:
            context = {
                'form':form,
            }
            return render(request, 'write.html', context)
    else:
        form = CashbookForm(instance= cashbook)
        return render(request, 'write.html', {'form':form})


#해시태그 정렬        
def read(request):
    cashbooks = Cashbook.objects
    return render(request, 'read.html', {'cashbooks':cashbooks})

@login_required
def detail(request, id):
    cashbooks = get_object_or_404(Cashbook, id=id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit = False)
            comment.cashbook_id = cashbooks
            comment.comment_writer = request.user
            comment.text = form.cleaned_data['text']
            comment.save()
            id=id
            return redirect('detail', id)
    else:
        form = CommentForm
        return render(request, 'detail.html', {'cashbooks':cashbooks, 'form':form})

def edit(request, id):
    cashbooks = get_object_or_404(Cashbook, id=id)
    if request.method == "POST":
        form = CashbookForm(request.POST, instance=cashbooks)
        if form.is_valid():
            form.save(commit=False)
            form.save()
            return redirect('read')

    else:
        form = CashbookForm(instance=cashbooks)
        return render(request, 'edit.html', {'form':form, 'cashbooks':cashbooks})

def delete(request, id):
    cashbooks = get_object_or_404(Cashbook, id=id)
    cashbooks.delete()
    return redirect('read')

def update_comment(request, id, com_id):
    post = get_object_or_404(Cashbook, id=id)
    comment = get_object_or_404(Comment, id=com_id)
    form = CommentForm(instance=comment)
    if request.method == "POST":
        update_form = CommentForm(request.POST, instance = comment)
        if update_form.is_valid():
            update_form.save()
            return redirect('detail', id)
    return render(request, 'update_comment.html', {'form':form, 'post':post, 'comment':comment})

def delete_comment(request, post_id, com_id):
    mycom = Comment.objects.get(id=com_id)
    mycom.delete()
    return redirect('detail', post_id)

def hashtag(request, tag = None):
    if request.method == 'POST':
        form = HashtagForm(request.POST, instance = tag)
        if form.is_valid():
            tag = form.save(commit = False)
            if Tag.objects.filter(tag_content=form.cleaned_data['tag_content']):
                form = HashtagForm()
                error_message = '이미 존재하는 해시태그입니다.'
                return render(request, 'hashtag.html', {'form':form, 'error_message':error_message})
            else:
                tag.tag_content = form.cleaned_data['tag_content']
                tag.save()
            return redirect('read')
    else:
        form = HashtagForm(instance=tag)
        return render(request, 'hashtag.html', {'form':form})
#해시태그 검색
def hashtag_search(request, id):
    tagging = get_object_or_404(Tag, id=id)
    tag = Tag.objects.filter(tag_content=tagging) 
    post = Cashbook.objects.filter(tagging__in = tag).order_by('-pub_date')# 해당 태그를 가진 post 저장
    return render(request, 'search_result.html', { 'tag':tag, 'post':post})
    

def likes(request, id):
    like_b = get_object_or_404(Cashbook, id=id)
    if request.user in like_b.post_like.all():
        like_b.post_like.remove(request.user)
        like_b.like_count -= 1
        like_b.save()
    else:
        like_b.post_like.add(request.user)
        like_b.like_count += 1
        like_b.save()
    return redirect('detail', like_b.id)

