from django.shortcuts import render
from django import template
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


register = template.Library()


@register.filter
def lower(value):
    return value.lower()


@csrf_exempt
def echo(request):
    if 'HTTP_X_PRINT_STATEMENT' in request.META:
        z = request.META['HTTP_X_PRINT_STATEMENT']
    else:
        z = 'empty'
    return render(request, 'echo.html', context={
        'a': request.GET.get('a', None),
        'b': request.GET.get('b', None),
        'c': request.GET.get('b', None),
        'd': request.GET.get('b', None),
        'method_name': request.method,
        'z': z
    })


def filters(request):
    return render(request, 'filters.html', context={
        'a': request.GET.get('a', 1),
        'b': request.GET.get('b', 1)
    })


def extend(request):
    return render(request, 'extend.html', context={
        'a': request.GET.get('a'),
        'b': request.GET.get('b')
    })
