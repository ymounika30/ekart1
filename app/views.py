from django.shortcuts import redirect,render,HttpResponse,HttpResponseRedirect
from django.views.generic import TemplateView,View,RedirectView,CreateView
from . models import*
from .forms import SignUpForm,Contact
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail

class HomeView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['myname']='Mounika'
        context['product_list']= Product.objects.all()
        return context
    
class AddToCartView(TemplateView):
    template_name ='addtocart.html'
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        product_id=self.kwargs['pro_id']
        product_obj=Product.objects.get(id=product_id)

        cart_id=self.request.session.get('cart_id',None)
        if cart_id:
            cart_obj=Cart.objects.get(id=cart_id)
            this_product_in_cart=cart_obj.cartproduct_set.filter(product=product_obj)
            if this_product_in_cart.exists():
                cartproduct=this_product_in_cart.last()
                cartproduct.quantity+=1
                cartproduct.subtotal+=product_obj.selling_price
                cartproduct.save()
                cart_obj.total+=product_obj.selling_price
                cart_obj.save()
            else:
                cartproduct=CartProduct.objects.create(
                    cart=cart_obj,product=product_obj,rate=product_obj.selling_price,quantity=1,subtotal=product_obj.selling_price
                )
                cart_obj.total += product_obj.selling_price
                cart_obj.save()
        else:
            cart_obj=Cart.objects.create(total=0)
            self.request.session['cart_id']=cart_obj.id
            cartproduct = CartProduct.objects.create(
                cart=cart_obj, product=product_obj, rate=product_obj.selling_price, quantity=1,
                subtotal=product_obj.selling_price
            )
            cart_obj.total += product_obj.selling_price
            cart_obj.save()

        return context
    
class MyCartView(TemplateView):
    template_name = 'mycart.html'
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        cart_id=self.request.session.get('cart_id',None)
        if cart_id:
            cart=Cart.objects.get(id=cart_id)
        else:
            cart=None
        context['cart']=cart
        return context
    
class AboutView(TemplateView):
    template_name = 'about.html'
    
# class ContactView(TemplateView):
#     template_name = 'contact.html'

class DeleteView(RedirectView):
    url='/'
    def get_redirect_url(self,*args,**kwargs):
        del_id=kwargs['id']
        Product.objects.get(pk=del_id).delete()
        return super().get_redirect_url(*args,**kwargs)
 
def contact(request):
    if request.method == 'POST':
        fm = Contact(request.POST)
        if fm.is_valid():
            fm.save()
            messages.success(request,'Thanks for Contacting Us')
            return HttpResponseRedirect("<h1> Succussfull </h1>")
    else:
        fm = Contact()
    return render(request,'contact.html',{'form':fm})

def signup(request):
    if request.method == "POST":
        fm=SignUpForm(request.POST)
        if fm.is_valid():
            EMAIL=fm.cleaned_data['email']
            user=fm.save()
            login(request,user)
            messages.success(request,'Account Created Successfully !!!')
            send_mail(
                'sending mail',
                'Hi, Hello, How are you??',
                'mounikayarramasu1994@gmail.com',
                [str(EMAIL)],
                fail_silently=False
            )
            
    else:
        fm=SignUpForm()
    return render(request,'signup.html',{'form':fm})



def ulogin(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            fm = AuthenticationForm(request=request, data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged in successfully !!')
                return HttpResponseRedirect('/dashboard/')
        else:
            fm = AuthenticationForm()
        return render(request, 'login.html', {'form':fm})
    else:
       return HttpResponseRedirect('/dashboard/')

def Logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')
