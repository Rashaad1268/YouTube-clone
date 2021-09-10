from django.shortcuts import (render, redirect, get_object_or_404)
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.core.mail import EmailMessage, send_mail
from django.template.loader import get_template
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required

# Local imports
from django.conf import settings
from .models import Video, Like, Subscribe, Channel, CreatorProfile, Comment
from .form import VideoUploadForm, VideoEditForm, ContactForm, CommentForm
from .filters import VideoFilter


def home_page(request):
    """Public videos will be displayed here."""
    videos = Video.objects.filter(is_public=True).order_by('-id')
    video_filter = VideoFilter(request.GET, queryset=videos)
    videos = video_filter.qs
    return render(request, "home.html", {"videos": videos, "video_filter": video_filter})


@login_required(login_url='login')
def video_upload_view(request):
    form = VideoUploadForm(initial={'is_public':True})

    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.creator = request.user
            video = form.save(commit=False)
            video.creator = request.user
            video.save()
            messages.success(request, 'Successfully uploaded video')
            return redirect("home")

    return render(request, "video_upload.html", {"form": form})


def video_watch_view(request, video_id, video_title):
    video = Video.objects.get(pk=video_id)
    # creator, created = CreatorProfile.objects.get_or_create(creator=video.creator)
    creator = CreatorProfile.objects.get(creator=video.creator)
    video_comments = Comment.objects.filter(video=video)
    channel = Channel.objects.get(owner=creator)
    comment_form = CommentForm()
    
    if video.is_public:
        video.views += 1
        video.save()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment_form.video = video
            comment_form.commentator = request.user
            comment = comment_form.save(commit=False)
            comment.video = video
            comment.commentator = request.user
            comment.save()

    return render(request, "video_watch_view.html", {"video": video, "channel": channel, "comments": video_comments, "comment_form": comment_form})


@login_required(login_url='login')
def video_edit_view(request, video_id, video_title):
    video_obj = Video.objects.get(pk=video_id)
    form = VideoEditForm(instance=video_obj)

    if not request.user.is_staff and not request.user == video_obj.creator:
        return redirect("home")

    if not request.user.is_authenticated:
        return redirect("home")

    if request.method == 'POST':
        form = VideoEditForm(request.POST, request.FILES, instance=video_obj)
        if form.is_valid():
            form.save() 
            return redirect('watch', video_obj.id, video_obj.title.replace(" ", "-"))
            messages.success(request, 'Successfully updated video info')

    
    return render(request, "video_edit_view.html", {"form": form, "video": video_obj})


@login_required(login_url='login')
def video_delete_view(request, video_id, video_title): 
    # fetch the object related to passed id
    obj = Video.objects.get(pk=video_id)

    if not request.user.is_staff and not request.user == obj.creator:
        return redirect("home")

    if not request.user.is_authenticated:
        return redirect("home")


    if request.method =="POST":
        # delete the object
        obj.delete()
        messages.success(request, 'Successfully deleted video')
        return redirect("home")
  
    return render(request, "video_delete_view.html", {"video":obj})


def channel_view(request, channel_id):
    channel = Channel.objects.get(pk=channel_id)
    video_creator = User.objects.get(creatorprofile=channel.owner)
    videos = Video.objects.filter(creator=video_creator, is_public=True)

    return render(request, "channel_view.html", {"channel":channel, "videos": videos})



@login_required(login_url='login')
def private_videos(request):
    videos = Video.objects.filter(is_public=False)

    return render(request, "private_video_view.html", {"videos": videos})


@login_required(login_url='login')
def comment_delete_view(request, comment_id): 
    context = {}
    # fetch the object related to passed id
    obj = Comment.objects.get(pk=comment_id)
    context['comment'] = obj

    if not request.user.is_staff and not request.user == obj.creator:
        return redirect("home")

    if request.method =="POST":
        # delete the object
        obj.delete()
        messages.success(request, 'Successfully deleted comment')
        return redirect("home")
  
    return render(request, "comment_delete_view.html", context)




def contact_view(request):
    form = ContactForm()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_name = form.cleaned_data.get('contact_name')
            contact_email = form.cleaned_data.get('contact_email')
            form_content = form.cleaned_data.get('content')

            template = get_template('contact_template.txt')
            
            context = {
                'contact_name': contact_name,
                'contact_email': contact_email,
                'form_content': form_content,
            }

            content = template.render(context)
            
            email = EmailMessage(
                subject=f"New contact form submission by {context['contact_name']}",
                body=f"{content}\n(Sent from your YouTube clone web site)",
                from_email=context['contact_email'],
                to=['rashaadzma@gmail.com'],
                headers = {"Reply to": context['contact_email']}
            )

            email.send(fail_silently=False)

            return render(request, "email_success.html", {})

    return render(request, "contact_view.html", {"form":form})


def like_view(request):
    user = request.user

    if request.method == 'GET':
        return redirect('home')

    if request.method == 'POST':
        video_id = request.POST.get('video_id')
        video_obj = Video.objects.get(pk=video_id)

        if user in video_obj.likes.all():
            video_obj.likes.remove(user)

        else:
            video_obj.likes.add(user)

        like, created = Like.objects.get_or_create(user=user, video_id=video_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            
            else:
                like.value = 'Like'

            like.save()
            video_obj.save()

        data = {
        'value': like.value,
        'likes': video_obj.total_likes
        }
    
        return JsonResponse(data, safe=False)


def subscribe_view(request):
    user = request.user

    if not request.method == 'POST':
        return redirect('home')

    if request.method == 'POST':
        channel_id = request.POST.get('channel_id')
        channel_obj = Channel.objects.get(pk=channel_id)

        if user in channel_obj.subscriber.all():
            channel_obj.subscriber.remove(user)

        else:
            channel_obj.subscriber.add(user)

        subscribe, created = Subscribe.objects.get_or_create(subscriber=user, channel_id=channel_id)

        if not created:
            if subscribe.value == 'Like':
                subscribe.value = 'Unlike'
            
            else:
                subscribe.value = 'Like'

            subscribe.save()
            channel_obj.save()

        data = {
        'value': subscribe.value,
        'subscribers': channel_obj.total_subscribers
        }
    
        return JsonResponse(data, safe=False)
