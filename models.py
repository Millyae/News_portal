from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        post_rating = sum(post.rating*3 for post in self.post_set.all())
        comments_rating = sum(comment.rating for post in self.post_set.all() for comment in post.comment_set.all())
        self.rating = post_rating+comments_rating
        self.save()

class Category(models.Model):
    name = models.CharField(max_length=255,  unique = True)

POST_TYPE = [
    ('article', 'Статья'),
    ('news', 'Новости'),
]
class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=10, choices=POST_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through="PostCategory")
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def preview(self):
        return self.content[124]+'..' if len(self.content)>124 else self.content

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def update_rating(self):
        self.post.author.update_rating()