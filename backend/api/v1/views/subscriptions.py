"""ViewSet`ы для работы с подписками."""

from rest_framework.decorators import action

from api.v1.viewsets import CreateDestroyListViewSet
from api.v1.serializers import SubscriptionSerializer, UserSubscriptionsReadSerializer
from users.models import Subscription


class SubscriptionViewSet(CreateDestroyListViewSet):
    """ViewSet для работы с подписками."""

    queryset = Subscription.objects.select_related(
        "user",
        "follower",
    )
    serializer_class = SubscriptionSerializer

    @action(methods=["get"], detail=False, url_path="subscriptions")
    def get_subscriptions(self, request, *args, **kwargs):
        """Получение списка подписок текущего пользователя."""
        subscriptions = self.queryset.filter(user=request.user)
        serializer = self.get_serializer(subscriptions)
        return self.response(serializer.data)
