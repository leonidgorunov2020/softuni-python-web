from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


class Job(models.Model):
    PART_TIME = 'Part Time'
    FULL_TIME = 'Full Time'
    OTHER = 'Other'

    DEVELOP = 'Develop'
    SUPPORT = 'Support'
    MAINTENANCE = 'Maintenance'
    QUALITY_ASSURANCE = 'Quality Assurance'
    DEVOPS = 'DevOps'

    JOB_TYPES = [(x, x) for x in (PART_TIME, FULL_TIME, OTHER)]
    JOB_RESPONSIBILITIES = [(x, x) for x in (DEVELOP, SUPPORT, MAINTENANCE, QUALITY_ASSURANCE, DEVOPS)]

    JOB_TITLE_MAX_LEN = 70

    title = models.CharField(
        max_length=JOB_TITLE_MAX_LEN
    )

    description = models.TextField(
        blank=True,
        null=True,
    )

    job_types = models.CharField(
        max_length=max(len(x) for (x, _) in JOB_TYPES),
        choices=JOB_TYPES,
    )

    job_responsibilities = models.CharField(
        max_length=max(len(x) for (x, _) in JOB_RESPONSIBILITIES),
        choices=JOB_RESPONSIBILITIES,
    )

    date_of_publish = models.DateTimeField(
        auto_now_add=True,
    )

    monthly_salary = models.FloatField()

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.title} {self.job_responsibilities} {self.job_types}"

