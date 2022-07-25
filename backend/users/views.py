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

    def get(self, request, *args, **kwargs):
        user = self.request.user
        data = Logs.objects.filter(name=user)
        if data:
            return Response(
                data.values("id", "message", "pub_date"),
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'detail': 'Записей не существует'},
                status=status.HTTP_404_NOT_FOUND
            )

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
                data.values("id", "message", "pub_date"),
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

    def delete(self, request, pk, *args, **kwargs):
        user = self.request.user
        try:
            log = Logs.objects.get(pk=pk)
            if user.id != log.name.id:
                return Response(
                    {'detail': 'Невозможно удалить запись от имени другого пользователя'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if log:
                log.delete()
                return Response(
                    {'detail': 'Запись удалена'},
                    status=status.HTTP_204_NO_CONTENT
                )
        except Logs.DoesNotExist:
            return Response(
                {'detail': 'Записи не существует'},
                status=status.HTTP_404_NOT_FOUND
            )


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticated,)
