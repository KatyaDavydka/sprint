from rest_framework import status, request
from rest_framework.test import APITestCase
from .models import *
from django.urls import reverse
from .serializers import PerevalSerializer
from django.test import TestCase


class PerevalTestCase(APITestCase):
    '''
    Тест на проверку получения записи о созданном объекте в таблице Pereval
    '''

    def setUp(self):
        self.pereval_1 = Pereval.objects.create(
            user=AppUser.objects.create(
                email='test@test.com',
                phone='89012345678',
                name='Test',
                surname='Testov',
                patronymic='Testovich'
            ),
            beauty_title='pereval',
            title='Pereval',
            other_titles='First Pereval',
            connect='Two Pereval and Three Pereval',
            coord_id=Coords.objects.create(
                latitude=32.456789,
                longitude=12.345678,
                height=1234
            ),
            level=Level.objects.create(
                winter='2a',
                summer='2a',
                autumn='2a',
                spring='2a'
            )
        )

    def test_pereval_detail(self):
        response = self.client.get(reverse('pereval-detail', kwargs={'pk': self.pereval_1.id}))
        serializer_data = PerevalSerializer(self.pereval_1, context={'request': response.wsgi_request}).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_list(self):
        response = self.client.get(reverse('pereval-detail', kwargs={'pk': self.pereval_1.id}))
        serializer_data = PerevalSerializer(self.pereval_1, context={'request': response.wsgi_request}).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(len(serializer_data), 11)
        self.assertEqual(status.HTTP_200_OK, response.status_code)


class PerevalSerializerTestCase(TestCase):
    def setUp(self):
        self.pereval_1 = Pereval.objects.create(
            beauty_title='BTitle_1',
            title='BT_1',
            other_titles='BT_11',
            connect='Connects1',
            user=AppUser.objects.create(
                email='email1@mail.ru',
                surname='Lastname1',
                name='Name1',
                patronymic='Patronymic1',
                phone='89210000001'
            ),
            coord_id=Coords.objects.create(
                latitude='11.11111111',
                longitude='11.11111111',
                height=111
            ),
            level=Level.objects.create(
                winter='1A',
                spring='1A',
                summer='1A',
                autumn='1A'
            ),
        )
        self.image_1 = Images.objects.create(
            name='imageTitle1',
            images='image1.jpg',
            pereval=self.pereval_1
        )

    def test_get_list(self):
        response = self.client.get(reverse('pereval-detail', kwargs={'pk': self.pereval_1.id}))
        # serializer_data = PerevalSerializer(self.pereval_1, context={'request': response.wsgi_request}).data
        serializer_data = PerevalSerializer([self.pereval_1], many=True,
                                            context={'request': response.wsgi_request}).data
        expected_data = [
            {
                'id': self.pereval_1.id,
                'beauty_title': 'BTitle_1',
                'title': 'BT_1',
                'other_titles': 'BT_11',
                'connect': 'Connects1',
                'add_time': self.pereval_1.add_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'status': 'new',
                'user': {
                    'email': 'email1@mail.ru',
                    'surname': 'Lastname1',
                    'name': 'Name1',
                    'patronymic': 'Patronymic1',
                    'phone': '89210000001'
                },
                'coord_id': {
                    'latitude': '11.11111111',
                    'longitude': '11.11111111',
                    'height': 111
                },
                'level': {
                    'winter': '1A',
                    'spring': '1A',
                    'summer': '1A',
                    'autumn': '1A'
                },
                'images': [
                    {
                        'name': 'imageTitle1',
                        'images': 'image1.jpg'
                    },
                ]
            },
        ]
        # self.assertEquals(serializer_data, expected_data)

