from django.db import models


class Combined(models.Model):
    dt_name = models.DateTimeField(auto_now_add=True)
    already_yt_used = models.BooleanField(default=False)
    already_tt_used = models.BooleanField(default=False)
    already_a1_used = models.BooleanField(default=False)
    already_a2_used = models.BooleanField(default=False)
    already_a2_used = models.BooleanField(default=False)

    # def __str__(self):
    #     return self.dt_name
