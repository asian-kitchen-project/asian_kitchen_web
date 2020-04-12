# dbsite/context_processors.py

from django.db.models import Count, Q

from delivery.models import Category


def common(request):
    context = {
        'categories': Category.objects.annotate(
            num_foods=Count('food', filter=Q(food__is_sale=True))),
    }
    return context
