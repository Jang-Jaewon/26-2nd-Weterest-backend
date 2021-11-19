import json, re, bcrypt, jwt, requests

from django.http      import JsonResponse
from django.views     import View

from config.settings  import SECRET_KEY, ALGORITHM
from users.models     import User

class SignUpView(View):
    def post(self, request):
        try:
            data              = json.loads(request.body)
            email             = data["email"]
            password          = data["password"]
            nickname          = data["nickname"]
            profile_image_url = data["profile_image_url"]
            description       = data["description"]
            login_platform    = "None"
            login_platform_id = "None"

            if not re.match("^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
                return JsonResponse({"MESSAGE" : "INVALD_EMAIL"}, status=400)
            
            if not re.match("^(?=.*[A-Za-z])(?=.*\d)(?=.*[?!@#$%*&])[A-Za-z\d?!@#$%*&]{8,}$", password):
                return JsonResponse({"MESSAGE" : "INVALD_PASSWORD"}, status=400)
        
            if User.objects.filter(email=email).exists():
                return JsonResponse({"MESSAGE" : "EMAIL_EXISTS"}, status=400)

            hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

            User.objects.create(
                email             = email,
                password          = hashed_password,
                nickname          = nickname,
                profile_image_url = profile_image_url,
                description       = description,
                login_platform    = login_platform,
                login_platform_id = login_platform_id,
            )        
            return JsonResponse({"MESSAGE" : "SUCCESS"}, status=201)
       
        except KeyError:
            return JsonResponse({"MESSAGE" : "KEY_ERROR"}, status=400)

class SignInView(View):
    def post(self, request):
        try:
            data        = json.loads(request.body)
            email       = data["email"]
            password    = data["password"]
            user        = User.objects.get(email=email)

            if not bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
                return JsonResponse({"MESSAGE":"INVALID_USER"}, status=401)

            access_token = jwt.encode({"id" : user.id}, SECRET_KEY, algorithm = ALGORITHM)
            return JsonResponse({"MESSAGE":"SUCCESS", "ACCESS_TOKEN": access_token}, status=200)

        except KeyError:
            return JsonResponse({"MESSAGE":"KEY_ERROR"}, status=400)

        except User.DoesNotExist:
            return JsonResponse({"MESSAGE":"USER_DOES_NOT_EXIST"}, status=404)

class Kakao:
    # Class = Property(Data) + Method(Action)
    def __init__(self, access_token):
        self.access_token  = access_token
        self.user_info_api = "https://kapi.kakao.com/v2/user/me"
    
    @property
    def user_information(self):
        response = requests.get(
            self.user_info_api, 
            headers = {"Authorization": f"Bearer {self.access_token}"},
            timeout = 3
        )

        if not response.status_code == 200:
            raise Exception("INVALID_TOKEN")

        return response.json()

class KakaoSignInView(View):
    def post(self, request):
        try:
            kakao        = Kakao(request.headers["Authorization"])
            kakao_user   = kakao.user_information

            user, created = User.objects.get_or_create(
                login_platform_id = kakao_user["id"],
                defaults = {
                    "email"             : kakao_user["kakao_account"]["email"],
                    "nickname"          : kakao_user["kakao_account"]["profile"]["nickname"],
                    "profile_image_url" : kakao_user["kakao_account"]["profile"]["profile_image_url"],
                    "login_platform"    : "kakao",
                }
            )

            access_token = jwt.encode({"id" : user.id}, SECRET_KEY, algorithm = ALGORITHM)

            return JsonResponse({"MESSAGE":"SUCCESS", "ACCESS_TOKEN": access_token}, status=200)
            
        except KeyError:
            return JsonResponse({"MESSAGE":"KEY_ERROR"}, status=400)
