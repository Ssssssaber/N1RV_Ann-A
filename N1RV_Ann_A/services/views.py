from django.shortcuts import render, get_object_or_404, redirect
from .models import Hairdresser, Service, OrderedServices
import datetime
from django.db.models import Count, Q
from django.core.paginator import Paginator
from accounts.models import UserAccount
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ProfileEditForm, ServiceForm, OrderForm, HairdresserForm
from .utils import _check_suitable_datetime, _get_time

POSTS_PER_PAGE = 3

def profile_view(request, username):
    template_name = 'main/profile.html'

    profile = get_object_or_404(UserAccount, username=username)
    orders = OrderedServices.objects.filter(
        customer=profile.pk
    ).order_by(
        '-serve_date'
    )

    page_obj = Paginator(orders, POSTS_PER_PAGE)
    page_obj = page_obj.get_page(request.GET.get('page'))

    hairdressers = profile.hairdresser_preference.all()

    context = {
        'profile': profile,
        'page_obj': page_obj,
        'hairdressers': hairdressers
    }
    return render(request, template_name, context)


@login_required
def edit_profile_view(request):

    form = ProfileEditForm(instance=request.user)

    if request.method == 'POST':
        form = ProfileEditForm(request.POST)

        if form.is_valid():
            user = UserAccount.objects.get(pk=request.user.pk)

            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.hairdresser_preference.set(form.cleaned_data['hairdresser_preference'])

            user.save()

    context = {
        'form': form
    }

    return render(request, 'main/user.html', context)

@user_passes_test(lambda u: u.is_staff)
@login_required
def service_create_view(request):
    template_name = 'main/create.html'
    form = ServiceForm()

    if (request.method == 'POST'):
        serviceForm = ServiceForm(request.POST, request.FILES)

        if serviceForm.is_valid():
            service = serviceForm.save(commit=False)
            service.author = request.user
            service.save()
            return redirect('main:index')
    context = {
        'form': form
    }
    return render(request, template_name, context)

@user_passes_test(lambda u: u.is_staff)
@login_required
def service_edit_view(request, service_id):
    template_name = 'main/create.html'
    service = get_object_or_404(Service, pk=service_id)
    service_form = ServiceForm(instance=service)

    context = {
        'form': service_form
    }
    if request.method == 'POST':
        service_form = ServiceForm(request.POST, request.FILES)
        if not service_form.is_valid():
            return redirect('main:service_detail', service_id=service_id)
        service.description = service_form.cleaned_data['description']
        service.title = service_form.cleaned_data['title']
        service.pub_date = service_form.cleaned_data['pub_date']
        service.price = service_form.cleaned_data['price']
        service.image = service_form.cleaned_data['image']
        service.save()
        return render(request, template_name, context)
    else:
        service_form = ServiceForm(instance=service)

    

    return render(request, template_name, context)


@user_passes_test(lambda u: u.is_staff)
@login_required
def service_delete_view(request, service_id):
    service = get_object_or_404(Service, pk=service_id)

    # if request.user.pk != post.author.pk:
    #     return redirect("main:post_detail", service_id=service_id)

    service.delete()
    return redirect("main:profile", username=request.user)


@login_required
def order_create_view(request, service_id):
    if request.method != 'POST':
        return redirect('main:service_detail', service_id=service_id)

    service = get_object_or_404(
        Service,
        pk=service_id
    )

    order_form = OrderForm(request.POST)
    order_form.fields['service'].initial = service
    order_form.fields['service'].disabled = True
    if order_form.is_valid():
        res_time = datetime.datetime.combine(order_form.cleaned_data['serve_date'], order_form.cleaned_data['serve_time'])
        if not _check_suitable_datetime(res_time): 
            return redirect('main:service_detail', service_id=service_id) 
        order = order_form.save(commit=False)
        order.customer = request.user
        order.serve_date = res_time
        order.save()

    return redirect('main:service_detail', service_id=service_id)


@login_required
def order_edit_view(request, service_id, order_id):
    template_name = 'main/order.html'

    order = get_object_or_404(OrderedServices, pk=order_id)
    form = OrderForm(instance=order)

    if request.method == 'POST' and request.user.pk == order.customer.pk:
        order_form = OrderForm(request.POST)
        if not order_form.is_valid():
            return redirect('main:service_detail', service_id=service_id)
        res_time = datetime.datetime.combine(order_form.cleaned_data['serve_date'], order_form.cleaned_data['serve_time'])
        if not _check_suitable_datetime(res_time): 
            return redirect('main:service_detail', service_id=service_id)       
        
        order.hairdresser = order_form.cleaned_data['hairdresser']
        order.service = order_form.cleaned_data['service']
        order.serve_date = res_time
        order.save()

        return redirect('main:service_detail', service_id=service_id)

    context = {
        'form': form,
        'order': order
    }
    return render(request, template_name, context)


@login_required
def order_delete_view(request, service_id, order_id):
    template_name = 'main/order.html'

    order = get_object_or_404(OrderedServices, pk=order_id)

    if request.method == 'POST' and request.user.pk == order.customer.pk:
        order.delete()
        return redirect('main:service_detail', service_id=service_id)

    context = {
        'order': order
    }

    return render(request, template_name, context)

def hairdresser_list(request):
    template_name = 'main/hairdresser-list.html'
    current_date = _get_time()
    hairdressers = Hairdresser.objects.filter(
        is_published=True).order_by('-created_at')

    page_obj = Paginator(hairdressers, POSTS_PER_PAGE)
    page_obj = page_obj.get_page(request.GET.get('page'))

    context = {
        'page_obj': page_obj
    }

    return render(request, template_name, context)


@user_passes_test(lambda u: u.is_staff)
@login_required
def hairdresser_create_view(request):
    template_name = 'main/hairdresser-create.html'

    hairdresser_form = HairdresserForm(request.POST, request.FILES)
    if hairdresser_form.is_valid():
        hairdresser = hairdresser_form.save(commit=False)
        hairdresser.save()
        return redirect('main:hairdresser_services', hairdresser_slug=hairdresser.slug)

    context = {
        'form': hairdresser_form
    }
    return render(request, template_name, context)


@user_passes_test(lambda u: u.is_staff)
@login_required
def hairdresser_edit_view(request, hairdresser_slug):
    template_name = 'main/hairdresser-create.html'

    hairdresser = get_object_or_404(Hairdresser, slug=hairdresser_slug)
    form = HairdresserForm(instance=hairdresser)

    if request.method == 'POST':
        order_form = HairdresserForm(request.POST, request.FILES)
        if not order_form.is_valid():
            return redirect('main:hairdresser_services', hairdresser_slug=hairdresser.slug)

        hairdresser.first_name = order_form.cleaned_data['first_name']
        hairdresser.last_name = order_form.cleaned_data['last_name']
        hairdresser.description = order_form.cleaned_data['description']
        hairdresser.image = order_form.cleaned_data['image']
        hairdresser.services.set(order_form.cleaned_data['services'])
    
        hairdresser.save()

        return redirect('main:hairdresser_services', hairdresser_slug=hairdresser.slug)

    context = {
        'form': form,
        'hairdresser': hairdresser
    }
    return render(request, template_name, context)


@user_passes_test(lambda u: u.is_staff)
@login_required
def hairdresser_delete_view(request, hairdresser_slug):
    template_name = 'main/hairdresser_create.html'

    hairdresser = get_object_or_404(Hairdresser, pk=order_id)

    if request.method == 'POST':
        hairdresser.delete()
        return redirect('main:index')

    context = {
        'hairdresser': hairdresser
    }

    return render(request, template_name, context)

# Create your views here.
def index(request):
    template_name = 'main/index.html'
    current_date = _get_time()
    services = Service.objects.filter(
        is_published=True,
        pub_date__lte=current_date).order_by('-pub_date')

    page_obj = Paginator(services, POSTS_PER_PAGE)
    page_obj = page_obj.get_page(request.GET.get('page'))

    context = {
        'page_obj': page_obj
    }

    return render(request, template_name, context)


def service_detail(request, service_id):
    template = 'main/detail.html'
    current_date = _get_time()
    # add check if any hairdresser can serve it
    service = get_object_or_404(
        Service,
        Q(pk=service_id, pub_date__lte=current_date, is_published=True)
    )

    orders = OrderedServices.objects.filter(
        service=service.id, 
        customer=request.user.id).order_by(
        'serve_date'
    )

    for order in orders:
        print(order.serve_date)

    order_form = OrderForm()

    suitable_hairdressers = Hairdresser.objects.filter(Q(services=service))

    order_form.fields['hairdresser'].queryset = suitable_hairdressers
    order_form.fields['service'].initial = service
    order_form.fields['service'].disabled = True
    context = {
        'service': service,
        'orders': orders,
        'form': order_form
    }

    return render(request, template, context)


def hairdresser_services(request, hairdresser_slug):
    template = 'main/hairdresser.html'
    hairdresser = get_object_or_404(
        Hairdresser,
        slug=hairdresser_slug,
        is_published=True
    )
    current_date = _get_time()

    services = hairdresser.services.filter(is_published=True);

    page_obj = Paginator(services, POSTS_PER_PAGE)
    page_obj = page_obj.get_page(request.GET.get('page'))

    context = {
        'hairdresser': hairdresser,
        'page_obj': page_obj
    }

    return render(request, template, context)
