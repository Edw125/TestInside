import re

from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import LogsSerializer, CustomUserSerializer


from users.models import User, Logs


class LogsViewSet(APIView):
    serializer_class = LogsSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        username = self.request.data['name']
        user = self.request.user
        if user.username != username:
            return Response(
                {'detail': 'Невозможно добавить запись от имени другого пользователя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if re.findall(r'^history ([1-9]|[1-9]\d+)$', self.request.data['message']):
            number = int(self.request.data['message'].split(' ')[1])
            data = Logs.objects.filter(name=user)[:number]
            return Response(
                data.values("message", "pub_date"),
                status=status.HTTP_200_OK
            )
        else:
            Logs.objects.create(
                name=user,
                message=self.request.data['message']
            )
            return Response(
                {'detail': 'Запись успешно добавлена'},
                status=status.HTTP_201_CREATED
            )

    def delete(self, request, *args, **kwargs):
        username = self.request.data['name']
        user = self.request.user
        if user.username != username:
            return Response(
                {'detail': 'Невозможно удалить запись от имени другого пользователя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        log = Logs.objects.filter(name=user)
        if log:
            log.delete()
            return Response(
                {'detail': 'Запись удалена'},
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            {'error': 'Записи не существует'},
            status=status.HTTP_400_BAD_REQUEST
        )


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticated,)
