from .models import SiteStats

class VisitorCounterMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.session.get("visited"):
            stats, created = SiteStats.objects.get_or_create(id=1)
            stats.total_visitors += 1
            stats.save()
            request.session["visited"] = True

        response = self.get_response(request)
        return response
