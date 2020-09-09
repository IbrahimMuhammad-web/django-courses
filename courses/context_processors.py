from .models import Topic


def head_menu(request):
    topics = Topic.objects.filter(topic_is_active='Yes')
    context = {
        'topics': topics
    }
    return context