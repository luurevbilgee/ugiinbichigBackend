from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

class HumanPostTestCase(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@example.com",
            phone_number="99119911",
            password="pass1234"
        )
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)  # <-- чухал хэсэг

    def test_create_human_success(self):
        url = reverse("human")
        data = {
            "urgiin_ovog": "Торгууд",
            "ovog": "Бат",
            "ys_undes": "Халх",
            "name": "Батбаяр",
            "RD": "АБ99112233",
            "birth_date": "2000-01-01",
            "birth_counter": 25,
            "birth_year": 2000,
            "gender": "эр"
        }
        response = self.client.post(url, data, format='json')

        print(response.data)  # Алдааг илрүүлэхийн тулд шалгана

        self.assertEqual(response.status_code, status.HTTP_200_OK)
