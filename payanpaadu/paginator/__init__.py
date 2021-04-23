from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginate_queryset(request, queryset, limit):
    paginator = Paginator(queryset, limit)
    page = request.GET.get('page', 1)
    try:
        return paginator.page(page)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)
