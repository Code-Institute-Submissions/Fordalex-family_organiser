from django.shortcuts import render
from user.models import Friend
from .models import Message, MessageNotification
from django.contrib.auth.models import User
from user.models import UserProfile
from django.db.models import Q

# Create your views here.
def new_conversation(request):

    if request.method == 'GET':

        try:

            query = request.GET['q']
            queries = Q(username__startswith=query) | Q(first_name__startswith=query) | Q(last_name__startswith=query) | Q(username__startswith=query.capitalize()) | Q(first_name__startswith=query.capitalize()) | Q(last_name__startswith=query.capitalize())
            users_friends = Friend.objects.get(current_user=request.user)
            all_users = users_friends.users.filter(queries)

            searched_users = []
            for one_user in all_users:
                user_profile = UserProfile.objects.get(user=one_user)

                user_dict = {
                    'first_name': one_user.first_name,
                    'last_name': one_user.last_name,
                    'username': one_user.username,
                    'id': one_user.id,
                    'user_profile': {
                        'profile_image': user_profile.profile_image,
                    }
                }
                searched_users.append(user_dict)
        except:
            searched_users = []
        
    try:
        friends = Friend.objects.get(current_user=request.user)
        all_friends_query_set = friends.users.all()
        all_friends = []
        for friend in all_friends_query_set:
            all_friends.append(friend.username)
    except:
        all_friends = []

    try:
        friend_requests = FriendRequests.objects.filter(from_user=request.user)
        friend_request_sent = []
        for friend_request in friend_requests:
            friend_request_sent.append(friend_request.to_user.username)
    except:
        friend_request_sent = []

    context = {
        'searched_users': searched_users,
        'friends': all_friends,
        'friend_request_sent': friend_request_sent,
    }

    return render(request, 'message/new_conversation.html', context)

def select_conversation(request):
    """
    Continue a coversation that has already been started.
    """
    # If user isn't logged in return to the home page.
    if request.user.is_anonymous:
        return redirect('home')

    conversations_from = Message.objects.filter(sent_from=request.user)
    conversations_to = Message.objects.filter(sent_to=request.user)
    current_conversations_with_users = []

    for conversation in conversations_from:
        print(conversation, conversation.sent_from)
        current_conversations_with_users.append(conversation.sent_to)

    for conversation in conversations_to:
        print(conversation, conversation.sent_from)
        current_conversations_with_users.append(conversation.sent_from)

    current_conversations = []

    for index, conversation in enumerate(current_conversations_with_users):
        if index == 0:
            current_conversations.append(conversation)
        else:
            new_conversation = True
            for list_item in current_conversations:
                if list_item == conversation:
                    new_conversation = False
            if new_conversation:
                current_conversations.append(conversation)

    new_message_conversation = MessageNotification.objects.filter(user=request.user)



    context = {
        'conversations': current_conversations,
        'new_message_conversation': new_message_conversation,
    }

    return render(request, 'message/select_conversation.html', context)

def conversation(request, pk):
    """
    Conversation page where users will see all their message between themself and the recipient,
    and be able to send new messages.
    """
    # If user isn't logged in return to the home page.
    if request.user.is_anonymous:
        return redirect('home')

    message_user = User.objects.get(pk=pk)

    notifications_from_recipient = MessageNotification.objects.filter(sent_from=pk)
    for notifications in notifications_from_recipient:
        notifications.delete()

    if request.method == 'POST':
        users_message = request.POST.get('message')

        new_message = Message(
            message = users_message,
            sent_from = request.user,
            sent_to = message_user,
        )
        new_message.save()

        message_notification = MessageNotification(
            user = message_user,
            sent_from = request.user,
            notifications = 1,
        )
        message_notification.save()

    messages_from_recipient = Message.objects.filter(sent_from=message_user, sent_to=request.user)
    message_from_current_user = Message.objects.filter(sent_to=message_user, sent_from=request.user)
    
    conversation_messages = []

    for message in messages_from_recipient:
        conversation_messages.append(message)

    for message in message_from_current_user:
        conversation_messages.append(message)

    conversation_messages = sorted(conversation_messages, key = lambda x: x.created_date)

    context = {
        'message_user': message_user,
        'messages': conversation_messages,
    }

    return render(request, 'message/conversation.html', context)