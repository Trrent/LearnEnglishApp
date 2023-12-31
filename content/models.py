from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

import uuid


def get_video_path(instance, filename):
    return f"{instance.lesson.title}/Season {instance.lesson.season_num}/Episode {instance.lesson.episode_num}/{filename}"


class Serial(models.Model):
    id = models.CharField(default=uuid.uuid4, primary_key=True)
    title = models.CharField(max_length=180, blank=False)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title


class Season(models.Model):
    id = models.CharField(default=uuid.uuid4, primary_key=True)
    title = models.CharField(max_length=200)
    serial = models.ForeignKey(Serial, on_delete=models.CASCADE, related_name='seasons')
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f"{self.serial.title} {self.title}"


class Episode(models.Model):
    id = models.CharField(default=uuid.uuid4, primary_key=True)
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='episodes')
    title = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.season.serial.title} ({self.season.title} {self.title})"


class ItemBase(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # content = GenericRelation('Content')

    class Meta:
        abstract = True


class Content(models.Model):
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, related_name='contents')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={'model__in': ('itext',
                                                                                                            'ivideo',
                                                                                                            'iquiz')})
    object_id = models.CharField()
    item = GenericForeignKey('content_type', 'object_id')


class IText(ItemBase):
    rus = models.TextField()
    eng = models.TextField()

    # content = GenericRelation('Content')

    def __str__(self):
        return f"IText (rus: {self.rus} - eng: {self.eng})"


class IVideo(ItemBase):
    name = models.CharField(max_length=250)
    subtitles = models.CharField(blank=True)
    poster = models.FileField(upload_to='images')

    def __str__(self):
        return f"IVideo (name: {self.name})"


class Video(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    quality = models.CharField(max_length=10)
    src = models.URLField()
    iVideo = models.ForeignKey(IVideo, on_delete=models.CASCADE, related_name='qualitySrc')


class IQuiz(ItemBase):
    QUIZ_TYPE = (
        ('quiz', 'quiz'),
        ('test', 'test'),
    )

    type = models.CharField(max_length=10, choices=QUIZ_TYPE, default='quiz')
    score = models.IntegerField(blank=False, default=0)

    def __str__(self):
        return f"IQuiz ({self.type})"


class Question(models.Model):
    QUESTION_TYPE = (
        ('Yes/No', 'Yes/No'),
        ('multiple-choice', 'multiple-choice'),
        ('select', 'select'),
    )

    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    quiz_id = models.ForeignKey(IQuiz, on_delete=models.CASCADE, related_name='questions')
    type = models.CharField(max_length=20, choices=QUESTION_TYPE, default='quiz')
    score = models.IntegerField(blank=False, default=0)
    content = models.CharField(max_length=250)
    active = models.BooleanField(default=True)


class Answer(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    quiz_id = models.ForeignKey(IQuiz, on_delete=models.CASCADE, related_name='answers')
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    content = models.CharField(max_length=250)
    correct = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
