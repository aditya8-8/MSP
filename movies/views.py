import re
from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Movies
from movies.utils import fetch_n_predict
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_protect
import json
from django.http import JsonResponse

def admin(request):
    admin_url = reverse('admin:index')
    return HttpResponse(admin_url)

def home(request):
    movies = Movies.objects.all().order_by('id')
    paginator = Paginator(movies, 6)  # Show 5 contacts per page
    page = request.GET.get('page')
    movies = paginator.get_page(page)

    for movie in movies:
        if movie.genres:
            movie.genres = movie.genres.split(', ') 

    return render(request, 'movies/home.html', {'movies': movies})

def details(request, id):
    detail = get_object_or_404(Movies, pk=id)
    print()
    print(f"---> Movie ID : '{detail.pk}'")
    yt_tr = detail.Youtube_trailer_link
    yt_tr = yt_tr.replace("watch?v=", "embed/")
    if detail.genres:
        genres = detail.genres.split(", ")
        return render(request, 'Movies/details.html', {'detail': detail, 'yt_tr': yt_tr, 'genres': genres})
    else:
        print()
        print(f"Movie Name : {detail.name}")
        return render(request, 'Movies/details.html', {'detail': detail, 'yt_tr': yt_tr,})

def search(request):
    keywords = ''
    movies = Movies.objects.all()
    if 'keywords' in request.POST:
        keywords = request.POST['keywords']
        if keywords:
            movies = movies.filter(name__icontains=keywords)
    return render(request, 'movies/search.html', {'movies': movies, 'keywords': keywords})

@csrf_protect
def predict(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        movie_ID = data.get('movie_ID')
        print()
        print(f"Movie ID : '{movie_ID}'")
        print()

        try:
            # Check if the movie instance exists
            movie_instance = Movies.objects.get(pk=movie_ID)
            
            # Check if Predicted_Rating is already populated
            if movie_instance.Predicted_Rating is not None:
                print("Already Predicted")
                movie_instance.Predicted_Rating = float(movie_instance.Predicted_Rating)
                movie_instance.g_score = float(movie_instance.g_score)
                movie_instance.v_score = float(movie_instance.v_score)
                movie_instance.f_score = float(movie_instance.f_score)

                result = movie_instance.Predicted_Rating + movie_instance.g_score + movie_instance.v_score + movie_instance.f_score
                result = round(result, 1)
                if result > 10:
                    result = 10

            else:
                # Call fetch_n_predict function
                directors = movie_instance.directors
                writers = movie_instance.writers
                producers = movie_instance.producers
                cast = movie_instance.cast

                movie_Name = movie_instance.name
                movie_year = movie_instance.year
                match = re.match(r'(.+)\s\((\d{4})\)', movie_Name)
                if match:
                    #print(f'Year included in Name')
                    movie_name = movie_Name
                else: 
                    #print(f'Year not included in Name')
                    # If the year is not included in the name, append it from the instance's year field
                    movie_name_with_year = f"{movie_Name} ({movie_year})"
                    #print(f'Year appended to Name')
                    movie_name = movie_name_with_year
                
                print(f'Cast&Crew info fetched from Database')
                predicted_rating = fetch_n_predict(movie_name, directors, writers, producers, cast)

                # Update Predicted_Rating field for the corresponding movie instance

                movie_instance.Predicted_Rating = predicted_rating
                movie_instance.save()

                #print("Updating Database")


                movie_instance.Predicted_Rating = float(movie_instance.Predicted_Rating)
                movie_instance.g_score = float(movie_instance.g_score)
                movie_instance.v_score = float(movie_instance.v_score)
                movie_instance.f_score = float(movie_instance.f_score)
                
                if movie_instance.g_score > 0 and movie_instance.v_score > 0 and movie_instance.f_score > 0 :
                    print("Adding Scores for Genre, View Count, Followers Count")
                    result = movie_instance.Predicted_Rating + movie_instance.g_score + movie_instance.v_score + movie_instance.f_score
                    result = round(result, 1)
                    print()
                    print(f"MSP Rating : {result}")
                
                elif movie_instance.g_score > 0 and movie_instance.v_score > 0 :
                    print("Adding Scores for Genre, View Count")
                    result = movie_instance.Predicted_Rating + movie_instance.g_score + movie_instance.v_score
                    result = round(result, 1)
                    print()
                    print(f"MSP Rating : {result}")

                elif movie_instance.g_score > 0 and movie_instance.f_score > 0 :
                    print("Adding Scores for Genre, Followers Count")
                    result = movie_instance.Predicted_Rating + movie_instance.g_score + movie_instance.f_score
                    result = round(result, 1)
                    print()
                    print(f"MSP Rating : {result}")
                
                elif movie_instance.v_score > 0 and movie_instance.f_score > 0 :
                    print("Adding Scores for View Count, Followers Count")
                    result = movie_instance.Predicted_Rating + movie_instance.v_score + movie_instance.f_score
                    result = round(result, 1)
                    print()
                    print(f"MSP Rating : {result}")

                elif movie_instance.g_score > 0 :
                    print("Adding Genre scores")
                    result = movie_instance.Predicted_Rating + movie_instance.g_score
                    result = round(result, 1)
                    print()
                    print(f"MSP Rating : {result}")

                elif movie_instance.v_score > 0 :
                    print("Adding Viewcount scores")
                    result = movie_instance.Predicted_Rating + movie_instance.v_score
                    result = round(result, 1)
                    print()
                    print(f"MSP Rating : {result}")

                elif movie_instance.f_score > 0 :
                    print("Adding Followers Count scores")
                    result = movie_instance.Predicted_Rating + movie_instance.f_score
                    result = round(result, 1)
                    print()
                    print(f"MSP Rating : {result}")

                else:
                    print("No additional scores to Add")
                    result =movie_instance.Predicted_Rating
                    result = round(result, 1)
                    print()
                    print(f"MSP Rating : {result}")

                result = round(result, 1)
                if result > 10:
                    result = 10

            # Return prediction result
            response = JsonResponse({'result': result})
            print()
            print("Response sent to Client")
            return response

        except Movies.DoesNotExist:
            return JsonResponse({'error': 'Movie not found'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
