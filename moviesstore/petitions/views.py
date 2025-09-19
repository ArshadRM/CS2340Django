from django.shortcuts import render, redirect, get_object_or_404
from .models import Petition
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

def index(request):
    petitions = Petition.objects.all()
    template_data = {
        'title': 'Petitions',
        'petitions': petitions
    }
    return render(request, 'petitions/index.html', {'template_data': template_data})

def show(request, id):
    petition = get_object_or_404(Petition, id=id)
    template_data = {
        'title': petition.movie_title,
        'petition': petition
    }
    return render(request, 'petitions/show.html', {'template_data': template_data})

@login_required
def create(request):
    if request.method == 'POST':
        petition = Petition()
        petition.movie_title = request.POST['movie_title']
        petition.description = request.POST['description']
        petition.user = request.user
        petition.save()
        return redirect('petitions.index')
    else:
        template_data = {
            'title': 'Create Petition'
        }
        return render(request, 'petitions/create.html', {'template_data': template_data})

@login_required
@require_POST
def vote(request, id):
    petition = get_object_or_404(Petition, id=id)
    if request.user in petition.votes.all():
        petition.votes.remove(request.user)
    else:
        petition.votes.add(request.user)
    petition.save()
    return redirect('petitions.show', id=id)
