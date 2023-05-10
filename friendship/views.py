from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import ViewUserForm, SearchUserForm
from .models import FriendRequest, FriendWith


def home(request):
    search_form = SearchUserForm()
    message = ''
    current_auth = request.user
    if request.method == 'GET':
        forms = list()
        if len(request.GET) == 0:
            for user in User.objects.all():
                if user != current_auth and not is_request_sent(current_auth.id, user.id)\
                        and not is_friends(current_auth.id, user.id):
                    forms.append(ViewUserForm(instance=user))
        else:
            try:
                user = User.objects.get(username=request.GET['username'])
                forms.append(ViewUserForm(instance=user))
            except:
                pass
        if len(forms) == 0:
            message = 'Пользователей не найдено'
        data = {
            'search_form': search_form,
            'message': message,
            'forms': forms
        }
        return render(request, 'friendship/home.html', data)
    if request.method == 'POST':
        form = ViewUserForm(request.POST)
        target_user = User.objects.get(username=form.data['username'])
        friend_request = FriendRequest(from_user=current_auth.id, to_user=target_user.id)
        if is_request_sent(target_user.id, current_auth.id):
            sent_request = FriendRequest.objects.get(from_user=target_user.id, to_user=current_auth.id)
            sent_request.delete()
            friendship = make_friends(target_user, current_auth)
            friendship.save()
            return redirect('home')
        if not is_request_sent(current_auth.id, target_user.id):
            friend_request.save()
        return redirect('home')


def sent_requests(request):
    current_auth = request.user
    message = ''
    if request.method == 'GET':
        forms = list()
        users = get_requested_users(current_auth.id)
        for user in users:
            forms.append(ViewUserForm(instance=user))
        if len(users) == 0:
            message = 'У вас пока что нет друзей. Добавьте их на главной странице'
        data = {
            'message': message,
            'forms': forms
        }
        return render(request, 'friendship/myrequests.html', data)
    if request.method == 'POST':
        form = ViewUserForm(request.POST)
        target_user = User.objects.get(username=form.data['username'])
        myrequest = FriendRequest.objects.get(from_user=current_auth.id, to_user=target_user.id)
        myrequest.delete()
        return redirect('myrequests')


def received_requests(request):
    current_auth = request.user
    message = ''
    if request.method == 'GET':
        forms = list()
        users = get_friendship_senders(current_auth.id)
        for user in users:
            forms.append(ViewUserForm(instance=user))
        if len(users) == 0:
            message = 'Никто не отправил вам заявку в друзья'
        data = {
            'message': message,
            'forms': forms
        }
        return render(request, 'friendship/receivedrequests.html', data)
    if request.method == 'POST':
        form = ViewUserForm(request.POST)
        sender_user = User.objects.get(username=form.data['username'])
        send_request = FriendRequest.objects.get(from_user=sender_user.id, to_user=current_auth.id)
        if request.POST.get('accept'):
            friendship = make_friends(sender_user, current_auth)
            friendship.save()
        send_request.delete()
        return redirect('received')


def friend_list(request):
    current_auth = request.user
    message = ''
    if request.method == 'GET':
        forms = list()
        users = User.objects.all()
        for user in users:
            if is_friends(current_auth.id, user.id):
                forms.append(ViewUserForm(instance=user))
        if len(forms) == 0:
            message = 'У вас нет друзей. Добавьте кого-нибудь на главной странице'
        data = {
            'message': message,
            'forms': forms
        }
        return render(request, 'friendship/friendlist.html', data)
    if request.method == 'POST':
        form = ViewUserForm(request.POST)
        target_user = User.objects.get(username=form.data['username'])
        if current_auth.id < target_user.id:
            friendship = FriendWith.objects.get(user1=current_auth.id, user2=target_user.id)
        else:
            friendship = FriendWith.objects.get(user1=target_user.id, user2=current_auth.id)
        friendship.delete()
        FriendRequest(from_user=target_user.id, to_user=current_auth.id).save()
        return redirect('friends')


def make_friends(user1, user2):
    if user1.id < user2.id:
        return FriendWith(user1=user1.id, user2=user2.id)
    else:
        return FriendWith(user1=user2.id, user2=user1.id)


def is_request_sent(sender_id, receiver_id):
    result = FriendRequest.objects.filter(from_user=sender_id, to_user=receiver_id).count()
    return result > 0


def get_requested_users(sender_id):
    current_requests = FriendRequest.objects.filter(from_user=sender_id)
    users = list()
    for req in current_requests:
        users.append(User.objects.get(id=req.to_user))
    return users


def get_friendship_senders(sender_id):
    current_requests = FriendRequest.objects.filter(to_user=sender_id)
    users = list()
    for req in current_requests:
        users.append(User.objects.get(id=req.from_user))
    return users


def is_friends(user1_id, user2_id):
    count1 = FriendWith.objects.filter(user1=user1_id, user2=user2_id).count()
    count2 = FriendWith.objects.filter(user1=user2_id, user2=user1_id).count()
    return count1 + count2 > 0
