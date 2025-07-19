from rest_framework.views import APIView
from rest_framework.response import Response
from app.models import VersionManager

class VersionView(APIView):

    def get(self, request):

        data = VersionManager.objects.all()[0]

        return Response({
            "minVersion": data.version,
            "expo_build_link_android": data.expo_build_link_android,
            "expo_build_link_ios": data.expo_build_link_ios
        })