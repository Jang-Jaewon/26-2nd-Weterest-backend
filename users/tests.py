import jwt

from unittest.mock import MagicMock, patch
from django.test   import TestCase, Client

from users.models  import User
from config.settings  import SECRET_KEY, ALGORITHM

class KaKaoSigninTest(TestCase):
    def setUp(self):
        User.objects.create(
            login_platform_id = 19999999,
            id                = 51,
            email             = "cckdals111@naver.com",
            nickname          = "전창민",
            profile_image_url = "http://k.kakaocdn.net/dn/b0BA8U/btqBtLuo0mm/2yYEyfr2pc7JfscHJ8MHuk/img_640x640.jpg",
            login_platform    = "kakao"
        )

    def tearDown(self) :
        User.objects.all().delete()

    @patch("users.views.requests")
    def test_success_kakao_signin_already_exist_user(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
                    "id" : 19999999, 
                    "kakao_account": {
                        "email"    : "cckdals111@naver.com",
                        "profile"  : {
                            "nickname"          : "전창민",
                            "profile_image_url" : "http://k.kakaocdn.net/dn/b0BA8U/btqBtLuo0mm/2yYEyfr2pc7JfscHJ8MHuk/img_640x640.jpg"
                        }
                    },
                    "login_platform" : "kakao"
                }

        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {"HTTP_Authorization": "fake_access_token1"}
        response            = client.get("/users/signin", **headers)
        access_token        = jwt.encode({"id" : 51}, SECRET_KEY, algorithm = ALGORITHM)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"MESSAGE":"SUCCESS", "ACCESS_TOKEN": access_token})

    @patch("users.views.requests")
    def test_success_kakao_signup_user_and_signin_him(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
                    "id" : 20000000,
                    "kakao_account": {
                        "email"    : "cckdals111@gmail.com",
                        "profile"  : {
                            "nickname"          : "창민",
                            "profile_image_url" : "https://images.unsplash.com/photo-1440404653325-ab127d49abc1?crop=entropy&cs=tinysrgb&fit=crop&fm=jpg&h=900&ixid=MnwxfDB8MXxyYW5kb218MHx8bW92aWV8fHx8fHwxNjM3MTM4MzY3&ixlib=rb-1.2.1&q=80&utm_campaign=api-credit&utm_medium=referral&utm_source=unsplash_source&w=1600"
                        }
                    },
                    "login_platform" : "kakao"
                }

        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {"HTTP_Authorization": "fake_access_token1"}
        response            = client.get("/users/signin", **headers)
        access_token        = jwt.encode({"id" : 52}, SECRET_KEY, algorithm = ALGORITHM)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"MESSAGE":"SUCCESS", "ACCESS_TOKEN": access_token})

    @patch("users.views.requests")
    def test_failure_get_kakao_access_token(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
                    "msg": "this kakao access token does not exist",
                    "code": -401
                }

        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {"HTTP_Authorization": "fake_access_token2"}
        response            = client.get("/users/signin", **headers)
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"MESSAGE":"INVALID_TOKEN"})

    @patch("users.views.requests")
    def test_failure_kakao_signin_from_key_error(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
                    "msg": "KEY_ERROR",
                    "code": 400
                }

        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {"HTTP_Authorization": "fake_access_token3"}
        response            = client.get("/users/signin", **headers)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"MESSAGE":"KEY_ERROR"})