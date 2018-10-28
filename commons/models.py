from django.db import models

# Create your models here.


class Resource(models.Model):
    class Meta:
        db_table = 'resources'
        index_together = (
            ('model_type', 'model_id', 'resource_type', 'order'),
        )

    RESOURCE_TYPE_VIDEO = 'v'
    RESOURCE_TYPE_IMAGE = 'i'
    RESOURCE_TYPES = (
        (RESOURCE_TYPE_VIDEO, 'VIDEO'),
        (RESOURCE_TYPE_IMAGE, 'IMAGE'),
    )

    MODEL_TYPE_GAME = 'g'
    MODEL_TYPE_WOD = 'w'
    MODEL_TYPES = (
        # (MODEL_TYPE_GAME, 'GAME'),
        (MODEL_TYPE_WOD, 'WOD'),
    )

    resource_type = models.CharField(max_length=10, choices=RESOURCE_TYPES, default=RESOURCE_TYPE_IMAGE)
    model_type = models.CharField(max_length=10, choices=MODEL_TYPES, default=MODEL_TYPE_WOD)
    model_id = models.IntegerField()

    order = models.IntegerField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
