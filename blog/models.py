from django.db import models
# from mdeditor.fields import MDTextField

# Create your models here.

class Post(models.Model):
    artist = models.CharField(verbose_name='アーティスト', max_length=50)
    slug = models.SlugField('スラッグ', max_length=40, unique=True)
    song_title = models.CharField(verbose_name='曲名', max_length=50)
    posted_at = models.DateTimeField(auto_now_add=True)
    body = models.TextField(verbose_name='本文')

    class Meta:
        ordering = ('-posted_at',)
        unique_together = ('artist', 'song_title')

    def __str__(self):
        return self.song_title


class Category(models.Model):
    name = models.CharField('カテゴリ名', max_length=30)
    slug = models.SlugField('スラッグ', max_length=30)

    def __str__(self):
        return self.name

"""""""""""
class About(models.Model):
    profile_image = models.ImageField('プロフィール画像')
    body = MDTextField()
"""""""""""