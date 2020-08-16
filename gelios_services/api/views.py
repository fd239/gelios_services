from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from passport_check.models import Passport

PASSPORT_FOUND_COMMENT = 'Не действителен'
PASSPORT_NOT_FOUND_COMMENT = 'Среди недействительных не значится'


@api_view(['POST'])
def passport_check(request):

    SERIES = request.POST.get('series')
    NUMBER = request.POST.get('number')

    if SERIES is None or NUMBER is None:
        return Response({'result': False, 'comment': 'Указаны не правильные параметры запроса'}, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

    passport_found = Passport.objects.filter(
        PASSP_SERIES=SERIES, PASSP_NUMBER=NUMBER).count() > 0

    if passport_found:
        return Response({'result': passport_found, 'comment': PASSPORT_FOUND_COMMENT}, status=status.HTTP_200_OK, content_type='application/json')
    else:
        return Response({'result': passport_found, 'comment': PASSPORT_NOT_FOUND_COMMENT}, status=status.HTTP_200_OK, content_type='application/json')
