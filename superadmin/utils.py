from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType


def create_log(request, model):
    action = action_for = None

    if request.method == 'POST':
        action = ADDITION
        action_for = 'added'
    if request.method == 'PUT':
        action = CHANGE
        action_for = 'edited'
    if request.method == 'DELETE':
        action = DELETION
        action_for = 'deleted'

    message = [{action_for: {'fields': [field for field in request.data.keys()]}}]

    LogEntry.objects.log_action(
        user_id=request.user.id,
        content_type_id=ContentType.objects.get_for_model(model).pk,
        change_message=message,
        object_repr=f'{request.user.id} - {action_for}: {model}',
        object_id='',
        action_flag=action)


