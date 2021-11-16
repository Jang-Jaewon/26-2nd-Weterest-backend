from django.db      import models
from core.models    import TimeStampModel


class User(TimeStampModel):
    email               = models.EmailField(max_length=254, unique=True)
    password            = models.CharField(max_length=300, null=True)
    nickname            = models.CharField(max_length=30, unique=True)
    profile_image_url   = models.URLField(max_length=2000, null=True)
    login_platform      = models.CharField(max_length=30)
    description         = models.TextField(null=True)
    pined_boards        = models.ManyToManyField('boards.Board', through="boards.PinBoard", related_name="users", null=True, blank=True)
    
    class Meta:
        db_table = 'users'