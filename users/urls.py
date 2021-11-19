from django.urls import path

from users.views import SignUpView, SignInView, KakaoSignInView

urlpatterns = [
    path("/signun", SignUpView.as_view()),
    path("/signin", SignInView.as_view()),
    path("/signin/kakao", KakaoSignInView.as_view()),
]