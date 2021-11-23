import json, jwt

from django.http                    import JsonResponse
from unittest.mock                  import MagicMock, patch
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test                    import TestCase, Client
from django.conf                    import settings

from .models                        import Board, Tag, TagBoard, PinBoard, Comment
from users.models                   import User


class BoardListViewTest(TestCase):
    def setUp(self):
        user_list = [
            User(
                id                = 1,
                email             = 'test1@kakao.com',
                password          = '1q2w3e4r!',
                nickname          = 'test1',
                profile_image_url = 'test_image_url1',
                login_platform    = 'kakao',
                login_platform_id = '0000000000',
                description       = 'hi',
            ),
            User(
                id                = 2,
                email             = 'test2@kakao.com',
                password          = '1q2w3e4r!',
                nickname          = 'test2',
                profile_image_url = 'test_image_url2',
                login_platform    = 'kakao',
                login_platform_id = '1111111111',
                description       = 'hi',
            ),
            User(
                id                = 3,
                email             = 'test3@kakao.com',
                password          = '1q2w3e4r!',
                nickname          = 'test3',
                profile_image_url = 'test_image_url1',
                login_platform    = 'kakao',
                login_platform_id = '2222222222',
                description       = 'hi',
            )
        ]
        User.objects.bulk_create(user_list)
        
        user = User.objects.get(email='test1@kakao.com')
        self.token = jwt.encode({'id' : user.id}, settings.SECRET_KEY, algorithm = settings.ALGORITHM)

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

        tag_list = [
            Tag(
                id   = 1,
                name = 'nature',
            ),
            Tag(
                id   = 2,
                name = 'animal',
            ),
            Tag(
                id   = 3,
                name = 'food',
            ),
            Tag(
                id   = 4,
                name = 'car',
            ),
            Tag(
                id   = 5,
                name = 'korea',
            ),
            Tag(
                id   = 6,
                name = 'children',
            ),
            Tag(
                id   = 7,
                name = 'love',
            ),
            Tag(
                id   = 8,
                name = 'sports',
            ),
            Tag(
                id   = 9,
                name = 'movie',
            ),
            Tag(
                id   = 10,
                name = 'trip',
            ),
        ]
        Tag.objects.bulk_create(tag_list)        
        
        tagboard_list = [
            TagBoard(
                id       = 1,
                board_id = Board.objects.get(id=1).id,
                tag_id   = Tag.objects.get(id=1).id,
            ),
            TagBoard(
                id       = 2,
                board_id = Board.objects.get(id=1).id,
                tag_id   = Tag.objects.get(id=3).id,
            ),
            TagBoard(
                id       = 3,
                board_id = Board.objects.get(id=1).id,
                tag_id   = Tag.objects.get(id=2).id,
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
                description = 'test description1',
            ),
            Comment(
                id          = 2,
                user_id     = User.objects.get(id=2).id,
                board_id    = Board.objects.get(id=1).id,
                description = 'test description2',
            ),
            Comment(
                id          = 3,
                user_id     = User.objects.get(id=3).id,
                board_id    = Board.objects.get(id=2).id,
                description = 'test description3',
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

    @patch('boards.views.boto3.client')
    def test_success_board_list_view_for_create_board_post_method(self, mocked_requests):
        client = Client()

        board = {
            'title'        : 'test title',
            'description'  : 'test description',
            'source'       : 'test.com',
            'filename'     : SimpleUploadedFile(
                name         = 'test.png',
                content      = b'file_content',
                content_type = 'image/ief',
            )
        }

        class MockedResponse:
            def upload_fileobj(self):
                return None

        mocked_requests.upload_fileobj = MagicMock(return_value = MockedResponse())
        headers                        = {'HTTP_Authorization' : self.token}
        response                       = client.post('/boards', board, ContentType='multipart/form-data', **headers)

        self.assertEqual(response.json(), {'message' : 'CREATE_SUCCESS'})
        self.assertEqual(response.status_code, 201)

    @patch('boards.views.boto3.client')
    def test_fail_board_list_view_for_create_board_key_error_post_method(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def upload_fileobj(self):
                return None

        board = {
            'title'       : 'test title',
            'description' : 'test description',
            'source'      : 'test.com',
        }

        mocked_requests.upload_fileobj = MagicMock(return_value = MockedResponse())
        headers                        = {'HTTP_Authorization' : self.token}
        response                       = client.post('/boards', board, **headers)
        self.assertEqual(response.json(), {'message' : 'KEY_ERROR'})
        self.assertEqual(response.status_code, 400)