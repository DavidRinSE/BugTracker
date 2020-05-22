from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, reverse, HttpResponseRedirect

from .forms import LoginForm, TicketForm
from .models import Ticket
def index(request):
    html = "index.html"
    return render(request, html)


@login_required
def view_ticket(request, id):
    html = "ticket.html"
    ticket = Ticket.objects.get(id=id)

    return render(request, html, {
        "ticket":ticket,
        "homepage":reverse("homepage"),
        "invalid": reverse("invalid", kwargs={'id':id}),
        "assign_self": reverse("assign", kwargs={'id':id}),
        "complete": reverse("complete", kwargs={'id':id}),
        "edit": reverse("edit", kwargs={'id':id}),
    })


@login_required
def assign_self(request, id):
    ticket = Ticket.objects.get(id=id)
    user = request.user
    ticket.assignTo(user)
    return HttpResponseRedirect(reverse("ticket", kwargs={"id":id}))


@login_required
def invalid_ticket(request, id):
    ticket = Ticket.objects.get(id=id)
    ticket.markInvalid()
    return HttpResponseRedirect(reverse("ticket", kwargs={"id":id}))


@login_required
def complete_ticket(request, id):
    ticket = Ticket.objects.get(id=id)
    user = request.user
    ticket.finishedBy(user)
    return HttpResponseRedirect(reverse("ticket", kwargs={"id":id}))


@login_required
def view_tickets(request):
    html = "tickets.html"

    ticket_lists = tuple()
    
    new_tickets = Ticket.objects.all().filter(status="New")
    ticket_lists += (("New", new_tickets),)
    
    inProgress_tickets = Ticket.objects.all().filter(status="In Progress")
    ticket_lists += (("In Progress", inProgress_tickets),)
    
    done_tickets = Ticket.objects.all().filter(status="Done")
    ticket_lists += (("Done", done_tickets),)
    
    invalid_tickets = Ticket.objects.all().filter(status="Invalid")
    ticket_lists += (("Invalid", invalid_tickets),)
    
    return render(request, html, {
        "lists":ticket_lists,
        "newticket":reverse("newticket"),
        "account":reverse("account"),
        "logout":reverse("logout")})



@login_required
def view_user(request):
    html = "user.html"

    user = request.user
    ticket_lists = tuple()

    filed_tickets = Ticket.objects.all().filter(userFiled=user)
    ticket_lists += (("Filed", filed_tickets),)

    assigned_tickets = Ticket.objects.all().filter(userAssigned=user)
    ticket_lists += (("Assigned", assigned_tickets),)

    completed_tickets = Ticket.objects.all().filter(userCompleted=user)
    ticket_lists += (("Completed", completed_tickets),)

    return render(request, html, {
        "lists":ticket_lists,
        "user":user,
        "logout":reverse("logout"),
        "homepage":reverse("homepage")
    })


@login_required
def create_ticket(request):
    html = "ticketform.html"

    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            status = "New" if not data['userAssigned'] else "In Progress"
            if data['userCompleted']:
                status = "Done"
            ticket = Ticket.objects.create(
                title=data['title'],
                description=data['description'],
                userFiled=request.user,
                userAssigned=data['userAssigned'],
                userCompleted=data['userCompleted'],
                status=status
            )
            return HttpResponseRedirect(reverse('ticket', kwargs={"id":ticket.id}))
    form = TicketForm()
    return render(request, html, {"form":form})


@login_required
def edit_ticket(request, id):
    html = "ticketform.html"

    ticket = Ticket.objects.get(id=id)
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            ticket.title = data["title"]
            ticket.description = data["description"]
            if data["userCompleted"] and ticket.userCompleted != data["userCompleted"]:
                ticket.userCompleted = data["userCompleted"]
                ticket.status = "Done"
                ticket.userAssigned = None
            elif data["userAssigned"] and ticket.userAssigned != data["userAssigned"]:
                ticket.userAssigned = data["userAssigned"]
                ticket.status = "In Progress"
                ticket.userCompleted = None
            ticket.save()
            return HttpResponseRedirect(reverse('ticket', kwargs={"id":ticket.id}))
    form = TicketForm(initial={
        "title":ticket.title,
        "description":ticket.description,
        "userAssigned":ticket.userAssigned.id if ticket.userAssigned else None,
        "userCompleted":ticket.userCompleted.id if ticket.userCompleted else None
    })
    return render(request, html, {"form":form})


def login_view(request):
    html = "loginform.html"

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])
            if user:
                login(request, user)
                return HttpResponseRedirect(
                    request.GET.get('next', reverse('homepage'))
                )

    form = LoginForm()
    return render(request, html, {"form": form})


def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))