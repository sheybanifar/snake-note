from django.shortcuts import render, redirect
from django.views.generic import ListView

from .models import Note

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    else:
        return redirect('accounts:dashboard')

class NoteListView(ListView):
    model = Note
    context_object_name = 'notes'
    template_name = 'notes/list_notes.html'
    paginate_by = 2

    def get_queryset(self):
        return self.model.note_manager.for_user(self.request)