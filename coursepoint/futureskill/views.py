from django.http import HttpResponse
from django.shortcuts import redirect, render
import razorpay
from time import time
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import routers, serializers, viewsets
# Create your views here.
from .serializers import UserSerializer
from coursepoint.settings import *
client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))


def index(request):
    # print("8888888888888888888888888888", request.session.get('name'))
    course = coursedtls.objects.all()

    return render(request, 'home.html', {'course_info': course})


def signup(request):
    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email_id = request.POST.get("email")
        password = request.POST.get("password")
        mobile = request.POST.get("mobile")
        gender = request.POST.get("gender")
        fetch = registration.objects.filter(email=email_id)
        if fetch:
            return HttpResponse("email already exsits")
        else:
            user_info = registration(first_name=fname, last_name=lname,
                                     email=email_id, password=make_password(password), mobile=mobile, gender=gender)

            user_info.save()

    return redirect('home')


def login(request):
    err_message = None
    if request.method == "POST":

        email_id = request.POST.get('email')
        password = request.POST.get('password')
        print(email_id)
        print(password)
        try:
            fetch_info = registration.objects.get(email=email_id)
            if (fetch_info.email == email_id):
                if check_password(password, fetch_info.password):
                    print("---------------------")
                    request.session['name'] = fetch_info.first_name
                    request.session['email'] = fetch_info.email
                    # return HttpResponse("your email and password are correct")
                    return redirect('home')
                else:
                    print("###########################")
                    err_message = "please enter valid passsword"
                    print(err_message)
                    return render(request, 'home.html', {'err_message': err_message})

        except:

            print("##############################################")
            err_message = "Please Enter valid Email"
            return render(request, 'home.html', {'err_message': err_message})

            return redirect("home")


def logout(request):
    request.session.clear()
    return redirect('home')


def course_informations(request, slug):

    fetch_dtls = coursedtls.objects.get(slug=slug)
    # auth = registration.objects.get()
    s_no = request.GET.get('serial_no')

    if s_no is None:
        s_no = 1
    try:
        video = Videos.objects.get(course=fetch_dtls, s_no=s_no)
        if video.is_preview is False:
            if request.session.get('name') is None:
                return redirect('home')
            else:
                user_id = registration.objects.get(
                    email=request.session['email'])
                print(user_id)
                try:
                    user_course = userCourse.objects.get(
                        user=user_id, course=fetch_dtls)
                except:
                    return redirect('checkout', slug=fetch_dtls.slug)

    except:
        return redirect('home')

    return render(request, 'course_dtls.html', {'co_dtls': fetch_dtls, 'video': video})


def checkout(request, slug):

    course = coursedtls.objects.get(slug=slug)
    if request.session.get('email') is None:
        return HttpResponse("please login")
    else:
        user_id = registration.objects.get(email=request.session['email'])

    order = None
    amount = None
    order_ids = None
    payment = None
    # if amount == 0:
    error = None

    action = request.GET.get('action')
    coupon_code = request.GET.get('couponcode')
    cpn_code_msg = None
    coup = None
    if error is None:
        amount = int(
            (course.price - (course.price * course.discount * 0.01)) * 100)
    if coupon_code:
        try:
            coup = RefCode.objects.get(course=course, code=coupon_code)
            amount = int(
                (course.price - (course.price * coup.discount * 0.01)) * 100)

        except:
            cpn_code_msg = "invalid code"

    if action == 'create_payment':

        try:
            user_course = userCourse.objects.get(user=user_id, course=course)
            error = "you have already purchase this course"
        except:
            pass

        if error is None:
            currency = "INR"
            receipt = f'courspoint-{int(time())}'
            notes = {
                'user': user_id.first_name,
                'email': user_id.email
            }
            order = client.order.create(
                {
                    'currency': currency,
                    'receipt': receipt,
                    'notes': notes,
                    'amount': amount
                }
            )

            order_ids = order.get('id')
            payment = Payment()
            payment.order_id = order_ids
            payment.user_info = user_id
            payment.course = course
            payment.save()

    if coupon_code == "":
        cpn_code_msg = "invalid code"

    context = {
        'order': order,
        'course': course,
        'user': user_id,
        'order_id': order_ids,
        "error": error,
        'coup': coup,
        "cpn_code_msg": cpn_code_msg

    }

    return render(request, 'checkout_info.html', context=context)


@csrf_exempt
def verify_payment(request):
    if request.method == 'POST':
        data = request.POST
        client.utility.verify_payment_signature(data)
        razorpay_payment_id = data['razorpay_payment_id']
        razorpay_order_id = data['razorpay_order_id']

        payment = Payment.objects.get(order_id=razorpay_order_id)
        payment.payment_id = razorpay_payment_id
        payment.status = True

        usercourse = userCourse(user=payment.user_info, course=payment.course)
        usercourse.save()

        payment.user_course = usercourse

        payment.save()

        try:
            return redirect('my_course')
        except:
            return HttpResponse("successfull")


def mycourse(request):

    user_id = registration.objects.get(email=request.session['email'])

    user_course = userCourse.objects.filter(user=user_id)
    context = {
        'user_course': user_course
    }

    return render(request, 'mycourse.html', context=context)


class UserViewSet(viewsets.ModelViewSet):
    queryset = registration.objects.all()
    serializer_class = UserSerializer
