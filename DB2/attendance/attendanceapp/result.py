from celery.result import AsyncResult
from django.conf import settings

def check_task(task_id):
    result = AsyncResult(task_id)
    if result.ready():
        return {'status':200,'task':'found','result':result.result}
    else:
        return {'status':404,'task':'not found','result':result.result}