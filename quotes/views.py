import random
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from django.http import JsonResponse
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Quote, SiteStats
from .forms import QuoteForm

def random_quote(request):
    total_weight = Quote.objects.aggregate(Sum("weight"))["weight__sum"] or 0
    stats = SiteStats.objects.first()
    total_visitors = stats.total_visitors if stats else 0

    if total_weight == 0:
        return render(request, "quotes/random.html", {"quote": None, "total_visitors": total_visitors})

    rnd = random.randint(1, total_weight)
    cumulative = 0
    for q in Quote.objects.all():
        cumulative += q.weight
        if rnd <= cumulative:
            session_key_view = f"viewed_quote_{q.id}"
            if not request.session.get(session_key_view, False):
                q.views += 1
                q.save(update_fields=["views"])
                request.session[session_key_view] = True

            voted = request.session.get(f"voted_quote_{q.id}", None)

            return render(request, "quotes/random.html", {
                "quote": q,
                "voted": voted,
                "total_visitors": total_visitors
            })

    return render(request, "quotes/random.html", {"quote": None, "total_visitors": total_visitors})


def vote_ajax(request, quote_id, action):
    q = get_object_or_404(Quote, id=quote_id)
    session_key = f"voted_quote_{q.id}"
    voted = request.session.get(session_key, None)

    if action not in ["like", "dislike"]:
        return JsonResponse({"error": "Invalid action"}, status=400)

    if voted == action:
        if action == "like":
            q.likes = max(q.likes - 1, 0)
        else:
            q.dislikes = max(q.dislikes - 1, 0)
        request.session[session_key] = None
    else:
        if voted == "like":
            q.likes = max(q.likes - 1, 0)
        elif voted == "dislike":
            q.dislikes = max(q.dislikes - 1, 0)

        if action == "like":
            q.likes += 1
        else:
            q.dislikes += 1
        request.session[session_key] = action

    q.save(update_fields=["likes", "dislikes"])
    return JsonResponse({
        "likes": q.likes,
        "dislikes": q.dislikes,
        "voted": request.session[session_key]
    })


def top_quotes(request):
    quotes = Quote.objects.order_by("-likes")[:10]
    stats = SiteStats.objects.first()
    total_visitors = stats.total_visitors if stats else 0
    return render(request, "quotes/top.html", {"quotes": quotes, "total_visitors": total_visitors})



class QuoteCreateView(CreateView):
    model = Quote
    form_class = QuoteForm
    template_name = "quotes/add_quote.html"
    success_url = reverse_lazy("random_quote")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stats = SiteStats.objects.first()
        context["total_visitors"] = stats.total_visitors if stats else 0
        return context
