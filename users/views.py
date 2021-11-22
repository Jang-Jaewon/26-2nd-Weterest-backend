class Kakao:
    # Class = Property(Data) + Method(Action)
    def __init__(self, access_token):
        self.access_token  = access_token
        self.user_info_api = "https://kapi.kakao.com/v2/user/me"
        self.map_api       = "https://kapi.kakao.com/v2/kakao-map/address"
    
    @property
    def user_information(self):
        response = requests.get(
            self.user_info_api, 
            headers = {"Authorization": f"Bearer {self.access_token}"},
            timeout = 3
        )

        if not response.status_code == 200:
            raise Exception("ss")

        return response.json()

    def get_current_address(self, lat, lng):
        return requests.get(self.map_api + f"?latitude={lat}&logitude={lng}")

class SignUpView(View):
    def post(self, request):
        try:
            kakao        = Kakao(request.headers["Authorization"])
            kakao_user   = kakao.user_information

            user, created = User.objects.get_or_create(
                login_platform_id = kakao_user["id"],
                defaults = {
                    "email"             : kakao_user["kakao_account"]["email"],
                    "login_platform"    : "kakao",
                }
            )

            access_token = jwt.encode({"id" : user.id}, SECRET_KEY, algorithm = ALGORITHM)

            return JsonResponse({"MESSAGE":"SUCCESS", "ACCESS_TOKEN": access_token}, status=200)
            
        except KeyError:
            return JsonResponse({"MESSAGE":"KEY_ERROR"}, status=400)
