from django.shortcuts import render


def massagemenu(request):
    return render(request, 'pages/menu.html')

def items(request):
    return render(request, 'pages/items.html')

def information(request):
    return render(request, 'pages/information.html')




