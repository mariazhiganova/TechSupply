from rest_framework import serializers

from suppliers.models import Product, Supplier


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'model', 'release_date']


class SupplierSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    level = serializers.IntegerField(read_only=True)

    class Meta:
        model = Supplier
        fields = '__all__'
        read_only_fields = ['debt']

    def validate(self, data):
        """Дополнительная проверка на случай ошибки"""
        if self.instance and 'debt' in self.initial_data:  # ← initial_data, не data!
            raise serializers.ValidationError({
                'debt': 'Изменение задолженности через API запрещено'
            })
        return data
