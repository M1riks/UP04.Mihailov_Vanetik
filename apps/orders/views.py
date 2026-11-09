from django.http import JsonResponse

# Заглушки для обработчиков, чтобы Django не ругался при запуске
def order_list(request):
    return JsonResponse({"status": "order list"})

def order_create(request):
    return JsonResponse({"status": "order create"})

def order_detail(request, pk):
    return JsonResponse({"status": f"order {pk} detail"})

def order_complete(request, pk):
    return JsonResponse({"status": f"order {pk} completed"})

def order_cancel(request, pk):
    return JsonResponse({"status": f"order {pk} canceled"})
