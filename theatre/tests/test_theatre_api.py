from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from theatre.models import (Play,
                            Performance,
                            TheatreHall,
                            Genre,
                            Actor)
from theatre.serializers import PlayDetailSerializer


PLAY_URL = reverse("theatre:play-list")
PERFORMANCE_URL = reverse("theatre:performance-list")


def sample_play(**params):
    defaults = {
        "title": "test_title",
        "description": "test_description",
    }
    defaults.update(params)

    return Play.objects.create(**defaults)


def sample_genre(**params):
    defaults = {
        "name": "Comedy",
    }
    defaults.update(params)

    return Genre.objects.create(**defaults)


def sample_actor(**params):
    defaults = {"first_name": "user", "last_name": "last"}
    defaults.update(params)

    return Actor.objects.create(**defaults)


def sample_performance(**params):
    theatre_hall = TheatreHall.objects.create(name="Big",
                                              rows=20,
                                              seats_in_row=20)

    defaults = {
        "show_time": "2020-01-01 00:00:00",
        "play": None,
        "theatre_hall": theatre_hall,
    }
    defaults.update(params)

    return Performance.objects.create(**defaults)


def detail_url(play_id):
    return reverse("theatre:play-detail", args=[play_id])


class AuthenticatedPlayApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = get_user_model().objects.create_user(
            email="admin1@gmail.com", password="admin"
        )

        self.client.force_authenticate(self.user)

    def test_list_of_plays(self):
        response = self.client.get(PLAY_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("results" in response.data)
        self.assertIsInstance(response.data["results"], list)

    def test_play_detail(self):
        temp_play = sample_play()
        url = detail_url(temp_play.id)
        response = self.client.get(url)
        serializer = PlayDetailSerializer(temp_play)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_list_of_plays_with_filtering_by_title(self):
        test_play1 = sample_play(title="PlayTitle")
        test_play2 = sample_play(title="Test")

        response = self.client.get(PLAY_URL, {"title": "te"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue("results" in response.data)
        titles = [play["title"] for play in response.data["results"]]
        self.assertNotIn(test_play1.title, titles)
        self.assertIn(test_play2.title, titles)

    def test_list_of_plays_with_filtering_by_genre(self):
        test_genre = sample_genre(name="Comedy")
        test_play1 = sample_play(title="Comedy Play 1")
        test_play2 = sample_play(title="Comedy Play 2")
        test_play1.genre.add(test_genre)
        test_play2.genre.add(test_genre)

        response = self.client.get(PLAY_URL, {"genre": test_genre.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("results" in response.data)
        titles = [play["title"] for play in response.data["results"]]
        self.assertIn(test_play1.title, titles)
        self.assertIn(test_play2.title, titles)

    def test_list_of_plays_with_no_filter(self):
        test_play1 = sample_play(title="Test title")
        test_play2 = sample_play(title="test second")

        response = self.client.get(PLAY_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("results" in response.data)
        titles = [play["title"] for play in response.data["results"]]
        self.assertIn(test_play1.title, titles)
        self.assertIn(test_play2.title, titles)


class UnauthenticatedPlayApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(PLAY_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
