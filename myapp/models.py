# coding=utf-8
from django.contrib.auth.models import User
from django.db import models


class Message(models.Model):
    message = models.TextField(verbose_name='Сообщение')
    date = models.DateTimeField(verbose_name='Дата отправления', auto_now_add=True)
    sender = models.ForeignKey(User)

    class Meta:
        db_table = 'messages'
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['date']

    def __unicode__(self):
        return self.message


    def messages(self, after_pk=None):
        m = Message.objects.all()
        if after_pk:
            m = m.filter(pk__gt=after_pk)
        return m.order_by('pk')
