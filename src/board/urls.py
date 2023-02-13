from django.urls import path
from .views import (TopView,
                    StreamView,
                    StreamDetailView,
                    ArchiveView,
                    StreamerView,
                    StreamerDetailView,
                    CommentCreateFormView,
                    )

urlpatterns = [
  path("", TopView, name="board-top"),
  # path("streams/<int:pk>/", StreamDetailView.as_view(), name="board-detail"),
  path("streams/<int:pk>/", StreamDetailView, name="board-detail"),
  path("streams/", StreamView.as_view(), name="board-streams"),
  path("archives/", ArchiveView.as_view(), name="board-archives"),
  path("streamers/", StreamerView.as_view(), name="board-streamers"),
  path("streamers/<int:pk>/", StreamerDetailView.as_view(), name="board-streamersdetail"),
  path("comment/<int:pk>/", CommentCreateFormView.as_view(), name="board-commentform"),
  # path("detail/<int:pk>/", nippoDetailView, name="nippo-detail"),

  # path("create/", NippoCreateFormView.as_view(), name="nippo-create"),
  # path("create/", nippoCreateView, name="nippo-create"),
  # path("update/<int:pk>", NippoUpdateModelFormView.as_view(), name="nippo-update"),
  # path("update/<int:pk>", nippoUpdateFormView, name="nippo-update"),
  # path("delete/<int:pk>/", NippoDeleteView.as_view(), name="nippo-delete"),
  # path("delete/<int:pk>/", nippoDeleteView, name="nippo-delete"),

  # path("twitchapi/", TwitchApi, name="nippo-twitchapi"),
]