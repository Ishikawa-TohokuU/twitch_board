from django.urls import path
from .views import (TopView,
                    StreamView,
                    )

urlpatterns = [
  path("", TopView, name="board-top"),
  # path("detail/<int:pk>/", NippoDetailView.as_view(), name="nippo-detail"),
  path("streams/", StreamView.as_view(), name="board-streams"),
  # path("detail/<int:pk>/", nippoDetailView, name="nippo-detail"),

  # path("create/", NippoCreateFormView.as_view(), name="nippo-create"),
  # path("create/", nippoCreateView, name="nippo-create"),
  # path("update/<int:pk>", NippoUpdateModelFormView.as_view(), name="nippo-update"),
  # path("update/<int:pk>", nippoUpdateFormView, name="nippo-update"),
  # path("delete/<int:pk>/", NippoDeleteView.as_view(), name="nippo-delete"),
  # path("delete/<int:pk>/", nippoDeleteView, name="nippo-delete"),

  # path("twitchapi/", TwitchApi, name="nippo-twitchapi"),
]