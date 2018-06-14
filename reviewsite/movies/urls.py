from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^index/', views.index, name="index"),
    url(r'^about-movie/(?P<pk>\d+)', views.about_movie),
    url(r'^login/', views.login_view, name='login'),
    url(r'^logout/', views.logout_view),
    url(r'^register/', views.register_view),
    url(r'^movies-rud/(?P<pk>\d+)', views.MovieRudView.as_view(), name="movies-rud"),
    url(r'^movies-cl/', views.MoviesCreateView.as_view(), name="movies-cl"),
    url(r'^post-review/', views.post_reviews, name="post-reviews"),
    url(r'^add_movie', views.add_movie, name="add-movie")
]
