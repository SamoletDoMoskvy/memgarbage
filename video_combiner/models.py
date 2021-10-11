from django.db import models


# TODO добавить модели для видео, которые уже были скомбинированы

class Combined(models.Model):
    name = models.CharField(max_length=50)
    already_yt_used = models.BooleanField(default=False)
    already_tt_used = models.BooleanField(default=False)
    already_a1_used = models.BooleanField(default=False)
    already_a2_used = models.BooleanField(default=False)
    already_a2_used = models.BooleanField(default=False)
    dt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
