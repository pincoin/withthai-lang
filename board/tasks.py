from celery import shared_task


@shared_task
def name_of_your_function(optional_param):
    print('get the task done')
