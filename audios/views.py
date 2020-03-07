from django.shortcuts import render, get_object_or_404
from audios.models import Audio, Author
from django.views import generic
from django.http import HttpResponse, FileResponse, JsonResponse
import pathlib
import os


def index(request):
    num_audios = Audio.objects.all().count()
    num_authors = Author.objects.all().count()

    context = {
        'num_audios': num_audios,
        'num_authors': num_authors,
    }

    return render(request, 'index.html', context=context)

class AudioListView(generic.ListView):
    model = Audio

class AudioDetailView(generic.DetailView):
    model = Audio

class AuthorListView(generic.ListView):
    model = Author

class AuthorDetailView(generic.DetailView):
    model = Author

# OK
# These show how standard functions can be used to achieve the same goal as above,
# perhaps with a little more control.
# When using below 2 functions instead of classes above, be sure to change
# 'audio_list' to 'audios' in audio_list.html file.
# def audio_list(request):
#     audios = Audio.objects.all()
#     return render(request, 'audios/audio_list.html', {'audios': audios})

# def audio_detail(request, pk):
#     audio = get_object_or_404(Audio, pk=pk)
#     return render(request, 'audios/audio_detail.html', {'audio': audio})

# Example of returning multiple items...
# def audio_detail(request, pk):
#     audio = get_object_or_404(Audio, pk=pk)
#     trackParts = pathlib.Path.home() / 'sharefromwindows' / 'frog_lillypad.mp3'
#     path = ""
#     for part in trackParts.parts:
#         if part != "/":
#             path += "/" + part
#     track = FileResponse(open(path, "rb"))

# #     Note how I am returning the model as well as the track, which I calculate above.
#     return render(request, 'audios/audio_detail.html', {'audio': audio, 'track': track})

# This views returns the actual audio content. It's path is called by audio_detail template. 
# If not called by a template, the audio will play directly in browser.
# From mediaserver project
# Return the actual track. Accessed with:
# http://127.0.0.1:8000/audios/scotty/frog_lillypad.mp3/
# OK GF def scottyMp3Filename(request, filename):
# GF
# def getAudioFile(request, filename):
#     # music = pathlib.Path.home() / 'sharefromwindows' / 'frog_lillypad.mp3'
#     music = pathlib.Path.home() / 'sharefromwindows' / filename
#     path = ""
#     for part in music.parts:
#         if part != "/":
#             path += "/" + part
    
#     response = FileResponse(open(path, "rb"))
#     return response

# With share hierarchy
# OK def getAudioFile(request, path1, path2, filename):
#     # music = pathlib.Path.home() / 'sharefromwindows' / 'frog_lillypad.mp3'
#     music = pathlib.Path.home() / 'sharefromwindows' / path1 / path2 / filename
#     path = ""
#     for part in music.parts:
#         if part != "/":
#             path += "/" + part
    
#     response = FileResponse(open(path, "rb"))
#     return response

# ToDo - These can be simplified into a single method that tests
# and constructs path as needed.
# Servve from share root.
def getAudioFilePath0(request, filename):
    audio = pathlib.Path.home() / 'sharefromwindows' / filename
    path = ""
    for part in audio.parts:
        if part != "/":
            path += "/" + part
    
    response = FileResponse(open(path, "rb"))
    return response

# Serve from one level below share root.
def getAudioFilePath1(request, path1, filename):
    audio = pathlib.Path.home() / 'sharefromwindows' / path1 / filename
    path = ""
    for part in audio.parts:
        if part != "/":
            path += "/" + part
    
    response = FileResponse(open(path, "rb"))
    return response

# Serve from two levels below share root.
def getAudioFilePath2(request, path1, path2, filename):
    audio = pathlib.Path.home() / 'sharefromwindows' / path1 / path2 / filename
    path = ""
    for part in audio.parts:
        if part != "/":
            path += "/" + part
    
    response = FileResponse(open(path, "rb"))
    return response

# Serve from three levels below share root.
def getAudioFilePath3(request, path1, path2, path3, filename):
    audio = pathlib.Path.home() / 'sharefromwindows' / path1 / path2 / path3 / filename
    path = ""
    for part in audio.parts:
        if part != "/":
            path += "/" + part
    
    response = FileResponse(open(path, "rb"))
    return response

# This returns path/title to support auto-play of next track.
def getPathTitle(request, pk):
    audio = get_object_or_404(Audio, pk=pk)
    data = {
        'path': audio.path,
        'title': audio.title
    }
    return JsonResponse(data)