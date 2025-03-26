from django.contrib.auth import get_user
from django.contrib.messages.context_processors import messages
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404

# Create your views here.
from  django.contrib.auth.mixins import (LoginRequiredMixin, PermissionRequiredMixin)
from . import models
from django.urls import reverse
from django.views import generic
from django.contrib import messages
from django.shortcuts import get_object_or_404
from groups.models import Group, GroupMember

class CreateGroup(LoginRequiredMixin, generic.CreateView):
    fields = ('name', 'description')
    model = Group

class SingleGroup(LoginRequiredMixin, generic.DetailView):
    model = Group

class ListGroups(LoginRequiredMixin, generic.ListView):
    model = Group


class JoinGroup(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single', kwargs={'slug': self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group, slug=self.kwargs.get('slug'))
        user = get_user(request)
        try:
            GroupMember.objects.create(user=user,group=group)
        except (GroupMember.DoesNotExist, IntegrityError):
            messages.warning(self.request, 'You are already a member of this group.')
        else:
            messages.success(self.request, 'You are now a member of this group.')

        return super().get(request, *args, **kwargs)

class LeaveGroup(LoginRequiredMixin, generic.RedirectView):
    model = Group

    def get_queryset(self):
        pass

    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single', kwargs={'slug': self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group, slug=self.kwargs.get('slug'))

        try:
            membership = models.GroupMember.objects.filter(user=self.request.user, group__slug=self.kwargs.get('slug')).get()
        except models.GroupMember.DoesNotExist:
            messages.warning(self.request, 'You are not a member of this group.')
        else:
            membership.delete()
            messages.success(self.request, 'You are left the group.')
        return super().get(request, *args, **kwargs)