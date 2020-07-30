from django.http import JsonResponse
from django.views.generic import View


class BaseView(View):
    @staticmethod
    def response(data={}, message="", status=200):
        result = {
            'data': data,
            'message': message,
        }

        return JsonResponse(result, status=status)

    @staticmethod
    def listResponse(num=0, data={}, message="", status=200):
        result = {
            'num': num,
            'data': data,
            'message': message,
        }

        return JsonResponse(result, status=status)
