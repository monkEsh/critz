from django.db import models
from django.conf import settings
from django.db.models import Avg


BASR_DIR = settings.BASE_DIR


def user_directory_path(instance, filename):
    return "movies/static/img/movies/{0}".format(instance.title)


# Create your models here.
class MovieModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    release_date = models.DateField()
    image = models.FileField(upload_to=user_directory_path,
                             default="portal/static/img/default-movie.jpg")
    trailer = models.URLField()
    synopsis = models.TextField(max_length=1000)
    movie_rating = models.DecimalField(max_digits=3,
                                       decimal_places=2,
                                       null=True)
    
    def __str__(self):
        return str(self.user.username)

    @property
    def owner(self):
        return self.user


class MovieReview(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="user", on_delete=models.CASCADE)
    movie = models.ForeignKey(MovieModel, related_name="reviews", on_delete=models.CASCADE)
    review_title = models.CharField(max_length=100)
    review = models.TextField(max_length=1000)
    rating = models.IntegerField(null=False)
    time = models.DateField(auto_now=True)
    
    def save(self, *args, **kwargs):
        super(MovieReview, self).save(*args, **kwargs)
        movie_obj = MovieReview.objects.filter(movie=self.movie).first()
        movie_reviews_obj = MovieReview.objects.filter(movie=self.movie).aggregate(Avg('rating'))
        
        save_obj = MovieModel.objects.get(title=movie_obj.movie.title)
        save_obj.movie_rating = movie_reviews_obj["rating__avg"]
        save_obj.save()
        return save_obj


