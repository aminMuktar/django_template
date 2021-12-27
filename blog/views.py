from django.shortcuts import render,get_object_or_404
from blog.models import Post,Comment
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from blog.forms import EmailPostForm,CommentForm
from django.core.mail import message, send_mail



def post_list(request):
    object_list=Post.published.all()
    # retrieve max of 3 pages
    paginator=Paginator(object_list,3)
    page=request.GET.get('page')
    try:
        posts=paginator.page(page)
    except PageNotAnInteger:
        posts=paginator.page(1)
    except EmptyPage:
        posts=paginator.page(paginator.num_pages)
    return render(request,'blog/post/list.html',{'posts':posts})

def post_detail(request,year,month,day,post):
    post=get_object_or_404(Post,slug=post,
                                status='published',
                                publish__year=year,
                                publish__month=month,
                                publish__day=day
        )
    comments=post.comments.filter(active=True)
    if request.method == 'POST':
        comment_form=CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment=comment_form.save(commit=False)
            new_comment.post=post
            new_comment.save()
    else:
        comment_form=CommentForm()
    return render(request,'blog/post/detail.html',{'post':post,
                                                    'comments':comments,
                                                    'comment_form':comment_form
                                                })

def post_share(request,post_id):
    post=get_object_or_404(Post,id=post_id,status='published')
    sent=False
    if request.method == 'POST':
        form=EmailPostForm(request.POST)
        if form.is_valid():
            # adictionary of form fields with their values
            cd=form.cleaned_data
            post_url=request.build_absolute_uri(post.get_absolute_url())
            subject='{} ({}) recommended you reading "{}"'.format(cd['name'],cd['email'],post.title)
            message='read "{}" at {}\n\n {}\'s comments: {}'.format(post.title,post_url,cd['name'],cd['comments'])
            # don't spam me(only contact)
            send_mail(subject,message,'myblog@mysite.com',[cd['to']])
            sent=True
    else:
        form=EmailPostForm()
    return render(request,'blog/post/share.html',{'post':post,
                                                    'form':form,
                                                    'sent':sent
                                                        })