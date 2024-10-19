from django.shortcuts import render


def base_coordinador(request):
    return render(request, 'base_coordinador.html')