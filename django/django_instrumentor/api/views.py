from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def root(request):
    return JsonResponse({"message": "Welcome to the API"})

@csrf_exempt
def get_item(request, item_id):
    if item_id == 0:
        return JsonResponse({"error": "Item not found"}, status=404)
    return JsonResponse({"item_id": item_id, "name": f"Item {item_id}"})

@csrf_exempt
def create_item(request):
    if request.method == "POST":
        data = json.loads(request.body)
        if data.get("price", 0) <= 0:
            return JsonResponse({"error": "Price must be positive"}, status=400)
        return JsonResponse({"message": "Item created", "item": data})
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def update_item(request, item_id):
    if request.method in ["PUT", "PATCH"]:
        data = json.loads(request.body)
        if item_id == 0:
            return JsonResponse({"error": "Item not found"}, status=404)
        if data.get("price", 0) <= 0:
            return JsonResponse({"error": "Price must be positive"}, status=400)
        return JsonResponse({"message": "Item updated", "item_id": item_id, "item": data})
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def delete_item(request, item_id):
    if request.method == "DELETE":
        if item_id == 0:
            return JsonResponse({"error": "Item not found"}, status=404)
        return JsonResponse({"message": f"Item {item_id} deleted"})
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def server_error(request):
    return JsonResponse({"error": "Internal Server Error"}, status=500)

@csrf_exempt
def handle_redirect(request):
    return JsonResponse({"message": "This should redirect to another URL"}, status=301)
