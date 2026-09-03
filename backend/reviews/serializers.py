from rest_framework import serializers

from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.full_name", read_only=True)

    class Meta:
        model = Review
        fields = ["id", "user_name", "rating", "comment", "created_at"]
        read_only_fields = ["id", "user_name", "created_at"]

    def validate_rating(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError("التقييم يجب أن يكون بين 1 و5 نجوم.")
        return value

    def create(self, validated_data):
        request = self.context["request"]
        product = self.context["product"]
        if Review.objects.filter(product=product, user=request.user).exists():
            raise serializers.ValidationError({"error": "لقد قيّمت هذا المنتج مسبقاً."})
        validated_data["user"] = request.user
        validated_data["product"] = product
        return super().create(validated_data)
