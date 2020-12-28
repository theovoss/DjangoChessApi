from django.views.generic.list import ListView

from DjangoChessApi.Chess.models import Game


class GameListView(ListView):

    context_object_name = 'my_games'
    paginate_by = 100  # if pagination is desired
    template_name = "chess/game_list.html"

    def get_queryset(self):
        return Game.objects.filter(player1=self.request.user) | Game.objects.filter(
            player1=self.request.user
        )
