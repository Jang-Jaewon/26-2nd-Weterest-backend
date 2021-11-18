import json
from django.http    import JsonResponse

from django.test    import TestCase, Client
from .models        import Board, Tag, TagBoard, PinBoard, Comment
from users.models   import User


class BoardListViewTest(TestCase):
    def setUp(self):
        user_list = [
            User(
                id = 1,
                email             = 'test1@kakao.com',
                password          = '1q2w3e4r!',
                nickname          = 'test1',
                profile_image_url = 'test_image_url1',
                login_platform    = 'kakao',
                description       = 'hi',
            ),
            User(
                id = 2,
                email             = 'test2@kakao.com',
                password          = '1q2w3e4r!',
                nickname          = 'test2',
                profile_image_url = 'test_image_url2',
                login_platform    = 'kakao',
                description       = 'hi',
            ),
            User(
                id = 3,
                email             = 'test3@kakao.com',
                password          = '1q2w3e4r!',
                nickname          = 'test3',
                profile_image_url = 'test_image_url1',
                login_platform    = 'kakao',
                description       = 'hi',
            )
        ]
        User.objects.bulk_create(user_list)

        board_list = [
            Board(
                id = 1,
                title             = 'test title1',
                description       = 'test description1',        
                board_image_url   = 'test_url_1',
                source            = 'test1.com',
                image_point_color = '#e587a9',
                image_width       = 1600,
                image_height      = 900,    
                user_id           = User.objects.get(id=1).id,   
            ),
            Board(
                id = 2,
                title             = 'test title2',
                description       = 'test description1',        
                board_image_url   = 'test_url_2',    
                source            = 'test2.com',
                image_point_color = '#bc80fc',
                image_width       = 1600,
                image_height      = 900,   
                user_id = User.objects.get(id=2).id,   
            ),
            Board(
                id                = 3,
                title             = 'test title3',
                description       = 'test description1',        
                board_image_url   = 'test_url_3',    
                source            = 'test3.com',
                image_point_color = '#26d661',
                image_width       = 1600,
                image_height      = 900,    
                user_id           = User.objects.get(id=3).id,
            )
        ]
        Board.objects.bulk_create(board_list)
        
        tag_id = Tag.objects.create(id=1, name='nature').id
        
        tagboard_list = [
            TagBoard(
                id       = 1,
                board_id = Board.objects.get(id=1).id,
                tag_id   = tag_id,
            ),
            TagBoard(
                id       = 2,
                board_id = Board.objects.get(id=1).id,
                tag_id  = tag_id,
            ),
            TagBoard(
                id       = 3,
                board_id = Board.objects.get(id=1).id,
                tag_id   = tag_id,
            ),
        ]
        TagBoard.objects.bulk_create(tagboard_list)

        pinboard_list = [
            PinBoard(
                id       = 1,
                user_id  = User.objects.get(id=1).id,
                board_id = Board.objects.get(id=3).id,
            ),
            PinBoard(
                id       = 2,
                user_id  = User.objects.get(id=2).id,
                board_id = Board.objects.get(id=1).id,
            ),
            PinBoard(
                id       = 3,
                user_id  = User.objects.get(id=3).id,
                board_id = Board.objects.get(id=2).id,
            ),
        ]
        PinBoard.objects.bulk_create(pinboard_list)

        comment_list = [
            Comment(
                id          = 1,
                user_id     = User.objects.get(id=1).id,
                board_id    = Board.objects.get(id=3).id,
                description = "test description1",
            ),
            Comment(
                id          = 2,
                user_id     = User.objects.get(id=2).id,
                board_id    = Board.objects.get(id=1).id,
                description = "test description2",
            ),
            Comment(
                id          = 3,
                user_id     = User.objects.get(id=3).id,
                board_id    = Board.objects.get(id=2).id,
                description = "test description3",
            ),
        ]
        Comment.objects.bulk_create(comment_list)
    
    def tearDown(self):
        User.objects.all().delete()
        Board.objects.all().delete()
        Tag.objects.all().delete()
        TagBoard.objects.all().delete()
        PinBoard.objects.all().delete()
        Comment.objects.all().delete()

    def test_success_board_list_view_for_mainpage_get_method(self):
        client   = Client()
        response = client.get('/boards')

        self.assertEqual(response.status_code, 200)

    def test_success_board_list_view_for_detail_page_query_parameter(self):
        client   = Client()
        response = client.get('/boards?tag_id=1')
        self.assertEqual(response.status_code, 200)

    def test_success_board_list_view_for_search_result_query_parameter(self):
        client   = Client()
        response = client.get('/boards?keyword=nature')
        self.assertEqual(response.status_code, 200)