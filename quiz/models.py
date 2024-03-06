from django.db import models

class LearningOption(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    value = models.CharField(max_length=200)
    label = models.CharField(max_length=200)

class LearningQuiz(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    section = models.IntegerField()
    number = models.IntegerField()
    question = models.TextField()
    answer = models.TextField()
    options = models.ManyToManyField(LearningOption)

class LearningSummary(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    section = models.IntegerField()
    title = models.TextField()
    content = models.TextField()