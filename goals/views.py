from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions, filters
from rest_framework.pagination import LimitOffsetPagination

from goals.filters import GoalDateFilter
from goals.models import GoalCategory, Goal, GoalComment, Board
from goals.permissions import BoardPermissions, GoalCategoryPermissions, GoalPermissions, CommentPermissions
from goals.serializers import GoalCreateSerializer, GoalCategorySerializer, GoalCategoryCreateSerializer, \
    GoalSerializer, CommentCreateSerializer, CommentSerializer, BoardSerializer, BoardCreateSerializer, \
    BoardListSerializer


class BoardListView(ListAPIView):
    """Список досок"""
    model = Board
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LimitOffsetPagination
    serializer_class = BoardListSerializer
    filter_backends = [
        filters.OrderingFilter,
    ]
    ordering = ["title"]

    def get_queryset(self):
        return Board.objects.filter(
            participants__user=self.request.user, is_deleted=False
        )


class BoardCreateView(CreateAPIView):
    """Создание доски"""
    model = Board
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoardCreateSerializer


class BoardView(RetrieveUpdateDestroyAPIView):
    """Представление доски"""
    model = Board
    permission_classes = [permissions.IsAuthenticated, BoardPermissions]
    serializer_class = BoardSerializer

    def get_queryset(self):
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance: Board):
        # При удалении доски помечаем ее как is_deleted,
        # «удаляем» категории, обновляем статус целей
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(
                status=Goal.Status.archived
            )
        return instance


class GoalCategoryCreateView(CreateAPIView):
    """Создание категории целей"""
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(ListAPIView):
    """Список категорий целей"""
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = ["board", "user"]
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]

    def get_queryset(self):
        return GoalCategory.objects.filter(
            board__participants__user=self.request.user, is_deleted=False
        )


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    """Представление категории целей"""
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [permissions.IsAuthenticated, GoalCategoryPermissions]

    def get_queryset(self):
        return GoalCategory.objects.filter(
            board__participants__user=self.request.user, is_deleted=False
        )

    def perform_destroy(self, instance):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            Goal.objects.filter(category=instance).update(status=Goal.Status.archived)
        return instance


class GoalCreateView(CreateAPIView):
    """Создание цели"""
    model = Goal
    serializer_class = GoalCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class GoalView(RetrieveUpdateDestroyAPIView):
    """Представление цели"""
    model = Goal
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated, GoalPermissions]

    def get_queryset(self):
        return Goal.objects.filter(
            category__board__participants__user=self.request.user
        )

    def perform_destroy(self, instance):
        instance.status = Goal.Status.archived
        instance.save()
        return instance


class GoalListView(ListAPIView):
    """Список целей"""
    model = Goal
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = GoalDateFilter
    search_fields = ["title"]
    ordering_fields = ["title", "created"]
    ordering = ["title"]

    def get_queryset(self):
        return Goal.objects.filter(
            category__board__participants__user=self.request.user
        )


class CommentCreateView(CreateAPIView):
    """Создание комментария"""
    model = GoalComment
    serializer_class = CommentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class CommentView(RetrieveUpdateDestroyAPIView):
    """Представление комментария"""
    model = GoalComment
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, CommentPermissions]

    def get_queryset(self):
        return GoalComment.objects.filter(
            goal__category__board__participants__user=self.request.user
        )


class CommentListView(ListAPIView):
    """Список комментариев"""
    model = GoalComment
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = ["goal"]
    ordering = ["-created"]

    def get_queryset(self):
        return GoalComment.objects.filter(
            goal__category__board__participants__user=self.request.user
        )
