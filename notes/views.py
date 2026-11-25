from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy

from .models import Note
from .forms import NoteCreateForm

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
        return self.model.note_manager.for_user(self.request.user)

class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    form_class = NoteCreateForm
    template_name = 'notes/create_note.html'
    success_url = reverse_lazy('notes:note_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user

        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class NoteDetailView(LoginRequiredMixin, DetailView):
    model = Note
    template_name = 'notes/note_detail.html'

    def get_queryset(self):
        return self.model.note_manager.for_user(user=self.request.user)

class NoteUpdateView(LoginRequiredMixin, UpdateView):
    pass