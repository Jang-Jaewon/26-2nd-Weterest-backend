import json
import random
import boto3

from uuid              import uuid4

from django.http       import JsonResponse
from django.views      import View
from django.db.models  import Q
from django.conf       import settings

from .models           import Board, Tag, Comment, PinBoard
from users.models      import User
from core.utils        import login_decorator


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

    @login_decorator
    def post(self, request):
        try:
            title             = request.POST['title']
            description       = request.POST['description']
            source            = request.POST['source']
            image             = request.FILES['filename']
            colors            = ['#FFF0E5', '#66C4FF', '#C3C5CB', '#AEE938', '#FFFAE5', '#FFF5FF', '#BE1809', '#FF8C00', '#E0E0E0', '#3A10E5']
            image_width       = 252
            image_height      = [252, 200, 500]
            
            upload_key        = str(uuid4().hex[:10]) + image.name

            s3_client = boto3.client(
               "s3",
                aws_access_key_id     = settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY
            )

            s3_client.upload_fileobj(
                image,
                settings.AWS_STORAGE_BUCKET_NAME,
                upload_key,
                ExtraArgs={
                    "ContentType": image.content_type
                }
            )

            board_image_url   = "https://weterest.s3.ap-northeast-2.amazonaws.com/"+upload_key
            image_point_color = random.choice(colors)
            user              = User.objects.get(id=request.user.id)
            tag_id            = random.randint(1,10)
            image_height      = random.choice(image_height)

            board = Board.objects.create(
                title             = title,
                description       = description,
                board_image_url   = board_image_url,
                source            = source,
                image_point_color = image_point_color,
                image_width       = image_width,
                image_height      = image_height,
                user              = user,
            )
            tag = Tag.objects.get(id=tag_id)
            board.tags.add(tag)
            board.save()
            
            return JsonResponse({'message':'CREATE_SUCCESS'}, status = 201)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)


class PinListView(View):
    @login_decorator
    def post(self, request):
        data     = json.loads(request.body)
        user_id  = request.user.id
        board_id = data["board_id"]

        pin_board, created = PinBoard.objects.get_or_create(
            user_id  = user_id,
            board_id = board_id
        )

        if not created:
            pin_board.delete()
            return JsonResponse({"message" : "NO CONTENTS"}, status = 204)

        return JsonResponse({"message" : "CREATE_SUCCESS"}, status = 201)

    @login_decorator
    def get(self, request):
        OFFSET  = int(request.GET.get("offset", 0))
        LIMIT   = int(request.GET.get("limit", 25))

        user   = request.user
        boards = user.pined_boards.all()[OFFSET:OFFSET+LIMIT]

        results = [
            {
                "id"           : board.id,
                "nickname"     : user.nickname,
                "title"        : board.title,
                "image_url"    : board.board_image_url,
                "point_color"  : board.image_point_color,
                "image_width"  : board.image_width,
                "image_height" : board.image_height,
            } for board in boards
        ]

        if len(results) == 0:
            return JsonResponse({"message" : "No Pin", "pined_boards" : results}, status=400)

        return JsonResponse({"pined_boards" : results}, status=200)


class MyBoardsView(View):
    @login_decorator
    def get(self, request):
        user   = request.user

        if not user.board_set.all().exists():
            return JsonResponse({"message": "DOSE_NOT_EXIST_CREATE_BOARD"}, status=404)

        boards = user.board_set.all().order_by("create_time")

        result = [
            {
                "id"           : board.id,
                "user"         : user.nickname,
                "title"        : board.title,
                "image_url"    : board.board_image_url,
                "point_color"  : board.image_point_color,
                "image_width"  : board.image_width,
                "image_height" : board.image_height,
            }
            for board in boards
        ]

        return JsonResponse({"message": result}, status=200)


class BoardDetailView(View):
    def get(self, request, board_id):
        try:
            board    = Board.objects.prefetch_related("comment_set", "comment_set__user").get(id = board_id)

            result = {
                "board_info" : {
                    "id"              : board.id,
                    "title"           : board.title,
                    "description"     : board.description,
                    "board_image_url" : board.board_image_url,
                    "source"          : board.source,
                    "username"        : board.user.nickname,
                    "tag_id"          : board.tags.first().id
                },
                "comments"   : [
                    {
                        "id"                : comment.id,
                        "username"          : comment.user.nickname,
                        "profile_image_url" : comment.user.profile_image_url,
                        "description"       : comment.description,
                    }
                    for comment in board.comment_set.all()
                ]
            }
        
            return JsonResponse({"message" : result}, status=200)

        except Board.DoesNotExist:
            return JsonResponse({"message" : "DOES_NOT_EXISTS"}, status=404)
