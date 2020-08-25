import json
import datetime

from .models import ContentsPosts

from django.http import JsonResponse
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name='dispatch')
class ContentsPostsView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            ContentsPosts(title=data['title'], price=data['price'], max_num=data['max_num'],
                          introduction=data['introduction'], policy=data['policy'],
                          start_time=data['start_time'], end_time=data['end_time']).save()

        except KeyError:
            return JsonResponse({'message': 'fail'}, status=400)

        return JsonResponse({'message': 'true'}, status=200)

    def get(self, request, id):
        try:
            post = ContentsPosts.objects.get(pk=id, is_active=True)

        except ContentsPosts.DoesNotExist:
            return JsonResponse({'message': f'{id}번에 해당하는 post가 존재하지 않습니다. '}, status=400)

        return JsonResponse({'id': post.pk, 'title': post.title, 'created_date': post.created_date}, status=200)

    def put(self, request, id):
        try:
            post = ContentsPosts.objects.get(pk=id, is_active=True)

            data = json.loads(request.body)

            ContentsPosts.objects.filter(
                pk=id, is_active=True).update(**data)

            ContentsPosts.objects.filter(
                pk=id, is_active=True).update(updated_date=datetime.datetime.now())

            new_post = ContentsPosts.objects.get(pk=id, is_active=True)
        except ContentsPosts.DoesNotExist:
            return JsonResponse({'message': f'{id}번에 해당하는 post가 존재하지 않습니다. '}, status=400)

        return JsonResponse({'id': new_post.pk, 'title': new_post.title,
                             'created_date': new_post.created_date, 'updated_date': new_post.updated_date}, status=200)

    def delete(self, request, id):
        try:
            post = ContentsPosts.objects.get(pk=id, is_active=True)

            ContentsPosts.objects.filter(
                pk=id, is_active=True).update(is_active=False)

        except ContentsPosts.DoesNotExist:
            return JsonResponse({'message': f'{id}번에 해당하는 post가 존재하지 않습니다. '}, status=400)

        return JsonResponse({'message': 'true'}, status=200)
