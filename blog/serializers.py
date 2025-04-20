from rest_framework import serializers
from .models import Post, Category
from django.utils.text import slugify

class UserPostSerializer(serializers.ModelSerializer):
    """
    ユーザー向けの投稿シリアライザ
    読み取り専用のフィールドのみを提供
    """
    class Meta:
        model = Post
        fields = ('id', 'artist', 'song_title', 'body', 'posted_at')
        read_only_fields = fields

class AdminPostSerializer(serializers.ModelSerializer):
    """
    管理者向けの投稿シリアライザ
    全てのフィールドを編集可能（slugは自動生成）
    """
    class Meta:
        model = Post
        fields = ('id', 'artist', 'song_title', 'body', 'posted_at', 'slug')
        read_only_fields = ('id', 'posted_at', 'slug')

    def validate(self, data):
        # 必須フィールドのチェック
        for field in ['artist', 'song_title', 'body']:
            if not data.get(field) or not data.get(field).strip():
                raise serializers.ValidationError({field: f"{field}は必須です"})
            data[field] = data[field].strip()

        # 重複チェック
        artist = data.get('artist')
        song_title = data.get('song_title')

        if artist and song_title:
            existing = Post.objects.filter(artist=artist, song_title=song_title)
            if self.instance:
                existing = existing.exclude(id=self.instance.id)

            if existing.exists():
                raise serializers.ValidationError({
                    'non_field_errors': ['この曲は既に登録されています']
                })

        return data

    def _generate_unique_slug(self, title, instance=None):
        """
        一意のスラッグを生成する
        """
        base_slug = slugify(title)
        slug = base_slug
        counter = 1

        while True:
            # 自身のレコードは除外してチェック
            exists_query = Post.objects.filter(slug=slug)
            if instance:
                exists_query = exists_query.exclude(id=instance.id)

            if not exists_query.exists():
                break

            slug = f"{base_slug}-{counter}"
            counter += 1

        return slug

    def create(self, validated_data):
        # スラッグを自動生成
        validated_data['slug'] = self._generate_unique_slug(validated_data['song_title'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # 曲名が変更された場合のみスラッグを更新
        if 'song_title' in validated_data:
            validated_data['slug'] = self._generate_unique_slug(
                validated_data['song_title'],
                instance
            )
        return super().update(instance, validated_data)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug',)



