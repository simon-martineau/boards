from django.http import HttpRequest


class LogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        print(request.headers)
        return self.get_response(request)
