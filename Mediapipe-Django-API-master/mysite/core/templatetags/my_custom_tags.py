from mysite.camera import VideoCamera
from django import template

register = template.Library()


@register.simple_tag
def my_tag():
    vc = VideoCamera()


    return str(vc.time_checker())
