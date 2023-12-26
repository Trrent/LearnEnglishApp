from django.db import models
import uuid


def get_video_path(instance, filename):
    return f"{instance.lesson.title}/Season {instance.lesson.season_num}/Episode {instance.lesson.episode_num}/{filename}"


# class VideoPart(models.Model):
#     uuid = models.UUIDField(default=uuid.uuid4, unique=True)
#     name = models.CharField(max_length=180)
#     src = models.FileField(upload_to=get_video_path, max_length=180)
#     subtitles = models.CharField(max_length=180, blank=True)
#     poster = models.FileField(upload_to=get_video_path, max_length=180, blank=True)
#     quality_src = models.CharField(max_length=180)
#
#     def __str__(self):
#         return self.task
#
#
# class Question(models.Model):
#     uuid = models.UUIDField(default=uuid.uuid4, unique=True)
#     question = models.CharField(max_length=180, blank=False)
#     right_answer = models.CharField(max_length=180, blank=False)
#
#     def __str__(self):
#         return self.question
#
#
# class Answer(models.Model):
#     uuid = models.UUIDField(default=uuid.uuid4, unique=True)
#     question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
#     answer = models.CharField(max_length=180, blank=True)
#
#     def __str__(self):
#         return f"Answer: {self.answer}"
#
#
# class Lesson(models.Model):
#     uuid = models.UUIDField(default=uuid.uuid4, unique=True)
#     title = models.CharField(max_length=180, blank=False)
#     description = models.CharField(max_length=500, blank=True)
#     season_num = models.IntegerField(blank=False)
#     episode_num = models.IntegerField(blank=False)
#     video_src = models.ForeignKey(VideoPart, on_delete=models.CASCADE, related_name='lesson', blank=True)
#
#     def __str__(self):
#         return f"{self.title} ({self.season_num} season, {self.episode_num} episode"
#
#
# class QuizPart(models.Model):
#     uuid = models.UUIDField(default=uuid.uuid4, unique=True)
#     questions = models.CharField(blank=True)
#     lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='quiz_src')
#
#     def __str__(self):
#         return self.questions


class Course(models.Model):
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
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='seasons')
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f"{self.course.title} {self.title}"


class Episode(models.Model):
    id = models.CharField(default=uuid.uuid4, primary_key=True)
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='episodes')
    title = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.season.course.title} ({self.season.title} {self.title})"