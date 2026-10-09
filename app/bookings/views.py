from django.shortcuts import render

# Create your views here.
from rest_framework import mixins, viewsets

from .models import Booking, Customer, Payment, TourPackage
from .serializers import (
    BookingSerializer,
    CustomerSerializer,
    PaymentSerializer,
    TourPackageSerializer,
)


class CreateListRetrieveUpdateViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """No delete: records linked to bookings or payments must be kept."""


class CreateListRetrieveViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """No update or delete: state changes go through business actions."""


class CustomerViewSet(CreateListRetrieveUpdateViewSet):
    queryset = Customer.objects.order_by("last_name", "first_name")
    serializer_class = CustomerSerializer


class TourPackageViewSet(CreateListRetrieveUpdateViewSet):
    queryset = TourPackage.objects.order_by("start_date")
    serializer_class = TourPackageSerializer


class BookingViewSet(CreateListRetrieveViewSet):
    queryset = Booking.objects.select_related("customer", "package").order_by("-created_at")
    serializer_class = BookingSerializer


class PaymentViewSet(CreateListRetrieveViewSet):
    queryset = Payment.objects.select_related("booking").order_by("-created_at")
    serializer_class = PaymentSerializer