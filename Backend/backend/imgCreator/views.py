from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseNotFound
import magic


class ImageView(View):
    def get(self, request, id=None):
        try:
            with open('images/123.jpg', 'rb') as img:
                mime = magic.Magic(mime=True)
                return HttpResponse(img.read(), content_type=mime.from_file('images/123.jpg'))
        except IOError:
            return HttpResponseNotFound()
