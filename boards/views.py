import json

from django.http       import JsonResponse
from django.views      import View
from django.db.models  import Q

from .models           import Board


class BoardListView(View):
    def get(self, request):
        tag_id  = int(request.GET.get("tag_id", 0))
        keyword = request.GET.get("keyword")
        OFFSET  = int(request.GET.get("offset", 0))
        LIMIT   = int(request.GET.get("display", 25))

        q = Q()

        if tag_id:
            q.add(Q(tagboard__tag_id=tag_id), q.AND)

        if keyword:
            q.add(Q(tags__name=keyword) | Q(title__icontains=keyword), q.AND)    

        boards = Board.objects.filter(q).select_related("user").order_by("?")[OFFSET:OFFSET+LIMIT]

        result = [
            {
                "id"           : board.id,
                "user"         : board.user.nickname,
                "title"        : board.title,
                "image_url"    : board.board_image_url,
                "point_color"  : board.image_point_color,
                "image_width"  : board.image_width,
                "image_height" : board.image_height,
            }
            for board in boards
        ]

        return JsonResponse({"message": result}, status=200)

