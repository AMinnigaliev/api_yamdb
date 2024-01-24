from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from api.serializers import CommentSerializer, ReviewSerializer
from reviews.models import Comment, Review, Title


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(review=self.kwargs['review_id'])

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.kwargs['review_id'],
        )


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        return Review.objects.filter(title=title)

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.kwargs['review_id'],
        )
