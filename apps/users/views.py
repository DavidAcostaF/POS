from django.views.generic import CreateView,TemplateView,CreateView,View
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth import login, logout,authenticate
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from apps.users.forms import FormUser,FormLogin,FormUserUpdate,UpdatePasswordForm
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from apps.users.models import MyUser
from apps.users.forms import FormUser
# Create your views here.

class Register(CreateView):
    model = MyUser
    template_name = 'accounts/register.html'
    form_class = FormUser
    success_url = reverse_lazy('login')

    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(request,username = username,password = password)
            print(user)
            login(request,user)
            return redirect('products_lists')
        context = {
            'form_errors':form.errors
        }
        return render(request,self.template_name,context)

class Login(FormView):
    template_name = 'accounts/login.html'
    form_class = FormLogin
    success_url = reverse_lazy('products_lists')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(Login, self).form_valid(form)

def UserLogout(request):
    logout(request)
    return redirect('login')



class Profile(CreateView):
    model = MyUser
    form_class = FormUserUpdate
    template_name = 'accounts/profile.html'
    success_url = ('profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(instance = self.request.user)
        context['formpassword'] = UpdatePasswordForm
        return context

    def post(self,request):
        form = self.form_class(request.POST,request.FILES,instance = self.request.user)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
        return redirect(request.path)
        

class UpdatePassword(View):
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('profile')

    def post(self,request):
        user = request.user
        form = self.form_class(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data.get('password1'))
            print(form.cleaned_data.get('password1'))
            user.save()
        return redirect('login')


class Activate(View):
    model = MyUser

    def get(self,request,slug):
        uid = slug
        user = self.model.objects.get(uuid = uid)
        user.activate = True
        user.save()
        return redirect('login')


class Resend(View):
    def post(self,request):
        template = render_to_string('mails/activate.html',{
            'uid':request.user.uuid
        })
        mail = EmailMultiAlternatives(
        'Activate account',
        template,
        from_email=settings.EMAIL_HOST_USER,
        to=[request.user.email],
        )
        mail.fail_silently = False
        mail.attach_alternative(template,'text/html')
        mail.send()
        return redirect('products_lists')