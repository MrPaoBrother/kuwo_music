# --*-- coding:utf8 --*--

from django.db import models

class Singer(models.Model):
    class Meta:
        db_table = "singer"

    id = models.BigIntegerField(primary_key=True, auto_created=True)
    singer_id = models.IntegerField(default=0)
    singer_name = models.CharField(max_length=255, default="")
    fans_num = models.IntegerField(default=0)
    music_num = models.IntegerField(default=0)
    album_num = models.IntegerField(default=0)
    # 1: kuwo music
    platform = models.IntegerField(default=1)
    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)
    extra = models.CharField(max_length=255, default="")

class Music(models.Model):
    class Meta:
        db_table = "music"

    id = models.BigIntegerField(primary_key=True, auto_created=True)
    sid = models.IntegerField(default=0)
    rid = models.IntegerField(default=0)
    artist = models.CharField(max_length=255, default="")
    music_name = models.CharField(max_length=255, default="")
    album_name = models.CharField(max_length=255, default="")
    album_id = models.IntegerField(default=0)
    duration = models.IntegerField(default=0)
    pub_date = models.CharField(max_length=255, default="")
    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)
    extra = models.CharField(max_length=255, default="")

class Link(models.Model):
    class Meta:
        db_table = "link"

    id = models.BigIntegerField(primary_key=True, auto_created=True)
    sid = models.IntegerField(default=0)
    rid = models.IntegerField(default=0)
    mp3_url = models.CharField(max_length=500, default="")
    downloaded = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)
    extra = models.CharField(max_length=255, default="")