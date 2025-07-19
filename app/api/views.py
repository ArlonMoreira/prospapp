from rest_framework.views import APIView
from rest_framework.response import Response
from app.models import VersionManager

class VersionView(APIView):

    def get(self, request):

        version = VersionManager.objects.all()[0].version

        return Response({"minVersion": version})