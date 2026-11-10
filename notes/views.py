from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

from .models import Note

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    else:
        return redirect('accounts:dashboard')

class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    context_object_name = 'notes'
    template_name = 'notes/list_notes.html'
    paginate_by = 2

    def get_queryset(self):
        return self.model.note_manager.for_user(self.request)

class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    fields = ['title', 'body', 'category']
    template_name = 'notes/create_note.html'
    success_url = reverse('notes:note_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)