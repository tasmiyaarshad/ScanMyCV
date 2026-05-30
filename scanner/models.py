from django.db import models

class ScanResult(models.Model):
    resume_filename = models.CharField(max_length=255)
    job_description = models.TextField()
    match_score = models.IntegerField()
    matched_skills = models.JSONField()
    missing_skills = models.JSONField()
    strengths = models.JSONField()
    improvements = models.JSONField()
    summary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.resume_filename} - {self.match_score}% - {self.created_at.strftime('%d %b %Y')}"