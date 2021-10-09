from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=50)
    dt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Download(models.Model):
    document_id = models.IntegerField()
    group = models.ForeignKey(Group,
                              on_delete=models.CASCADE,
                              related_name='downloads')
    dt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Video(models.Model):
    document_id = models.ForeignKey(Download,
                                    on_delete=models.CASCADE,
                                    related_name='videos_id')
    group = models.ForeignKey(Group,
                              on_delete=models.CASCADE,
                              related_name='videos')
    already_used = models.BooleanField(default=False)
    dt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name