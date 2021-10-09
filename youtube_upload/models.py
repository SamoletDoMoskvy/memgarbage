from django.db import models
from download.models import Video, Download


class Upload(models.Model):
    document = models.OneToOneField(Video,
                                    on_delete=models.CASCADE,
                                    related_name='uploads')

    dt = models.DateTimeField(auto_now_add=True)
    dt2 = models.DateTimeField(auto_now_add=True)

    download = models.OneToOneField(Download,
                                    on_delete=models.CASCADE,
                                    related_name='uploads')

    def __str__(self):
        return self.name

    #@property
    #def document_id(self):
        #return self.document.id

    @property
    def download_dt(self):
        return self.download.id


