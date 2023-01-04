from collections import OrderedDict
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import PostViewSet
from .models import Post
from account.models import User


class PostTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        user = User.objects.create_user(email='test@gmail.com', password='12345678')
        posts = [
            Post(author=user, body='new post'),
            Post(author=user, body='2 post'),
            Post(author=user, body='hello world')
        ]
        Post.objects.bulk_create(posts)

    def test_list(self):
        request = self.factory.get('/posts/')
        view = PostViewSet.as_view({'get': 'list'})
        response = view(request)

        assert response.status_code == 200
        assert type(response.data) == ReturnList
        assert len(response.data) == 3
        assert type(response.data[0]) == OrderedDict
        assert response.data[0]['body'] == 'new post'

    def test_retrieve(self):
        id = Post.objects.all()[0].id
        request = self.factory.get(f'/posts/{id}/') # хз почему он по несколько раз создает и удаляет их
        view = PostViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk=id)

        assert response.status_code == 200
        assert type(response.data) == ReturnDict
        assert response.data['body'] == 'new post'

    def test_auth(self):
        data = {
            'body':'new new new'
        }
        request = self.factory.post('/posts/', data, format='json')
        view = PostViewSet.as_view({'post':'create'})
        response = view(request)

        assert response.status_code == 401
    
    def test_create(self):
        user = User.objects.all()[0]
        data = {
            'body':'new new new'
        }
        request = self.factory.post('/posts/', data, format='json')
        force_authenticate(request, user)
        view = PostViewSet.as_view({'post':'create'})
        response = view(request)

        assert response.status_code == 201
        assert response.data['body'] == data['body']
        assert response.data['author'] == user.id
        assert Post.objects.filter(author=user, body=data['body']).exists()
    
    def test_update(self):
        user = User.objects.all()[0]
        data = {
            'body':'updated body'
        }
        post = Post.objects.all()[2]
        request = self.factory.patch(f'/posts/{post.id}', data, format='json')
        force_authenticate(request, user)
        view = PostViewSet.as_view({'patch':'partial_update'})
        response = view(request, pk=post.id)

        assert response.status_code == 200
        assert Post.objects.get(id=post.id).body == data['body']

    def test_delete(self):
        user = User.objects.all()[0]
        post = Post.objects.all()[2]
        request = self.factory.delete(f'/posts/{post.id}')
        force_authenticate(request, user)
        view = PostViewSet.as_view({'delete':'destroy'})
        response = view(request, pk=post.id)

        assert response.status_code == 204
        assert not Post.objects.filter(id=post.id).exists()
