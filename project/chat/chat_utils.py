from project.models import Chat
from django.db.models import Max, QuerySet
from django.db.models import Q

def get_last_chats(user_id):
    sended_messages = Chat.objects.filter(sender_user__id = user_id)\
                            .values('receiver_user__id').annotate(max_date=Max('Date'))\
                            .order_by("-max_date")
    received_messages = Chat.objects.filter(receiver_user__id = user_id)\
                        .values('sender_user__id').annotate(max_date=Max('Date'))\
                        .order_by("-max_date")
    messages = dict()
    for dic in sended_messages:
        messages[dic['receiver_user__id']] = (dic['max_date'],'send')
        
    for dic in received_messages:
        sender_id = dic['sender_user__id']
        if sender_id in messages:
            if dic['max_date'] > messages[sender_id][0]:
                messages[sender_id] = (dic['max_date'],'recv')
        else:
            messages[sender_id] = (dic['max_date'],'recv')
    
    message = Chat.objects.none()
    for (user_id_2,(date,mode)) in messages.items():
        if mode == 'send':
            message |= Chat.objects.filter(sender_user__id = user_id,receiver_user__id = user_id_2, Date = date)
        else:
            message |= Chat.objects.filter(receiver_user__id = user_id,sender_user__id = user_id_2, Date = date)
    
    return message

def get_users_chats(user_id1, user_id2):
    q = (Q(sender_user__id = user_id1) & Q(receiver_user__id=user_id2)) |\
        (Q(receiver_user__id = user_id1) & Q(sender_user__id=user_id2))
    qs = Chat.objects.filter(q)
    return qs.order_by('-Date')