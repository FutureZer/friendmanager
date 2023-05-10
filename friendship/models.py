from django.db import models


class FriendRequest(models.Model):
    from_user = models.IntegerField('Отправитель')
    to_user = models.IntegerField('Получатель')


class FriendWith(models.Model):
    user1 = models.IntegerField()
    user2 = models.IntegerField()
