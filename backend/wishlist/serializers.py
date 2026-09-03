from rest_framework import serializers

from catalog.serializers import ProductSummarySerializer

from .models import WishlistItem


class WishlistItemSerializer(serializers.ModelSerializer):
    product_detail = ProductSummarySerializer(source="product", read_only=True)

    class Meta:
        model = WishlistItem
        fields = ["id", "product", "product_detail", "created_at"]
        read_only_fields = ["id", "product_detail", "created_at"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        item, _ = WishlistItem.objects.get_or_create(
            user=validated_data["user"], product=validated_data["product"]
        )
        return item
