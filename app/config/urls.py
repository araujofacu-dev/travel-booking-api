from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

from bookings.views import (
    BookingViewSet,
    CustomerViewSet,
    PaymentViewSet,
    TourPackageViewSet,
)

router = DefaultRouter()
router.register("customers", CustomerViewSet)
router.register("packages", TourPackageViewSet)
router.register("bookings", BookingViewSet)
router.register("payments", PaymentViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
]