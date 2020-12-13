from background_task.tasks import autodiscover, tasks
from django.conf import settings
from django.http import HttpResponseForbidden, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


@require_POST
@csrf_exempt
def execute_background_task(request):
    key = request.META.get('HTTP_KEY')
    if not key == settings.BACKGROUND_JOB_AUTH_KEY:
        raise HttpResponseForbidden

    autodiscover()
    queue = None

    if not tasks.run_next_task(queue):
        pass

    return JsonResponse({
        'ok': True
    })
