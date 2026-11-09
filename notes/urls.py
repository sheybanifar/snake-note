from django.urls import path

from . import views

app_name = 'notes'

urlpatterns = [
    path('notes/', views.NoteListView.as_view(), name='note_list'),
    path('note/create/', ),
]