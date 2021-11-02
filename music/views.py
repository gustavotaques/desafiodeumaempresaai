from datetime import timedelta
from music.services import music, weather
from django.utils import timezone
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Music, TemperatureLocation
from .serializers import MusicSerializer

class MusicViewSet(ModelViewSet):
    serializer_class = MusicSerializer
    model = Music

    def get_queryset(self):
        location = self.request.GET.get('location', default='Joinville,Santa Catarina,BR')
        music_style = self._music_style_from_location(location)

        music_search =  Music.objects.filter(style=music_style)

        if music_search.count() == 0:
            music_list = self._request_music(music_style)

            if music_list:
                for music_name in music_list:
                    Music(name=music_name, style=music_style).save()
        
        return music_search

    def _music_style_from_location(self, location):
        cached_temperature = TemperatureLocation.objects.filter(location=location).first()
        if cached_temperature:
            limit_time = timezone.now() - timedelta(hours=1)

            if cached_temperature.last_update_time >= limit_time:
                return cached_temperature.style

        temp_location = self._request_temperature(location)

        if temp_location > 30:
            music_style = 'Party'
        if 15 <= temp_location <= 30:
            music_style = 'Pop'
        if 10 <= temp_location <= 14:
            music_style = 'Rock'
        if temp_location < 10:
            music_style = 'Classical'

        if not cached_temperature:
            cached_temperature = TemperatureLocation(location=location)
        
        cached_temperature.style = music_style
        cached_temperature.last_update_time = timezone.now()
        cached_temperature.save()

        return music_style


    def _request_temperature(self, location):
        return weather.temperature_in_celsius(location)
    
    def _request_music(self, query):
        return music.find_musics(query)