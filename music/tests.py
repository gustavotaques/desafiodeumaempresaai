from datetime import timedelta
from time import timezone
from music.views import MusicViewSet
from django.http import response
from django.test import TestCase
from django.utils import timezone
from .services import music, weather
from .models import Music, TemperatureLocation
from unittest.mock import MagicMock


class TestOpenWeatherMapService(TestCase):
    def test_simple_request(self):
        self.assertTrue(weather.temperature_in_celsius('Joinville,Santa Catarina,BR') != 0)
        self.assertIsNone(weather.temperature_in_celsius('asldjasldkjaslk'))


class TestSpotifyService(TestCase):
    def test_simple_request(self):
        self.assertTrue(music.find_musics('Pop'))


class TestMusicView(TestCase):
    def setUp(self) -> None:
        Music(name='Party Music', style='Party').save()
        Music(name='Pop Music', style='Pop').save()
        Music(name='Rock Music', style='Rock').save()
        Music(name='Classical Music', style='Classical').save()

    def test_above_30_degrees_must_return_party_music(self):
        self.assertEqual('Party Music', self._simulate_weather(31))
        self.assertEqual('Party Music', self._simulate_weather(50))

    
    def test_between_15_to_30_degrees_must_return_pop_music(self):
        self.assertEqual('Pop Music', self._simulate_weather(30))
        self.assertEqual('Pop Music', self._simulate_weather(15))
        self.assertEqual('Pop Music', self._simulate_weather(20))
    
    def test_between_10_to_14_degrees_must_return_rock_music(self):
        self.assertEqual('Rock Music', self._simulate_weather(14))
        self.assertEqual('Rock Music', self._simulate_weather(10))
        self.assertEqual('Rock Music', self._simulate_weather(12))
    
    def test_below_10_degrees_must_return_classical_music(self):
        self.assertEqual('Classical Music', self._simulate_weather(9))
        self.assertEqual('Classical Music', self._simulate_weather(0))

    def test_no_music_on_database_must_search_on_spotify_and_return(self):
        Music.objects.all().delete()

        MusicViewSet._request_music = MagicMock(return_value=['Party Music'])

        self.assertEqual('Party Music', self._simulate_weather(50))
    
    def test_dont_request_temperature_when_have_recent_data_in_database(self):
        TemperatureLocation(location='Belo Horizonte,Minas Gerais,BR', style='Party', last_update_time=timezone.now()).save()
        MusicViewSet._request_temperature = MagicMock(return_value=0)

        response = self.client.get('/music/?location=Belo Horizonte,Minas Gerais,BR')

        self.assertEqual(200, response.status_code)
        self.assertEqual(0, MusicViewSet._request_temperature.call_count)
        self.assertEqual('Party Music', response.json()[0]['name'])

    def test_request_temperature_when_have_old_data_in_database(self):
        old_time = timezone.now() - timedelta(hours=10)
        TemperatureLocation(location='Belo Horizonte,Minas Gerais,BR', style='Party',
                            last_update_time=old_time).save()
        MusicViewSet._request_temperature = MagicMock(return_value=0)
        
        response = self.client.get('/music/?location=Belo Horizonte,Minas Gerais,BR')
        self.assertEqual(200, response.status_code)

        self.assertEqual(1, MusicViewSet._request_temperature.call_count)

        self.assertTrue(old_time != TemperatureLocation.objects.first().last_update_time)



    def _simulate_weather(self, temperature):
        MusicViewSet._request_temperature = MagicMock(return_value=temperature)
        response = self.client.get('/music/?location=Joinville,Santa Catarina,BR')

        self.assertEqual(200, response.status_code)

        return response.json()[0]['name']