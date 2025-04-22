from django.contrib.auth.models import AbstractUser
from django.db import models
from markdownx.models import MarkdownxField


# Create your models here.
class Site(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    logo = models.ImageField(upload_to="images/")

    class Meta:
        verbose_name = "Site"
        verbose_name_plural = "Sites"

    def __str__(self):
        return self.name


class User(AbstractUser):
    avatar = models.ImageField(
        upload_to="images/users/avatars", default="images/users/avatars/default.jpg"
    )
    bio = models.TextField(max_length=500, null=True)
    ip_location = models.CharField(max_length=30, null=True)
    location = models.CharField(max_length=30, null=True)
    website = models.URLField(null=True)
    email = models.EmailField(max_length=254, unique=True)
    joined_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()  # preventing duplicate slugs
    description = models.TextField()

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    description = models.TextField()

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    content = MarkdownxField()
    featured_image = models.ImageField(upload_to="posts/featured_images/%Y/%m/%d/")
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_top = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)
    # Each post can receive likes from multiple users, and each user can like multiple posts
    likes = models.ManyToManyField(User, related_name="post_like")

    # Each post belong to one user and one category.
    # Each post has many tags, and each tag has many posts.
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    tag = models.ManyToManyField(Tag)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return self.title

    def get_number_of_likes(self):
        return self.likes.count()


class Comment(models.Model):
    content = models.TextField(max_length=1000)
    created_at = models.DateField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    # Each comment can receive likes from multiple users, and each user can like multiple comments
    likes = models.ManyToManyField(User, related_name="comment_like")

    # Each comment belongs to one user and one post
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        if len(self.content) > 50:
            comment = self.content[:50] + "..."
        else:
            comment = self.content
        return comment

    def get_number_of_likes(self):
        return self.likes.count()
