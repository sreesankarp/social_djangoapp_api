from django.shortcuts import render
from django.contrib.auth.models import User,auth
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import FriendRequests
from .serializers import FriendRequestsSerializer,UserSerializer
import re
import datetime
from django.conf import settings


def validateEmail(email):
    pattern = r'[^a-zA-Z0-9.@]'
    try:
        validate_email(email)
        matches = re.findall(pattern, email)
        if not matches:
            return True
        else:
            raise ValidationError("Invalid email format")
    except ValidationError:
        return False

@api_view(['POST'])
def user_signup(request):
    password = request.POST.get('password')
    email = request.POST.get('email')
    name = request.POST.get('name')
    print([password,email,name],None in [password,email,name])
    if not None in [password,email,name]:
        if validateEmail(email):
            email = email.lower()
            if User.objects.filter(email=email).exists():
                return JsonResponse({'message':'Email already exists, user creation failed!','status':'error'})
            else:
                user = User.objects.create_user(username=name,email=email, password=password)
                user.save()
                return JsonResponse({'message':'User created successfully!','status':'success'})
        else:
            return JsonResponse({'message':'Invalid email address, please enter correct email!','status':'error'})
    else:
        return JsonResponse({'message':'Name, Email and Password are mandatory, please check if you have supplied all fields!','status':'error'})
        
@api_view(['POST'])
def user_login(request):
    
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            return JsonResponse({'message':'Login successfull!','status':'success'})

        else:
            return JsonResponse({'message':'Invalid Email/Password, Please try again!','status':'error'})


@api_view(['POST'])
@login_required(login_url='userstatus')
def user_logout(request):
    auth.logout(request)
    return JsonResponse({'message':'User signed out!','status':'success'})
    
        
def user_status(request):
    if not request.user.is_authenticated:
        return JsonResponse({'message':'No active sessions found!','status':'error'})

@api_view(['POST'])
@login_required(login_url="userstatus")
def search_user(request):
    if request.method == 'POST':
        search_query= request.POST.get("query")
        current_user = request.user.email
        page= int(request.POST.get("page"))
        if search_query and page:
            matches = {}
            for user in User.objects.filter(username__icontains=search_query):
                if user.username[:len(search_query)] == search_query:
                    matches[user.email] = user.username

            for user in User.objects.filter(email__icontains=search_query):
                if user.email[:len(search_query)] == search_query:
                    matches[user.email] = user.username

            if current_user in matches:
                del matches[current_user]

            if matches:
                page_result_limit = settings.SEARCH_RESULTS_PER_PAGE
                total_results = len(matches)
                total_pages = (-(-total_results//page_result_limit))
                start_index = (total_results//page) - 1
                paged_results = [*matches.items()][start_index:start_index+page_result_limit]
                return JsonResponse({'message':'Found match!','result':paged_results,"totalPages":total_pages,"totalResults":total_results,'status':'success'})
            else:
                return JsonResponse({'message':'No match found!','status':'success'})
        else:
            return JsonResponse({'message':'Search string and page number are mandatory!','status':'error'})

@api_view(['POST'])
@login_required(login_url="userstatus")
def send_friend_request(request):
    from_user = request.user
    to_email = request.POST.get("email")
    current_user = request.user.email
    if current_user!=to_email:
        to_user = User.objects.get(email=to_email)
        minute_diff = datetime.datetime.now() - datetime.timedelta(minutes=1)
        requests_last_min = FriendRequests.objects.filter(created_at__gte=minute_diff).count()
        
        if FriendRequests.objects.filter(from_user=from_user, to_user=to_user, status='pending').exists():
            return JsonResponse({'message':'Request pending,cannot send new request!','status':'error'})
        
        if requests_last_min<3:
            friend_request = FriendRequests.objects.create(from_user=from_user, to_user=to_user)
            serializer = FriendRequestsSerializer(friend_request)
            return JsonResponse({'message':'Request sent!',"action":serializer.data,'status':'success'})
        else:
            return JsonResponse({'message':'Limit reached, you can only send 3 requests per minute!','status':'success'})
    else:
        return JsonResponse({'message':'You cant send request to yourself!','status':'error'})


@api_view(['POST'])
@login_required(login_url="userstatus")
def accept_friend_request(request):
    to_email = request.POST.get("email")
    to_user = User.objects.get(email=to_email)
    friend_request = FriendRequests.objects.get(from_user=to_user, to_user=request.user, status='pending')
    friend_request.status = 'accepted'
    friend_request.save()
    serializer = FriendRequestsSerializer(friend_request)
    return JsonResponse({'message':'Request accepted!',"action":serializer.data,'status':'success'})

@api_view(['POST'])
@login_required(login_url="userstatus")
def reject_friend_request(request):
    to_email = request.POST.get("email")
    to_user = User.objects.get(email=to_email)
    friend_request = FriendRequests.objects.get(from_user=to_user, to_user=request.user, status='pending')
    friend_request.status = 'rejected'
    friend_request.save()
    return JsonResponse({'message':'Request rejected!','status':'success'})

@api_view(['GET'])
@login_required(login_url="userstatus")
def list_pending_requests(request):
    user = request.user
    pending_requests = FriendRequests.objects.filter(to_user=user, status='pending')
    serializer = FriendRequestsSerializer(pending_requests, many=True)
    return JsonResponse({'message':'Pending requests!','action':serializer.data,'status':'success'})


@api_view(['GET'])
@login_required(login_url="userstatus")
def list_friends(request):
    user = request.user
    friends = User.objects.filter(sent_requests__to_user=user, sent_requests__status='accepted') | \
              User.objects.filter(received_requests__from_user=user, received_requests__status='accepted')
    serializer = UserSerializer(friends, many=True)
    return JsonResponse({'message':'Friends!',"action":serializer.data,'status':'success'})