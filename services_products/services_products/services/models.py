from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


class Service(models.Model):
    ONE_TIME = 'One Time'
    WEEKLY = 'Weekly'
    MONTHLY = 'Monthly'
    OTHER = 'Other'

    CYCLES = [(x, x) for x in (ONE_TIME, WEEKLY, MONTHLY, OTHER)]

    NAME_MAX_LEN = 100

    name = models.CharField(
        max_length=NAME_MAX_LEN
    )

    description = models.TextField(
        blank=True,
        null=True,
    )

    cycle = models.CharField(
        max_length=max(len(x) for (x, _) in CYCLES),
        choices=CYCLES,
    )

    date_of_publish = models.DateTimeField(
        auto_now_add=True,
    )

    fee = models.FloatField()

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.name} {self.cycle}"
