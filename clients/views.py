from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.views.generic import ListView, DetailView
from .models import models
from .models import Client, Comment
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

class ClientListView(LoginRequiredMixin,ListView):
    model = Client
    template_name = 'client_list.html'

class ClientDetailView(LoginRequiredMixin,DetailView):
    model = Client
    template_name = 'client_detail.html'
    login_url = 'login'

class ClientUpdateView(LoginRequiredMixin,UpdateView):
    model = Client
    fields = ('name', 'notes', 'address', 'city', 'state', 'zipcode', 'email', 'cell_phone', 'acct_number')
    template_name = 'client_edit.html'

class ClientDeleteView(LoginRequiredMixin,DeleteView):
    model = Client
    template_name = 'client_delete.html'
    success_url = reverse_lazy('client_list')

class ClientCreateView(LoginRequiredMixin,CreateView):
    model = Client
    template_name = 'client_new.html'
    fields = ('name', 'notes', 'address', 'city', 'state', 'zipcode', 'email', 'cell_phone', 'acct_number')
    login_url = 'login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class CommentCreateView(LoginRequiredMixin,CreateView):
    model = Comment
    template_name = 'comment_new.html'
    fields = ('comment',)
    login_url = 'login'
    success_url = reverse_lazy('client_list')

    def form_valid(self, form):
        #default author to currently signed in user
        form.instance.author = self.request.user
        
        #make sure we are adding the comment to the client provided by pk
        foundClient = Client.objects.get(pk = self.kwargs['pk'])
        form.instance.client = foundClient

        return super().form_valid(form)
