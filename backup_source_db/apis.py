from rest_framework import generics
from rest_framework.response import Response

from .models import BackupOffices
from .serializers import OfficesSerializer


class OfficeListAPI(generics.ListAPIView):
    queryset = BackupOffices.objects.filter(active_status=1)
    serializer_class = OfficesSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        term = request.GET.get('term')
        if term:
            queryset = BackupOffices.objects.filter(source_id__startswith=term)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
