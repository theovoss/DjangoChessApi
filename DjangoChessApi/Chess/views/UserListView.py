from django.db.models import Count
from django.utils import timezone
from django.views.generic.list import ListView

from DjangoChessApi.Chess.models import User


class UserListView(ListView):
    model = User
    context_object_name = 'users'
    paginate_by = 100  # if pagination is desired

    def get_template_names(self):
        return ['chess/user_list.html']

    def get_queryset(self):
        return User.objects.annotate(count=Count('gametype__id')).order_by('-count')
