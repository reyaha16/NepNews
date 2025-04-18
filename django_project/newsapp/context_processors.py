from .models import Category

def base_context(request):
    return {'categories': Category.objects.all()}