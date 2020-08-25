import json
import datetime

from django.http import JsonResponse
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .models import Reservations


@method_decorator(csrf_exempt, name='dispatch')
class ReservationsView(View):
    def post(self, request, post_id):
        try:
            data = json.loads(request.body)

            Reservations().save()

        except KeyError:
            return JsonResponse({'message': 'fail'}, status=400)

        return JsonResponse({'message': 'true'}, status=200)

    def get(self, request, post_id, reservation_id):
        try:
            reservation = Reservations.objects.get(
                pk=reservation_id, is_active=True)

        except Reservations.DoesNotExist:
            return JsonResponse({'message': f'{reservation_id}번에 해당하는 reservation이 존재하지 않습니다. '}, status=400)

        return JsonResponse({'id': reservation.pk, 'title': reservation.title, 'created_date': reservation.created_date}, status=200)

    def put(self, request,  post_id, reservation_id):
        try:
            reservation = Reservations.objects.get(
                pk=reservation_id, is_active=True)

            data = json.loads(request.body)

            Reservations.objects.filter(
                pk=reservation_id, is_active=True).update(**data)

            Reservations.objects.filter(
                pk=reservation_id, is_active=True).update(updated_date=datetime.datetime.now())

            new_reseration = Reservations.objects.get(
                pk=reservation_id, is_active=True)
        except Reservations.DoesNotExist:
            return JsonResponse({'message':  f'{reservation_id}번에 해당하는 reservation이 존재하지 않습니다. '}, status=400)

        return JsonResponse({'id': new_reseration.pk, 'title': new_reseration.title,
                             'created_date': new_reseration.created_date, 'updated_date': new_reseration.updated_date}, status=200)

    def delete(self, request, post_id, reservation_id):
        try:
            if not Reservations.objects.filter(pk=reservation_id, is_active=True).exist():
                return JsonResponse({'message':  f'{reservation_id}번에 해당하는 reservation이 존재하지 않습니다. '}, status=400)

            Reservations.objects.filter(
                pk=reservation_id, is_active=True).update(is_active=False)

        except Reservations.DoesNotExist:
            return JsonResponse({'message':  f'{reservation_id}번에 해당하는 reservation이 존재하지 않습니다. '}, status=400)

        return JsonResponse({'message': 'true'}, status=200)
