from django.shortcuts import render, HttpResponseRedirect, reverse
from homepage.models import Ticket, CustomUser
from django.contrib.auth.decorators import login_required
from homepage.forms import LoginForm, AddTicketForm
from django.contrib.auth import login, authenticate
from datetime import datetime

# Create your views here.

def login_view(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data.get('username'), password=data.get('password'))
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))

    return render(request, 'generic_form.html', {'form': form})

@login_required
def homepage_view(request):
    tickets = Ticket.objects.all()
    new_status = Ticket.objects.filter(status=Ticket.NEW)
    in_progress_status = Ticket.objects.filter(status=Ticket.IN_PROGRESS)
    done_status = Ticket.objects.filter(status=Ticket.DONE)
    invalid_status = Ticket.objects.filter(status=Ticket.INVALID)

    return render(request, 'home.html', {'tickets': tickets, 'new_tickets': new_status, 'in_progress_tickets': in_progress_status, 'done_tickets': done_status, 'invalid_tickets': invalid_status})

@login_required
def file_ticket_view(request):
    if request.method == 'POST':
        form = AddTicketForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_ticket = Ticket.objects.create(
                title = data.get('title'),
                description = data.get('description'),
                time_created = datetime.now(),
                filer = request.user,
                status = 'New',
                completed_by = None,
                assigned_to = None
            )
            if new_ticket:
                return HttpResponseRedirect(reverse('home'))

    form = AddTicketForm()
    return render(request, 'generic_form.html', {'form': form})

def edit_ticket_view(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)

    if request.method == 'POST':
        form = AddTicketForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            ticket.title = data['title']
            ticket.description = data['description']
            ticket.save()
        return HttpResponseRedirect(reverse('spec_ticket', args=[ticket.id]))

    data = {
        'title': ticket.title,
        'description': ticket.description
    }
    form = AddTicketForm(initial=data)
    return render(request, 'generic_form.html', {'form': form})

def ticket_view(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)

    return render(request, 'ticket_detail.html', {'ticket': ticket})

def user_view(request, username):
    user = CustomUser.objects.get(username=username)
    filed_tickets = Ticket.objects.filter(filer=user)
    assigned_tickets = Ticket.objects.filter(assigned_to=user)
    completed_tickets = Ticket.objects.filter(completed_by=user)


    return render(request, 'user_detail.html', {'user': user, 'filed_tickets': filed_tickets, 'assigned_tickets': assigned_tickets, 'completed_tickets': completed_tickets})

def claim_ticket_view(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)

    ticket.status = Ticket.IN_PROGRESS
    ticket.assigned_to = request.user
    ticket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def unclaim_ticket_view(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)

    ticket.status = Ticket.NEW
    ticket.assigned_to = None
    ticket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def complete_ticket_view(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)

    ticket.status = Ticket.DONE
    ticket.assigned_to = None
    ticket.completed_by = request.user
    ticket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def invalid_ticket_view(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)

    ticket.status = Ticket.INVALID
    ticket.assigned_to = None
    ticket.completed_by = None
    ticket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



