from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy

from .forms import  ImageForm

import urllib
import numpy as np
from script.hand_image_detector import hand_detection
import cv2

from mysite.camera import VideoCamera, gen
from django.http import StreamingHttpResponse

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import UserForm


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
def video_stream(request):
    videoCamera = VideoCamera()
    vid = StreamingHttpResponse(gen(videoCamera, False),
    content_type='multipart/x-mixed-replace; boundary=frame')
    return vid

def video_save(request):
    vid = StreamingHttpResponse(gen(VideoCamera(), True), 
    content_type='multipart/x-mixed-replace; boundary=frame')
    return vid

def video_input(request):
    return render(request, 'video_input.html')

def video_input01(request):
    return render(request, 'video_input01.html')

def video_input02(request):
    return render(request, 'video_input02.html')

def video_input03(request):
    return render(request, 'video_input03.html')

def guide(request):
    return render(request, 'guide.html')

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            return redirect('/guide')
    else:
        form = UserForm()
    return render(request, 'signup.html', {'form': form})

