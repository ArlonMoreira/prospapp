from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import StatusSerializer
from ..models import Company, CompanyPeople

class StatusViews(generics.GenericAPIView):
    serializer_class = StatusSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        companys = list(Company.objects.all().values())
        
        result = []
        for v in companys:
            joined = CompanyPeople.objects.filter(company=v['id'], user=request.user)
            result.append({
                'id': v['id'],
                'identification_number': v['identification_number'],
                'trade_name': v['trade_name'],
                'logo': v['logo'],
                'is_joined': joined.first().is_joined if joined.exists() else False,
                'is_pending': joined.first().is_pending if joined.exists() else False
            })

        serializer = self.serializer_class(result, many=True).data

        return Response({'message': 'Dados retornados com sucesso', 'data': serializer}, status=status.HTTP_200_OK)
