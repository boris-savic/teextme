from django.http import HttpResponse
from django.utils import simplejson as json
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required

from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response

from teextme.models import Stats


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'contacts': reverse('contact-list', request=request)
    })


@login_required
def stats(request):
    stats = Stats(request.user)

    monthly = stats.monthly()

    data = {
        'monthly': monthly
    }

    return HttpResponse(
        json.dumps(data, cls=DjangoJSONEncoder),
        content_type='application/json'
    )
