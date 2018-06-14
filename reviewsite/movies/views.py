from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    ListAPIView
)
from rest_framework.mixins import (
    CreateModelMixin
)
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Q
from .forms import UserLoginForm, UserRegistraionForm, MoviesAddForm
from .permissions import IsOwnerOrReadOnly
from .serializers import MoviePostSerializer
from .models import MovieModel, MovieReview
from django.contrib.auth import (authenticate, get_user_model, login, logout)
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
UserModel = get_user_model()


def index(request):
    data = {"user_auth": request.user.is_authenticated()}
    try:
        if request.session["admin"]:
            data["admin"] = True
    except:
        pass

    return render(request, "pages/index.html", data)


def about_movie(request, pk):
    data = {"user_auth": request.user.is_authenticated(),
            "id": pk,
            "form": UserLoginForm}

    try:
        if request.session["admin"]:
            data["admin"] = True
    except:
        pass

    return render(request, "pages/about-movie.html", data)


def login_view(request):
    data = {"title": "Login"}
    form = UserLoginForm(request.POST or None)

    if form.is_valid():
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)

        login(request, user)
        if request.user.is_authenticated():
            user_obj = UserModel.objects.filter(username=username).filter(is_staff=True)
            print("Data is ", type(user_obj.count()))
            if user_obj.count() == 1:
                request.session["admin"] = True

            return redirect('index')

    data["form"] = form
    return render(request, "pages/login.html", data)


def logout_view(request):
    request.session["admin"] = False
    logout(request)
    return redirect('index')


def register_view(request):
    data = {"title": "Sign Up"}
    form = UserRegistraionForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        password = form.cleaned_data.get("password")
        new_user.set_password(password)
        new_user.save()
        return redirect('index')
        
    data["form"] = form
    return render(request, "pages/login.html", data)


@csrf_exempt
def post_reviews(request):
    data = {"success": False,
            "message": "None",
            "data": None}
    if request.method == "POST":
        try:

            user_obj = request.user
            review_title = request.POST.get("title")
            ratings = request.POST.get("rating")
            review = request.POST.get("review")
            pk = request.POST.get("id")

            movie_obj = MovieModel.objects.get(pk=pk)

            review_obj = MovieReview.objects.create(user=user_obj,
                                                    movie=movie_obj,
                                                    review=review,
                                                    review_title=review_title,
                                                    rating=ratings)
            review_obj.save()
            data["message"] = "data saved"
            data["success"] = True
        except Exception as ex:
            data["message"] = "Exception Raised [%s] " % ex
        finally:
            return JsonResponse(data)


def add_movie(request):
    data = {"title": "Add Movie",
            "form": MoviesAddForm,
            "message": None}
    if request.method == "POST":
        form = MoviesAddForm(request.POST,
                             request.FILES)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.user = request.user
            model_instance.save()
    return render(request, "pages/login.html", data)


########################################################
"""              Api for movie review                """
########################################################


class MoviesCreateView(CreateModelMixin, ListAPIView):
    lookup_field = 'pk'
    serializer_class = MoviePostSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        qs = MovieModel.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(
                Q(title__icontains=query)
            ).distinct()
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        try:
            if request.session["admin"]:
                return self.create(request, *args, **kwargs)
            else:
                return Response("user does not have permission for this operation")
        except:
            return Response("user does not have permission for this operation")


class MovieRudView(RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = MoviePostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    def get_queryset(self):
        return MovieModel.objects.all()


