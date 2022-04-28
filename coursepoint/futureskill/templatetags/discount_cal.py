from tkinter.tix import Tree
from django import template
from matplotlib.pyplot import disconnect

from futureskill.models import userCourse, registration


register = template.Library()


@register.simple_tag
def fnl_discount(price, discount):

    if discount is None or discount is 0:
        return price

    sp = price
    sp = sp - (sp * discount * 0.01)
    return int(sp)


@register.simple_tag
def is_enroll(request, course):

    user = None
    try:
        if not request.session['name']:
            return False
    except:
        return False

    user = registration.objects.get(email=request.session['email'])

    try:
        user_course = userCourse.objects.get(user=user, course=course)
        return True
    except:
        return False
