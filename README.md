# 🌟 PROJECT_WINTEREST | 위터레스트

WINTEREST UI/UX 메인 서비스

1. 카카오 소셜 로그인 서비스를 제공합니다.
2. 사진들을 매직그리드 및 무한스크롤 기능을 통해 제공합니다.
3. WINTEREST 회원이 본인 로컬에 있는 사진을 저장하면 마이페이지에 등록합니다.
4. 원하는 카테고리를 검색하면 해당 사진들을 제공합니다.

WINTEREST API 메인 서비스

1. WINTEREST에 게시된 Pin 리스트 및 상세정보를 제공합니다.
2. WINTEREST 회원이 Pin 등록, Pin 저장, 댓글을 제공합니다.
3. WINTEREST에 등록된 Pin을 제목, 태그별로 검색하여 관련된 Pin 리스트를 한눈에 볼 수 있습니다.

- 사이트 링크 : https://www.pinterest.co.kr/

# 🚀  TEAM_WINTEREST

- 시연 영상 [링크](https://drive.google.com/file/d/1iQs4AqUM8KooI1IRBBUGhPjELsggv2hY/view?usp=sharing)
- 배포한 웹사이트 [링크](http://wecode26winterestproject.s3-website.ap-northeast-2.amazonaws.com/)

## 👫 팀원

- Front-end : 김유신, 임연수, 전창민
- Back-end : 권상현, 장재원

## 개발 기간

- 기간: 2021년 11월 15일 ~ 2021년 11월 26일(12일간)

## 적용 기술

- Front-end: JavaScript, React, React Hook, Styled-Component
- Back-end: Django, Python, MySQL, jwt, bcrypt, AWS EC2, AWS RDS, AWS S3, Docker
- 협업툴: Trello, Slack, Notion, Git, Ddiagram, Postman

## 구현 기능 및 개인 역할

> **권상현**

- KaKao Social 로그인/회원가입, 인증/인가 API 구현
- 마음에 드는 다른 사람의 Pin을 저장하는 PinBoard API 구현(토글버튼)
- 저장한 Pin을 마이페이지에서 한 번에 보는 API 구현

> **장재원**

- 메인 페이지 Pin, 유사 Pin, 검색 결과 Pin 리스트 제공 API
- Pin 상세페이지 정보, 댓글 제공 API
- S3를 연동한 Pin 등록 및 조회 API


## EndPoint : [API 명세서 링크](https://documenter.getpostman.com/view/14471334/UVJZoyY2)

[post] SignUpView(일반회원가입) : /users/signup

[post] SignInView(로그인) : /users/signin

[post] KakaoSignInView(Social로그인) : /users/signin/kakao

[get] BoardListView(메인페이지) : /boards?offset=<<int:pk>>&limit=<<int:pk>>

[get] BoardListView(유사Pinlist) : /boards?tag_id=<<int:pk>>&offset=<<int:pk>>&limit=<<int:pk>>

[get] BoardListView(검색 결과) /boards?keyword=<<srt:pk>>&offset=<<int:pk>>&limit=<<int:pk>>

[post] BoardListView(Pin 생성) : /boards

[get] BoardDetailView(Pin 상세보기) : /boards/<<int:pk>>

[get] PinListView(저장한 Pin 보기) : /boards/pin

[post] PinListView(Pin 저장) : /boards/pin?offset=<<int:pk>>&limit=<<int:pk>>

[get] MyBoardsView(생성한 Pin 보기) : /boards/board/me

## Modeling

![title](https://media.vlpt.us/images/jewon119/post/2f9995f9-5fa6-4d1c-9c1e-ae46c8ae0766/weterest.png)

## 소감 및 후기

> **권상현** : 1차 프로젝트 때는 기능구현을 위한 시간도 촉박했던 바람에 배포의 기쁨에 대해 몰랐고 이번 프로젝트 끝날 때까지도 배포에 대한 중요함을 깨닫지 못했습니다. 그런데 막상 프론트엔드와 백엔드 모두 배포에 성공하고 팀원들이 힘을 합쳐 구현한 페이지에 직접 접속해 사용해보고 느낀 감정은 이루 말할 수 없었습니다. 이게 개발자인가 싶기도 하면서 1차 프로젝트 배포에 대한 욕심이 생기기 시작했습니다. 첫 프로젝트보다 무조건 더 잘, 더 많이 하고 싶다는 욕심에 압박감도 불안감도 컸지만 우리 팀원님들, 특히 재원님 덕분에 무사히 프로젝트를 끝냈습니다! 믿고 맡기고 기다려주신 점을 비롯해 모든 것에 항상 감사드리고 사랑합니다♡ [상현님 vlog](https://velog.io/@gshduet/2ndproject)

> **장재원** : 기획 단계에서 blocker를 얼마나 인지할 수 있는지가 원활한 프로젝트 진행에 있어 얼마나 중요한 점인지 인식할 수 있었습니다. 또한 S3를 통해 이미지 업로드를 구현하고, Docker를 활용해서 backend 배포를 성공할 수 있어서 행복했습니다. 무엇보다 서로의 blocker에 대해 함께 고민하고 해결방안을 찾기 위해 노력했던 점이 팀원 간 깊은 신뢰를 만들고, 프로젝트에 높은 동기를 유지할 수 있었던 비결이었습니다. 원팀이되어 끝가지 치지않고 프로젝트를 마무리할 수 있게 해준 팀원들께 감사드립니다. [재원님 vlog](https://velog.io/@jewon119/TIL97.-Wetest-Project-2%EC%B0%A8-%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8-%ED%9A%8C%EA%B3%A0)   


## 레퍼런스

- 이 프로젝트는 <u>[핀터레스트](https://www.pinterest.com/)</u> 사이트를 참조하여 학습목적으로 만들었습니다.
- 실무수준의 프로젝트이지만 학습용으로 만들었기 때문에 이 코드를 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제될 수 있습니다.