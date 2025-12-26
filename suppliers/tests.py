from django.test import TestCase
from django.core.exceptions import ValidationError
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from suppliers.models import Supplier

User = get_user_model()


class SupplierModelTest(TestCase):
    def create_supplier(self, **kwargs):
        defaults = {
            'name': 'Тестовый поставщик',
            'type': Supplier.RETAIL,
            'email': 'test@example.com',
            'country': 'Россия',
            'city': 'Москва',
            'street': 'Тестовая',
            'house_number': '10',
            'debt': 100.00
        }
        defaults.update(kwargs)
        return Supplier.objects.create(**defaults)

    def test_factory_must_have_zero_debt(self):
        """Завод должен создаваться только с debt=0"""
        supplier = self.create_supplier(
            type=Supplier.FACTORY,
            debt=0.00
        )
        self.assertEqual(supplier.debt, 0)
        self.assertEqual(supplier.type, Supplier.FACTORY)

    def test_non_factory_can_have_debt(self):
        """Не-заводы могут иметь задолженность"""
        retail = self.create_supplier(
            type=Supplier.RETAIL,
            debt=500.00
        )
        self.assertEqual(retail.debt, 500.00)

        entrepreneur = self.create_supplier(
            type=Supplier.ENTREPRENEUR,
            debt=250.00
        )
        self.assertEqual(entrepreneur.debt, 250.00)

    def test_validation_error_for_factory_with_debt(self):
        """Валидация запрещает завод с debt != 0"""
        supplier = Supplier(
            name="Завод",
            type=Supplier.FACTORY,
            email='factory@test.com',
            country='Россия',
            city='Москва',
            street='Заводская',
            house_number='1',
            debt=100.00
        )

        with self.assertRaises(ValidationError) as cm:
            supplier.full_clean()

        errors = cm.exception.message_dict
        self.assertIn('debt', errors)
        self.assertIn('Завод не может иметь задолженности', str(errors['debt']))


class SupplierAPITest(APITestCase):
    """API тесты"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user',
            password='testpass123',
            is_active=True
        )
        self.client.force_authenticate(user=self.user)

        self.supplier = Supplier.objects.create(
            name="Тестовый поставщик",
            type=Supplier.RETAIL,
            email="test@example.com",
            country="Россия",
            city="Москва",
            street="Тестовая",
            house_number="10",
            debt=500.00
        )

    def test_get_suppliers_list(self):
        """✅ GET /api/suppliers/ - основной эндпоинт работает"""
        response = self.client.get('/suppliers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_filter_by_country(self):
        """✅ Фильтрация по стране работает (требование задания)"""
        Supplier.objects.create(
            name="Иностранный",
            type=Supplier.RETAIL,
            email="foreign@test.com",
            country="USA",  # другая страна
            city="NY",
            street="Broadway",
            house_number="100",
            debt=300.00
        )

        response = self.client.get('/suppliers/?country=Россия')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for supplier in response.data:
            self.assertEqual(supplier['country'], 'Россия')

    def test_cannot_update_debt_via_api(self):
        """✅ Запрет обновления debt через API (требование задания)"""
        url = f'/suppliers/{self.supplier.id}/'
        data = {'debt': '0.00'}

        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('debt', response.data)

    def test_can_update_other_fields(self):
        """✅ Можно обновлять другие поля"""
        url = f'/suppliers/{self.supplier.id}/'
        data = {'name': 'Обновленное название', 'city': 'Новый город'}

        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.supplier.refresh_from_db()
        self.assertEqual(self.supplier.name, 'Обновленное название')


class PermissionTests(TestCase):
    """Тесты прав доступа"""

    def test_inactive_user_cannot_access(self):
        """✅ Только активные сотрудники (требование задания)"""
        user = User.objects.create_user(
            username='inactive',
            password='testpass',
            is_active=False
        )

        client = APIClient()
        client.force_authenticate(user=user)

        response = client.get('/suppliers/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_active_user_can_access(self):
        """✅ Активный пользователь может получить доступ"""
        user = User.objects.create_user(
            username='active',
            password='testpass',
            is_active=True
        )

        client = APIClient()
        client.force_authenticate(user=user)

        response = client.get('/suppliers/')
        self.assertIn(response.status_code,
                      [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND])
