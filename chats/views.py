# chat/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer

User = get_user_model()


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    # Создание нового чата между двумя участниками
    @action(detail=False, methods=['post'])
    def create_chat(self, request):
        user1 = request.user
        user2_id = request.data.get('user2_id')
        user2 = User.objects.get(id=user2_id)

        if user1 == user2:
            return Response({"error": "You cannot create a chat with yourself."}, status=status.HTTP_400_BAD_REQUEST)

        # Проверим, существует ли уже чат между этими пользователями
        chat = Chat.objects.filter(participants=user1).filter(participants=user2).first()

        if not chat:
            chat = Chat.objects.create()
            chat.participants.add(user1, user2)

        serializer = self.get_serializer(chat)
        return Response(serializer.data)

    # Получение всех чатов пользователя
    @action(detail=False, methods=['get'])
    def my_chats(self, request):
        chats = Chat.objects.filter(participants=request.user)
        serializer = self.get_serializer(chats, many=True)
        return Response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    # Отправка нового сообщения
    @action(detail=False, methods=['post'])
    def send_message(self, request):
        sender = request.user
        chat_id = request.data.get('chat_id')
        text = request.data.get('text')

        chat = Chat.objects.get(id=chat_id)

        # Проверяем, что пользователь является участником чата
        if sender not in chat.participants.all():
            return Response({"error": "You are not a participant of this chat."}, status=status.HTTP_403_FORBIDDEN)

        message = Message.objects.create(chat=chat, sender=sender, text=text)
        serializer = self.get_serializer(message)
        return Response(serializer.data)

    # Помечаем сообщение как прочитанное
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        message = self.get_object()
        if request.user in message.chat.participants.all():
            message.is_read = True
            message.save()
            return Response({"message": "Message marked as read."})
        return Response({"error": "You are not a participant of this chat."}, status=status.HTTP_403_FORBIDDEN)
