import json
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.template import loader
from django.http import HttpResponse

from .models import *
from .serializers import *

from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.

def deletev(request, pk):
    Post.objects.get(pk=pk).delete()
    return redirect('home')

def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    selected_option = None 
    socialevents = None
    clubevents = None
    internships = None
    accomodations = None
    transports = None
    data = request.GET.dict()
    if len(data)==0:
        socialevents = SocialEvent.objects.all()
        clubevents = ClubEvent.objects.all()
        internships = Internship.objects.all()
        accomodations = Accommodation.objects.all()
        transports = Transport.objects.all()

    elif 'posttype' in data.keys():
        if data['posttype'] == '0':
            clubevents = ClubEvent.objects.all()
            selected_option = 0
            
            if data['keys'] != '':
                clubevents = clubevents.filter(club__icontains=data['keys'])
        elif data['posttype'] == '1':
            socialevents = SocialEvent.objects.all()
            selected_option = 1
            if data['keys'] != '':
                socialevents = socialevents.filter(description__icontains=data['keys'])
        elif data['posttype'] == '2':
            internships = Internship.objects.all()
            selected_option = 2
            if data['keys'] != '':
                internships = internships.filter(typeStg__icontains=data['keys'])
        elif data['posttype'] == '3':
            accomodations = Accommodation.objects.all()
            selected_option = 3
            if data['keys'] != '':
                accomodations = accomodations.filter(location__icontains=data['keys'])
        elif data['posttype'] == '4':
            transports = Transport.objects.all()
            selected_option = 4
            if data['keys'] != '':
                transports = transports.filter(destination__icontains=data['keys'])

    li = [socialevents, clubevents, internships, accomodations, transports]
    return render(request, 'home.html', {'posts':li ,'selected_option':selected_option})

def loginf(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':

        data = request.POST
        user = None
        try:
            user = Users.objects.get(email=data['email'])
        except:
            messages.error(request, "L'utilisateur '" + data['email'] + "' n'existe pas.")
            return render(request, 'login.html')
        
        if not user.check_password(data['password']):
            messages.error(request, "Mot de passe incorrect.")
            return render(request, 'login.html')

        login(request, user)
        return redirect('home')

    if request.method == 'GET':
        return render(request, 'login.html')
    


def signupf(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'GET':
        return render(request, 'signup.html')

    if request.method == 'POST':
        data = request.POST
        user = Users.objects.create(email=data['email'],username=data['first_name'] ,first_name=data['first_name'], last_name=data['last_name'], telephone=data['telephone'])
        if user:
            user.set_password(data['password'])
            user.save()
            login(request, user)
            return redirect('home')
        
def logoutf(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('login')
    else:
        return redirect('login')
    
def deposit(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'GET':
        return render(request, 'deposit.html')
    
    if request.method == 'POST':
        data = json.dumps(request.POST)
        data = json.loads(data)
        
        child_type = data.pop('posttype')
        print(child_type)
        data.pop('csrfmiddlewaretoken')
        data['owner'] = request.user
        data['image'] = request.FILES['image']
        base =  None
        if child_type == '0':
            base=ClubEvent
        elif child_type =='1':
            base=SocialEvent
        elif child_type =='2':
            base=Internship
        elif child_type =='3':
            base=Accommodation
        elif child_type =='4':
            base=Transport
        elif child_type =='5':
            base=Recommendation 
        
        instance = base(**data)
        instance.save()

        return redirect('home')
    
    

    
def postv(request, pk):
    
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'GET':
        data = request.GET.dict()

        if 'adore' in data.keys():
            reaction = Reaction.objects.filter(owner=request.user, post=pk)
            if not reaction.exists():
                Reaction.objects.create(owner=Users.objects.get(id=request.user.id), post=Post.objects.get(pk=pk))
                message = request.user.first_name + ' ' + request.user.last_name + ' a adore votre Post.'
                link = "post:" + str(pk)
                Notifications.objects.create(owner=Users.objects.get(id=request.user.id), comment=message, url=link)

        type = data['type']
        post = None
        model = None
        r = []
        if type == 'Évènements culturels':
            model = SocialEvent
            post = model.objects.get(pk=pk)


            
                
            r = [
                ['Post:', type],
                ['Intitule:', post.titled],
                ['Description:', post.description],
                ['Lieu:', post.place],
                ['Contact:', post.contactinfo],
                ['Date:', post.date],
                ['Price:', post.price]
            ]
            ty = "Offre" if post.type == 0 else "Demande"
            r.append(['Type:', ty])
            r.append(['Adores:', Reaction.objects.filter(post=pk).count()])
            
    
            
        if type=='Évènements scientifiques':
            model = ClubEvent
            post = model.objects.get(pk=pk)
            r.append(['Post:', type])
            r.append(['Intitule:', post.titled])
            r.append(['Description:', post.description])
            r.append(['Lieu:', post.place])
            r.append(['Contact:', post.contactinfo])
            r.append(['Date:', post.date])
            r.append(['Club:', post.club])
            ty = "Offre" if post.type == 0 else "Demande"
            r.append(['Type:', ty])
            r.append(['Adores:', Reaction.objects.filter(post=pk).count()])
            
                
                 
           

        if type=='Transport':
            model = Transport
            post = model.objects.get(pk=pk)
            r.append(['Post:', type])
            r.append(['Depart:', post.departure])
            r.append(['Destination:', post.departure_hour])
            r.append(['Heure depart:', post.destination])
            r.append(['Nombre de Sieges:', post.seats])
            r.append(['Contact:', post.contactinfo])
            
            ty = "Offre" if post.type == 0 else "Demande"
            r.append(['Type:', ty])
            r.append(['Adores:', Reaction.objects.filter(post=pk).count()])
            

        if type=='Logement':
            model = Accommodation
            post = model.objects.get(pk=pk)
            r.append(['Post:', type])
            r.append(['Localisation:', post.location])
            r.append(['Description:', post.description])
            r.append(['Contact:', post.contactinfo])
            
            ty = "Offre" if post.type == 0 else "Demande"
            r.append(['Type:', ty])
            r.append(['Adores:', Reaction.objects.filter(post=pk).count()])
            

        if type=='Stage':
            model = Internship
            post = model.objects.get(pk=pk)
            r.append(['Post:', type])
            r.append(['Societe:', post.company])
            r.append(['Duree:', post.duration])
            r.append(['Sujet:', post.subject])
            r.append(['Contact:', post.contactinfo])
            r.append(['Specialite:', post.speciality])
            if post.typeStg == 1:
                t = "Ouvrier"
            elif post.typeStg == 2:
                t = "Technicien"
            elif post.typeStg == 3:
                t = "PFE"
            
            ty = "Offre" if post.type == 0 else "Demande"
            r.append(['Type:', ty])
            r.append(['Adores:', Reaction.objects.filter(post=pk).count()])
            
    
        if type=='Recommendation':
            model = Recommendation
            post = model.objects.get(pk=pk)
            r.append(['Post:', type])
            r.append(['text:', post.text])
            ty = "Offre" if post.type == 0 else "Demande"
            r.append(['Type:', ty])
            r.append(['Adores:', Reaction.objects.filter(post=pk).count()])
            
        comments = Comment.objects.filter(post=pk)
        print(data['type'])
        return render(request, 'postv.html', {'img':post.image.url,'id':post.pk,'p':type,'r':r, 'comments':comments})

        
    
    if request.method == 'POST':
        data = json.dumps(request.POST)
        data = json.loads(data)

        data['owner'] = request.user
        data['post'] = Post.objects.get(id=pk)
        data.pop('csrfmiddlewaretoken')
        instance = Comment(**data)
        instance.save()

        message = request.user.first_name + ' ' + request.user.last_name + ' a commente votre Post.'
        link = "post:" + str(pk)
        Notifications.objects.create(owner=Users.objects.get(id=request.user.id), comment=message, url=link)

        request.method = 'GET'
        return postv(request, pk)

class userapi(APIView):
    def get(self, request, pk=None):
        if pk==None:
            return Response(UserSerializer(Users.objects.all(), many=True).data)
        else:
            return Response(UserSerializer(Users.objects.get(id=pk)).data)
        
class postsapi(APIView):
    def get(self, request):
        es = SocialEventSerializer(SocialEvent.objects.all(),many=True).data
        ec = ClubEventSerializer(ClubEvent.objects.all(),many=True).data
        ac = AccommodationSerializer(Accommodation.objects.all(),many=True).data
        tr = TransportSerializer(Transport.objects.all(),many=True).data
        st = InternshipSerializer(Internship.objects.all(),many=True).data
        rc = RecommendationSerializer(Recommendation.objects.all(),many=True).data

        sss = {
            'evensocial':es,
            'evenclub':ec,
            'longement':ac,
            'transport':tr,
            'stage':st,
            'recommandation':rc
        }
        return Response(sss)