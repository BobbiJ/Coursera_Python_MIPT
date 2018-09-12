from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt


def simple_rout(request):
    if request.method == 'GET':
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=405)


@require_http_methods('GET')
def slug_route(request, text):
    try:
        return HttpResponse(text)
    except:
        return HttpResponse(status=404)


@require_http_methods('GET')
def sum_route(request, a, b):
    try:
        return HttpResponse(str(int(a) + int(b)))
    except:
        return HttpResponse(status=404)


@require_http_methods('GET')
def sum_get_method(request):
    try:
        a = request.GET['a']
        b = request.GET['b']
        return HttpResponse(str(int(a) + int(b)))
    except:
        return HttpResponse(status=400)


@csrf_exempt
@require_http_methods('POST')
def sum_post_method(request):
    try:
        print(request)
        a = request.GET['a']
        b = request.GET['b']
        return HttpResponse(str(int(a) + int(b)))
    except:
        return HttpResponse(status=400)




