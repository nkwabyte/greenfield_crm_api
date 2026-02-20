from rest_framework import serializers
from farmers.models import Farmer, FarmerGroup, FarmerRequest, RequestItem

class FarmerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farmer
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class FarmerGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmerGroup
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class RequestItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestItem
        fields = ['id', 'product', 'product_name', 'quantity', 'dynamic_price', 'total']
        read_only_fields = ['id']

class FarmerRequestSerializer(serializers.ModelSerializer):
    items = RequestItemSerializer(many=True, required=False)

    class Meta:
        model = FarmerRequest
        fields = [
            'id', 'farmer', 'group', 'season_year', 'grand_total', 
            'status', 'request_date', 'created_at', 'updated_at', 
            'is_deleted', 'items'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        request = FarmerRequest.objects.create(**validated_data)
        for item_data in items_data:
            RequestItem.objects.create(request=request, **item_data)
        return request

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if items_data is not None:
            instance.items.all().delete()
            for item_data in items_data:
                RequestItem.objects.create(request=instance, **item_data)
                
        return instance
