from django.views.generic.list import ListView

from DjangoChessApi.Chess.models import GameType


class UserGameTypeListView(ListView):

    context_object_name = 'game_types'
    paginate_by = 100  # if pagination is desired

    def get_queryset(self):
        print(self.request)
        return GameType.objects.filter(created_by=self.request.user)

    def get_template_names(self):
        return ['chess/user_gametype_list.html']
