import json
from marshmallow import Schema, fields, ValidationError
from marshmallow.validate import Length, Range
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
from .models import Item, Review


@method_decorator(csrf_exempt, name='dispatch')
class AddItemView(View):
    """View для создания товара."""

    def post(self, request):
        try:
            document = json.loads(request.body)
            schema = AddItemReview(strict=True)
            valid_data = schema.load(document)
            item = Item(title=valid_data.data['title'], description=valid_data.data['description'], price=valid_data.data['price'])
            item.save()
            data = {'id': item.id}
            return JsonResponse(data, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except ValidationError as e:
            return JsonResponse({'error': e.messages}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class PostReviewView(View):
    """View для создания отзыва о товаре."""

    def post(self, request, item_id):
        try:
            document = json.loads(request.body)
            schema = PostItemReview(strict=True)
            valid_data = schema.load(document)
            review = Review(text=valid_data.data['text'], grade=valid_data.data['grade'],
                            item=Item.objects.get(pk=item_id))
            review.save()
            data = {'id': item_id}
            return JsonResponse(data, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except ValidationError as e:
            return JsonResponse({'error': e.messages}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'no such id'}, status=404)


class GetItemView(View):
    """View для получения информации о товаре.

    Помимо основной информации выдает последние отзывы о товаре, не более 5
    штук.
    """

    def get(self, request, item_id):
        try:
            entries = Review.objects.all().order_by('-id')
            item = Item.objects.get(pk=item_id)
            data = model_to_dict(item)
            data["reviews"] = []
            if len(entries) > 5:
                entries = entries[:5]
                for entry in entries:
                    data["reviews"].append(model_to_dict(entry))
            else:
                for entry in entries:
                    data["reviews"].append(model_to_dict(entry))
            return JsonResponse(data, status=200)
        except Exception as e:
            return JsonResponse({'error': 'no such id'}, status=404)


class AddItemReview(Schema):
    title = fields.Str(validate=Length(1, 64), required=True)
    description = fields.Str(validate=Length(1, 1024), required=True)
    price = fields.Int(validate=Range(1, 1000000), required=True)


class PostItemReview(Schema):
    text = fields.Str(validate=Length(1, 1024), required=True)
    grade = fields.Int(validate=Range(1, 10), required=True)
