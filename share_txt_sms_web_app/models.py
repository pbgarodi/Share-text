# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import uuid

# Create your models here.
class Message(models.Model):
    message = models.CharField(max_length=1024)
    message_id = models.CharField(max_length=1024,blank =True)
