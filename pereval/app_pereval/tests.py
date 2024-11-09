from app_pereval.models import Coords, Images, Level, Pereval, AppUser
from app_pereval.serializers import PerevalSerializer

from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase


class PerevalAPITestCase(APITestCase):
    def setUp(self):
        self.pereval_1 = Pereval.objects.create(
            beauty_title='Beauty title 1',
            title='Title 1',
            other_titles='Other titles 1',
            connect='Connect',
            user=AppUser.objects.create(
                email='user1@mail.ru',
                surname='lastname1',
                name='firstname1',
                patronymic='patronymic1',
                phone='11111111111'
            ),
            coord_id=Coords.objects.create(
                latitude='11.11111',
                longitude='22.22222',
                height='1111'
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

        self.pereval_2 = Pereval.objects.create(
            beauty_title='Beauty title 2',
            title='Title 2',
            other_titles='Other titles 2',
            connect='Connect',
            user=AppUser.objects.create(
                email='user2@mail.ru',
                surname='lastname2',
                name='firstname2',
                patronymic='partonymic2',
                phone='22222222222'
            ),
            coord_id=Coords.objects.create(
                latitude='33.33333',
                longitude='44.44444',
                height='2222'
            ),
            level=Level.objects.create(
                winter='',
                spring='1A',
                summer='1A',
                autumn='1A'
            ),
        )

        self.image_2 = Images.objects.create(
            name='imageTitle2',
            images='image2.jpg',
            pereval=self.pereval_2
        )

    def test_get_list(self):
        url = f'{reverse("pereval-list")}?get_all=true'
        response = self.client.get(url)
        serializer_data = PerevalSerializer([self.pereval_1, self.pereval_2], many=True).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(len(serializer_data), 2)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_detail(self):
        url = reverse('pereval-detail', args=(self.pereval_1.id,))
        response = self.client.get(url)
        serializer_data = PerevalSerializer(self.pereval_1).data
        self.assertEqual(serializer_data, response.data)
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

        self.pereval_2 = Pereval.objects.create(
            beauty_title='BTitle_2',
            title='BT_2',
            other_titles='BT_22',
            connect='Connects2',
            user=AppUser.objects.create(
                email='email2@mail.ru',
                surname='Lastname2',
                name='Name2',
                patronymic='Patronymic2',
                phone='89210000002'
            ),
            coord_id=Coords.objects.create(
                latitude='22.22222222',
                longitude='22.22222222',
                height=222
            ),
            level=Level.objects.create(
                winter='2A',
                spring='2A',
                summer='2A',
                autumn='2A'
            )
        )
        self.image_2 = Images.objects.create(
            title='imageTitle2',
            image='image2.jpg',
            pereval=self.pereval_2
        )

    def test_get_list(self):
        serializer_data = PerevalSerializer([self.pereval_1, self.pereval_2], many=True).data
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
                        'title': 'imageTitle1',
                        'image': 'image1.jpg'
                    },
                ]
            },

            {
                'id': self.pereval_2.id,
                'beauty_title': 'BTitle_2',
                'title': 'BT_2',
                'other_titles': 'BT_22',
                'connect': 'Connects2',
                'add_time': self.pereval_2.add_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'status': 'new',
                'user': {
                    'email': 'email2@mail.ru',
                    'surname': 'Lastname2',
                    'name': 'Name2',
                    'patronymic': 'Patronymic2',
                    'phone': '89210000002'
                },
                'coord_id': {
                    'latitude': '22.22222222',
                    'longitude': '22.22222222',
                    'height': 222
                },
                'level': {
                    'winter': '2A',
                    'spring': '2A',
                    'summer': '2A',
                    'autumn': '2A'
                },
                'images': [
                    {
                        'title': 'imageTitle2',
                        'image': 'image2.jpg'
                    },
                ]
            }
        ]
        self.assertEquals(serializer_data, expected_data)
