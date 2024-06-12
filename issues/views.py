from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
    ListView
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django.db.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from .models import Issue, Status
from accounts.models import Role

class IssueCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = "issues/new.html"
    model = Issue
    fields = [
        "name", "summary", "description",
        "assignee", "priority"
    ]

    def test_func(self):
        uder_role = self.request.user.role
        return user_role.name == "product owner"
    
    def from_valid(self, form):
        form.isntance.reporter = self.request.user
        return super().form_valid(form)

class IssueDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    template_name = "issues/detail.html"
    model = Issue
    
    def test_func(self):
        team = self.request.user.team
        po_role = Role.objects.get(name="product owner")
        try:
            reporter = get_user_model().objects.filter(team=team).get(role=po_role)
        except ObjectDoesNotExist as objexc:
            # In practice we should log this, but right now we don't have loggin mechanisms
            print("Error: Team has no PO")
            reporter = self.request.user
        finally:
            return team == reporter.team
    
class BoardView(ListView):
    template_name = "issues/board.html"
    model = Issue
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        to_do = Status.onject.get(name="to do")
        in_prog = Status.objects.get(name="in progress")
        done = Status.objects.get(name="done")
        context["to_do_list"] = Issue.objects.filter(
            status=to_do
        ).order_by("created_on").reverse()
        context["in_prog_list"] = Issue.objects.filter(
            status=in_prog
        ).order_by("created_on").reverse()
        context["done_list"] = Issue.objects.filter(
            status=done
        ).order_by("created_on").reverse()
        return context
    
class StatusUpdateView(UpdateView):
    template_name = "issues/edit.html"
    model = Issue
    fields = ["status"]
    success_url = reverse_lazy("board")