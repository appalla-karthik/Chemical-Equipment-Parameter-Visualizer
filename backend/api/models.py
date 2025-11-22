
# Create your models here.
from django.db import models
import json

class Dataset(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='datasets/')
    original_filename = models.CharField(max_length=255)
    summary_json = models.TextField(blank=True)
    pdf_report = models.FileField(upload_to='reports/', null=True, blank=True)

    def set_summary(self, summary_dict):
        self.summary_json = json.dumps(summary_dict)
        self.save()

    def get_summary(self):
        import json
        return json.loads(self.summary_json) if self.summary_json else {}
