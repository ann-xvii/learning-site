from django.db import models


class Course(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title


class Step(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    content = models.TextField(blank=True, default='')
    # 0 is a safe default, you could also have it autoincrement
    order = models.IntegerField(default=0)
    course = models.ForeignKey(Course)

    def __str__(self):
        return self.title

    # Django models are classes that represent tables in the database
    # Django models have an optional piece to them known as class meta.
    # Class meta is a class inside of our model class that controls how
    # that model does a few things.

    # We're going to use it to set a default ordering for our instances
    # we'll say ordering = order so order them by order
    class Meta:
        ordering = ['order', ]
