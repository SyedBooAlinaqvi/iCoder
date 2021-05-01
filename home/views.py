from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from django.contrib import messages
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# HTML pages
def home(request):
    return render(request, 'home/home.html')
    # return HttpResponse('This is home')


def contact(request):
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        print(name, email, phone, content)
        if name.strip()=='' or email.strip()=='' or content.strip()=='':
            messages.error(request, 'please dont leave empty fields')                
            return render(request, 'home/contact.html')
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request, 'please fill the form correctly')
            return render(request, 'home/contact.html')
        
        contact = Contact(name=name, phone=phone, email=email, content=content)
        contact.save()
        messages.success(request, 'Your message has been sent successfully!')
        
    return render(request, 'home/contact.html') 


def about(request):
    return render(request, 'home/about.html')

# Authentication APIs
def search(request):
    query = request.GET['query']
    if len(query)>78:
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent)
    
    if allPosts.count() == 0:
        messages.warning(request, '"No search results found. Please refine your search query"')
    params = {'allPosts': allPosts, 'query':query}
    return render(request, 'home/search.html', params)


def handleSignup(request):
    if request.method=="POST":
        # Get the post parameters
        username=request.POST['username']
        email=request.POST['email']
        fname=request.POST['fname']
        lname=request.POST['lname']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        # check for errorneous input
        if User.objects.filter(username=username).exists():
            messages.error(request,'User already exists')
            return redirect('home')
        if User.objects.filter(email=email).exists():
            messages.error(request,'Email already exists')
            return redirect('home')
        
        if len(username)>10:
            messages.error(request, " Your user name must be under 10 characters")
            return redirect('home')
        if not username.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return redirect('home')
        if username.strip() == '' or email.strip() == '' or fname.strip() == '' or lname.strip() == '':
            messages.error(request, 'Donot leave empty spaces in fields')
            return redirect('home')
        if (pass1!= pass2):
             messages.error(request, " Passwords do not match")
             return redirect('home')
         
        
        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name= fname
        myuser.last_name= lname
        myuser.save()
        messages.success(request, " Your iCoder has been successfully created")
        return redirect('home')

    else:
        return HttpResponse("404 - Not found")
    

def handleLogin(request):
    if request.method=="POST":
        # Get the post parameters
        loginusername=request.POST['loginusername']
        loginpass=request.POST['loginpass']
        user = authenticate(username=loginusername, password=loginpass)
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged In')
            return redirect('home')
        else:
            messages.error(request, 'Invalid Credentials, Please try again!')
            return redirect('home')
    return HttpResponse('404 - Not Found')


def handleLogout(request):
    logout(request)
    messages.success(request, 'Successfully Logged Out')
    return redirect('home')


# def SocialAuth(request):
#     pass