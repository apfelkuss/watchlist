from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import DeleteView
from django.shortcuts import render
from django.urls import reverse_lazy

from kinopoisk.movie import Movie

from films.models import Film


class IndexView(ListView):
    template_name = "films/index.html"
    context_object_name = "all_films"

    def get_queryset(self):
        return Film.objects.all()

    def get(self, request):
        to_watch_films = Film.objects.filter(status="to_watch").order_by("-edit_time")[:4]
        completed_films = Film.objects.filter(status="completed").order_by("-edit_time")[:4]
        return render(request, self.template_name, {"to_watch_films": to_watch_films,
                                                    "completed_films": completed_films})

    def post(self, request):
        self.helper(request)
        to_watch_films = Film.objects.filter(status="to_watch").order_by("-edit_time")
        completed_films = Film.objects.filter(status="completed").order_by("-edit_time")
        return render(request, self.template_name, {"to_watch_films": to_watch_films,
                                                    "completed_films": completed_films})

    def helper(self, request):
        # pulls all required info from kinopoisk
        kinopoisk_id = request.POST.get("kinopoisk_id")
        kinopoisk_info = Movie(id=kinopoisk_id)
        kinopoisk_info.get_content("main_page")
        film = Film()
        film.kinopoisk_id = kinopoisk_id
        film.title = kinopoisk_info.title
        film.title_original = kinopoisk_info.title_original
        film.year = kinopoisk_info.year
        film.country = ", ".join(kinopoisk_info.countries)
        film.poster = "https://st.kp.yandex.net/images/film_iphone/iphone360_" + kinopoisk_id + ".jpg"
        film.genre = ", ".join(kinopoisk_info.genres)
        film.director = ", ".join(kinopoisk_info.directors)
        film.scriptwriter = ", ".join(kinopoisk_info.screenwriters)
        film.actors = ", ".join(kinopoisk_info.actors)
        film.plot = kinopoisk_info.plot
        film.length = kinopoisk_info.runtime
        film.status = self.status
        film.save()


class ToWatchView(IndexView):
    template_name = "films/to_watch.html"
    context_object_name = "to_watch_films"
    films = Film.objects.filter(status="to_watch").order_by("-edit_time")
    status = "to_watch" # is used in the helper function

    def get(self, request):
        return render(request, self.template_name, {"to_watch_films": self.films})

    def post(self, request):
        self.helper(request)
        return render(request, self.template_name, {"to_watch_films": self.films})


class CompletedView(IndexView):
    template_name = "films/completed.html"
    context_object_name = "completed_films"
    films = Film.objects.filter(status="completed").order_by("-edit_time")
    status = "completed" # is used in the helper function

    def get(self, request):
        return render(request, self.template_name, {"completed_films": self.films})

    def post(self, request):
        self.helper(request)
        return render(request, self.template_name, {"completed_films": self.films})


class DetailView(DetailView):
    model = Film
    template_name = "films/detail.html"


class MarkAsCompleted(TemplateView):
    template_name = "films/completed.html"

    def post(self, request, pk):
        queryset = Film.objects.filter(pk=pk)
        for film in queryset:
            film.status = "completed"
            film.save()
        return render(request, self.template_name, {"completed_films": Film.objects.filter(status="completed")})


class FilmDelete(DeleteView):
    model = Film
    success_url = reverse_lazy("films:index")


class SearchView(TemplateView):
    template_name = "films/search.html"

    def get(self, request):
        query = request.GET.get("q", None)
        search_result = Movie.objects.search(query)
        ids = []
        titles = []
        years = []
        posters = []
        for film in search_result:
            ids.append(str(film.id))
            titles.append(film.title)
            years.append(film.year)
            posters.append("https://st.kp.yandex.net/images/film_iphone/iphone360_"
                           + str(film.id) + ".jpg")
        # replacing Nones with TBAs in movies with no release date.
        years = ["TBA" if x is None else x for x in years]
        base_info = list(zip(ids, titles, years, posters))
        # sorting movies by release year (desc),
        # movies with no release date are moved to the top.
        base_info.sort(key=lambda x: (type(x[2]) is not int, x[2]), reverse=True)
        return render(request, self.template_name, {"base_info": base_info,
                            "results": len(search_result), "q": query})
