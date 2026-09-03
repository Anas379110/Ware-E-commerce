from rest_framework import serializers

from .models import Category, Product, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "parent", "icon"]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["image", "is_primary", "order"]


class ProductSummarySerializer(serializers.ModelSerializer):
    primary_image_url = serializers.SerializerMethodField()
    average_rating = serializers.FloatField(read_only=True)
    review_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "slug", "price", "primary_image_url", "in_stock", "average_rating", "review_count"]

    def get_primary_image_url(self, obj):
        image = obj.images.filter(is_primary=True).first() or obj.images.first()
        if image and image.image:
            request = self.context.get("request")
            url = image.image.url
            return request.build_absolute_uri(url) if request else url
        return None


class ProductDetailSerializer(ProductSummarySerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    related_products = serializers.SerializerMethodField()

    class Meta(ProductSummarySerializer.Meta):
        fields = ProductSummarySerializer.Meta.fields + [
            "description",
            "images",
            "category",
            "stock_quantity",
            "related_products",
        ]

    def get_related_products(self, obj):
        return ProductSummarySerializer(obj.related_products(), many=True, context=self.context).data
