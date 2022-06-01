from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy

from django.contrib.auth import get_user_model

from .forms import ImageForm

import urllib
import numpy as np
from script.hand_image_detector import hand_detection
import cv2

from mysite.camera import VideoCamera, gen
from django.http import StreamingHttpResponse, JsonResponse

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import UserForm

import sqlite3
from .models import Tutorial


class Home(TemplateView):
    template_name = 'home.html'


def image_upload_view(request):
    """Process images uploaded by users"""
    data = {"success": False}
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if request.FILES.get("image", None) is not None:
            image = _grab_image(stream=request.FILES["image"])
            # call the detection here
            annotated_image = hand_detection(image)
            # open cv window once it is done, to show the output image
            # alternatively one can put it in the html
            cv2.imshow("output", annotated_image)
            cv2.waitKey(0)

            form.save()
            img_obj = form.instance
            return render(request, 'image_upload.html', {'form': form, 'img_obj': img_obj})
    else:
        form = ImageForm()
    return render(request, 'image_upload.html', {'form': form})


# a helper function to convert img.url into a cv.img object
# for image upload and detection only
def _grab_image(path=None, stream=None, url=None):
    if path is not None:
        image = cv2.imread(path)
    else:
        if url is not None:
            resp = urllib.urlopen(url)
            data = resp.read()
        elif stream is not None:
            data = stream.read()
        # convert the image to a NumPy array and then read it into
        # OpenCV format
        image = np.asarray(bytearray(data), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    # return the image
    return image


# for video input and detection
# the whole thing, video
# is returned as a streaming http response, or bytes
def video_stream1(request):
    userMODEL = get_user_model().objects.get(username=request.user.username)
    print(userMODEL)

    Tutorial.objects.filter(NAME=userMODEL).update(STEP1=0, STEP2=0, STEP3=0, STEP4=0)

    videoCamera = VideoCamera(userMODEL)
    videoCamera.select_mode(0)
    vid = StreamingHttpResponse(gen(videoCamera, False),
                                content_type='multipart/x-mixed-replace; boundary=frame')
    return vid


def video_stream2(request):
    userMODEL = get_user_model().objects.get(username=request.user.username)
    videoCamera = VideoCamera(userMODEL)
    videoCamera.select_mode(1)
    vid = StreamingHttpResponse(gen(videoCamera, False),
                                content_type='multipart/x-mixed-replace; boundary=frame')
    return vid


def video_stream3(request):
    userMODEL = get_user_model().objects.get(username=request.user.username)
    videoCamera = VideoCamera(userMODEL)
    videoCamera.select_mode(2)
    vid = StreamingHttpResponse(gen(videoCamera, False),
                                content_type='multipart/x-mixed-replace; boundary=frame')
    return vid


def video_stream4(request):
    userMODEL = get_user_model().objects.get(username=request.user.username)
    videoCamera = VideoCamera(userMODEL)
    videoCamera.select_mode(3)
    vid = StreamingHttpResponse(gen(videoCamera, False),
                                content_type='multipart/x-mixed-replace; boundary=frame')
    return vid


def video_save(request):
    vid = StreamingHttpResponse(gen(VideoCamera(), True),
                                content_type='multipart/x-mixed-replace; boundary=frame')
    return vid


def video_input(request):
    return render(request, 'video_input.html')


@csrf_exempt
def refresh_step1(request, username):
    userMODEL = get_user_model().objects.get(username=request.user.username)

    object = get_object_or_404(get_user_model(), username=userMODEL.username)

    print(userMODEL)

    tutorial = Tutorial.objects.get(NAME=userMODEL)
    print(tutorial)

    true = 'True'
    false = 'False'

    if tutorial.STEP1 == 1:
        step1 = true
    else:
        step1 = false

    if tutorial.STEP2 == 1:
        step2 = true
    else:
        step2 = false

    if tutorial.STEP3 == 1:
        step3 = true
    else:
        step3 = false

    if tutorial.STEP4 == 1:
        step4 = true
    else:
        step4 = false

    print(step1)
    context = {'step1': step1,
               'step2': step2,
               'step3': step3,
               'step4': step4
               }

    return JsonResponse(context)


def video_input01(request):
    return render(request, 'video_input01.html')


def video_input02(request):
    return render(request, 'video_input02.html')


def video_input03(request):
    return render(request, 'video_input03.html')


def guide(request):
    return render(request, 'guide.html')


def signup(request):
    con = sqlite3.connect('./db.sqlite3', check_same_thread=False)
    cur = con.cursor()

    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인

            userMODEL = get_user_model().objects.get(username=username)
            print(userMODEL)
            tutorial = Tutorial(NAME=userMODEL, STEP1=0, STEP2=0, STEP3=0, STEP4=0)
            tutorial.save()

            rows = Tutorial.objects.get(NAME=userMODEL)
            print(rows.NAME, rows.STEP1, rows.STEP2, rows.STEP3, rows.STEP4)

            return redirect('/guide')
    else:
        form = UserForm()
    return render(request, 'signup.html', {'form': form})
