from django.urls import path
from . import views

app_name = 'bulletin'
urlpatterns = [
    # 기본 페이지
    path('', views.board, name='board'),
    # 해당 post_id 게시글
    path('<int:post_id>/', views.post),
    # 글쓰기
    path('upload/', views.upload, name='upload'),
	# 수정, 삭제
    path('<int:post_id>/modify/', views.modify, name='modify'),
    path('<int:post_id>/delete/', views.delete, name='delete'),    
]