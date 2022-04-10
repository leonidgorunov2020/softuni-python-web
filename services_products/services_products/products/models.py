from django.contrib.auth import get_user_model
from django.db import models

from services_products.products.validators import MaxFileSizeInMbValidator

UserModel = get_user_model()


class Product(models.Model):
    TEMPLATE = "Template"
    PLUGIN = "Plugin"
    MODULE = "Module"
    OTHER = "Other"

    TYPES = [(x, x) for x in (TEMPLATE, PLUGIN, MODULE, OTHER)]

    IMAGE_MAX_SIZE_IN_MB = 5

    NAME_MAX_LEN = 100

    IMAGE_UPLOAD_TO_DIR = 'items/'

    name = models.CharField(
        max_length=NAME_MAX_LEN
    )

    description = models.TextField(
        blank=True,
        null=True,
    )

    screenshot = models.ImageField(
        upload_to=IMAGE_UPLOAD_TO_DIR,
        null=True,
        blank=True,
        default='default-image.jpeg',
        validators=(
            MaxFileSizeInMbValidator(IMAGE_MAX_SIZE_IN_MB),
        )
    )

    type = models.CharField(
        max_length=max(len(x) for (x, _) in TYPES),
        choices=TYPES,
    )

    date_of_release = models.DateTimeField(
        auto_now_add=True,
    )

    price = models.FloatField()

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.name} {self.type}"