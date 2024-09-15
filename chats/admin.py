# chat/admin.py

from django.contrib import admin
from .models import Chat, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 1  # Показывает поле для добавления сообщения

class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_participants', 'created_at')
    inlines = [MessageInline]

    def get_participants(self, obj):
        return ", ".join([user.username for user in obj.participants.all()])
    get_participants.short_description = 'Participants'


class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat', 'sender', 'text', 'timestamp', 'is_read')
    list_filter = ('is_read', 'timestamp')
    search_fields = ('text', 'sender__username', 'chat__id')

admin.site.register(Chat, ChatAdmin)
admin.site.register(Message, MessageAdmin)
