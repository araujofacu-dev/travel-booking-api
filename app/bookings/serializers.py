from rest_framework import serializers

from .models import Booking, Customer, Payment, TourPackage


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "id", "keycloak_id", "email", "first_name", "last_name",
            "phone", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class TourPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourPackage
        fields = [
            "id", "name", "description", "destination", "start_date",
            "end_date", "price", "capacity", "is_active",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate(self, attrs):
        start = attrs.get("start_date", getattr(self.instance, "start_date", None))
        end = attrs.get("end_date", getattr(self.instance, "end_date", None))
        if start and end and end < start:
            raise serializers.ValidationError(
                {"end_date": "End date must be on or after the start date."}
            )
        return attrs


class BookingSerializer(serializers.ModelSerializer):
    seats = serializers.IntegerField(min_value=1)

    class Meta:
        model = Booking
        fields = [
            "id", "customer", "package", "seats", "status",
            "total_amount", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "status", "total_amount", "created_at", "updated_at"]

    def validate_package(self, package):
        if not package.is_active:
            raise serializers.ValidationError("This package is not available.")
        return package

    def create(self, validated_data):
        package = validated_data["package"]
        validated_data["total_amount"] = package.price * validated_data["seats"]
        return super().create(validated_data)


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id", "booking", "amount", "status", "external_reference",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "status", "created_at", "updated_at"]