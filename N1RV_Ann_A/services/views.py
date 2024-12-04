from django.shortcuts import render, get_object_or_404, redirect
from .models import Hairdresser, Service, OrderedServices
import datetime
from django.db.models import Count, Q
from django.core.paginator import Paginator
from accounts.models import UserAccount
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ProfileEditForm, ServiceForm, OrderForm

POSTS_PER_PAGE = 10

# Create your views here.
def _get_time():
    return datetime.datetime.now(datetime.timezone.utc)


def profile_view(request, username):
    template_name = 'main/profile.html'

    profile = get_object_or_404(UserAccount, username=username)
    orders = OrderedServices.objects.select_related(
        'hairdresser', 'service'
    ).filter(
        customer=profile.pk
    ).order_by(
        '-serve_date'
    )

    page_obj = Paginator(orders, POSTS_PER_PAGE)
    page_obj = page_obj.get_page(request.GET.get('page'))

    context = {
        'profile': profile,
        'page_obj': page_obj
    }
    return render(request, template_name, context)


@login_required
@user_passes_test(lambda u: u.is_staff)
def edit_profile_view(request):

    form = ProfileEditForm(instance=request.user)

    if request.method == 'POST':
        form = ProfileEditForm(request.POST)

        if form.is_valid():
            user = User.objects.get(pk=request.user.pk)

            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            hairdresser_preference = form.cleaned_data['hairdresser_preference']

            user.save()

    context = {
        'form': form
    }

    return render(request, 'main/user.html', context)

@user_passes_test(lambda u: u.is_staff)
@login_required
def service_create_view(request):
    # check if user is admin or not

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
    if request.method == 'POST':
        service_form = ServiceForm(request.POST, request.FILES)
        if request.user.pk != service.author.pk or not service_form.is_valid():
            return redirect('main:post_detail', service_id=service_id)
        service.description = service_form.cleaned_data['description']
        service.title = service_form.cleaned_data['title']
        service.pub_date = service_form.cleaned_data['pub_date']
        service.price = service_form.cleaned_data['price']
        service.image = service_form.cleaned_data['image']
        service.save()
        return redirect('main:service_detail', service_id=service_id)
    else:
        service_form = ServiceForm(instance=service)

    context = {
        'form': service_form
    }

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
    if order_form.is_valid():
        order = order_form.save(commit=False)
        order.customer = request.user

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
        
        order.hairdresser = order_form.cleaned_data['hairdresser']
        order.service = order_form.cleaned_data['service']
        order.serve_date = order_form.cleaned_data['serve_date']
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

    orders = OrderedServices.objects.filter(Q(service=service, customer=request.user))

    context = {
        'service': service,
        'orders': orders,
        'form': OrderForm()
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

    services = hairdresser.service.related.all();

    page_obj = Paginator(posts, POSTS_PER_PAGE)
    page_obj = page_obj.get_page(request.GET.get('page'))

    context = {
        'hairdresser': hairdresser,
        'page_obj': page_obj
    }

    return render(request, template, context)
