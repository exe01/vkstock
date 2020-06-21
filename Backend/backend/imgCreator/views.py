from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseNotFound
import magic


class ImageView(View):
    def get(self, request, id=None):
        path = 'images/' + str(id)
        try:
            with open(path, 'rb') as img:
                mime = magic.Magic(mime=True)
                return HttpResponse(img.read(), content_type=mime.from_file(path))
        except IOError:
            return HttpResponseNotFound()
