from django.db      import models

from core.models    import TimeStampModel


class Board(TimeStampModel):
    title               = models.CharField(max_length=100)
    description         = models.TextField()
    board_image_url     = models.URLField(max_length=2000)
    source              = models.CharField(max_length=50)
    image_point_color   = models.CharField(max_length=50)
    image_width         = models.PositiveIntegerField()
    image_height        = models.PositiveIntegerField()
    user                = models.ForeignKey('users.User', on_delete=models.CASCADE)
    commented_users     = models.ManyToManyField('users.User', through="Comment", related_name="boards", null=True, blank=True)
    tags                = models.ManyToManyField('Tag', through="TagBoard", related_name="boards", null=True, blank=True)

    class Meta:
        db_table = 'boards'


class Tag(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'tags'


class TagBoard(TimeStampModel):
    board = models.ForeignKey('Board', on_delete=models.CASCADE)
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE)

    class Meta:
        db_table = 'tag_boards'


class PinBoard(TimeStampModel):
    user  = models.ForeignKey('users.User', on_delete=models.CASCADE)
    board = models.ForeignKey('Board', on_delete=models.CASCADE)

    class Meta:
        db_table = 'pin_boards'


class Comment(TimeStampModel):
    user        = models.ForeignKey('users.User', on_delete=models.CASCADE)
    board       = models.ForeignKey('Board', on_delete=models.CASCADE)
    description = models.TextField()

    class Meta:
        db_table = 'comments'