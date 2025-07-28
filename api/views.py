from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def empty_json(request):
    """
    Returns an empty JSON object
    """
    return Response({})

@api_view(['GET'])
def api_status(request):
    """
    Returns API status
    """
    return Response({
        'status': 'API is running',
        'message': 'Django REST API backend is working'
    })