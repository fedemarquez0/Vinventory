from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from .models import Bodega, Estante, Origen, Variedad, Vino
from .forms import VinoForm, BodegaForm, OrigenForm, VariedadForm, EstanteForm, VinoStockIncrementarForm, VinoStockDecrementarForm, SignUpForm

from .spotify import obtener_estilo_musical, obtener_url_de_spotify_por_genero
from .scanner import bar_code_scanner

# Create your views here.

#Login:
def custom_login(request): #Login
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Redirigir a la página anterior o a una página por defecto
            next_page = request.GET.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect('/')  # Página por defecto después del inicio de sesión
        else:
            error_message = 'Usuario o contraseña invalido'
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')

@login_required
def custom_signup(request): #Signup
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Registro exitoso! Ahora puedes iniciar sesión.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def custom_logout(request): #Logout
    logout(request)
    return redirect('/')

#Vino:
class VinoList(ListView): #Listar
    login_url = 'login'
    model = Vino
    template_name = 'index.html'
    context_object_name = 'vinos_list'

    def get_queryset(self): #Funcion para el buscador
        queryset = super().get_queryset()
        query = self.request.GET.get('search')
        if query:
            queryset = queryset.filter(
                Q(nombre__icontains=query) | 
                Q(bodega__bodega__contains=query) |
                Q(variedad__variedad__contains=query) |
                Q(cosecha__contains=query) |
                Q(origen__origen__contains=query) |
                Q(codigo__contains=query) |
                Q(estante__estante__contains=query)
            )
        return queryset

class DetalleVino(DetailView): #vino por ID:
    model = Vino
    template_name = 'vino_detail.html'
    context_object_name = 'vino'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_spotify'] = obtener_url_de_spotify_por_genero(obtener_estilo_musical(context['vino'].variedad.variedad))
        return context


@login_required
def crear_vino(request, codigo_vino):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        bodega = Bodega.objects.get(id=request.POST.get('bodega'))
        variedad = Variedad.objects.get(id=request.POST.get('variedad'))
        cosecha = request.POST.get('cosecha')
        origen = Origen.objects.get(id=request.POST.get('origen'))
        cantidad = request.POST.get('cantidad')
        precio = request.POST.get('precio')
        estante = Estante.objects.get(id=request.POST.get('estante'))
        imagen = request.POST.get('imagen')
        
        vino = Vino(
            nombre=nombre,
            bodega=bodega,
            variedad=variedad,
            cosecha=cosecha,
            origen=origen,
            cantidad=cantidad,
            codigo=codigo_vino,
            precio=precio,
            estante=estante,
            imagen = request.FILES['imagen']
        )
        vino.save()

        return redirect('/')
    else:
        bodegas = Bodega.objects.all()
        variedades = Variedad.objects.all()
        origenes = Origen.objects.all()
        estantes = Estante.objects.all()
        context = {
            'bodegas': bodegas,
            'variedades': variedades,
            'origenes': origenes,
            'estantes': estantes,
            'codigo': codigo_vino
        }

        return render(request, 'vino_create.html', context)


@method_decorator(login_required, name='dispatch')
class VinoUpdate(UpdateView): #Modificar
    login_url = 'login'
    model = Vino
    template_name = 'vino_create.html'
    form_class = VinoForm
    success_url = "/"

@method_decorator(login_required, name='dispatch')
class VinoDelete(DeleteView): #Eliminar
    login_url = 'login'
    model = Vino
    template_name = 'eliminar.html'
    form_class = VinoForm
    success_url = "/"

@login_required
def decrementar_stock(request, vino_id): #Decrementar el stock de los vinos
    vino = Vino.objects.get(id=vino_id) # Obtener el objeto Vino correspondiente al ID
    if request.method == 'POST':
        form = VinoStockDecrementarForm(request.POST)
        if form.is_valid():
            cantidad = form.cleaned_data['cantidad_a_decrementar'] # Obtener la cantidad de stock a decrementar del formulario
            if(cantidad <= vino.cantidad):
                # Decrementar el stock del objeto Vino y guardarlo
                vino.cantidad -= cantidad
                vino.save()
                # messages.success(request, f'Se han decrementado {cantidad} unidades del stock del vino {vino.nombre}')# Mostrar mensaje de éxito ver de mostrarlo como popup
                return redirect('/') #redirigimos al home
            else:
                # Mostrar mensaje de error
                messages.error(request, f'La cantidad especificada es mayor que el stock disponible ({vino.cantidad} unidades)')
    else:
        form = VinoStockDecrementarForm()
    return render(request, 'vino_actualizar_stock.html', {'form': form, 'vino': vino})

@login_required
def incrementar_stock(request, vino_id): #Incrementar el stock de los vinos
    vino = Vino.objects.get(id=vino_id) # Obtener el objeto Vino correspondiente al ID
    if request.method == 'POST':
        form = VinoStockIncrementarForm(request.POST)
        if form.is_valid():
            cantidad = form.cleaned_data['cantidad_a_incrementar'] # Obtener la cantidad de stock a incrementar del formulario
            # Incrementar el stock del objeto Vino y guardarlo
            vino.cantidad += cantidad
            vino.save()
            messages.success(request, f'Se han incrementado {cantidad} unidades del stock del vino {vino.nombre}')# Mostrar mensaje de éxito
            return redirect('/') #redirigimos al home
    else:
        form = VinoStockIncrementarForm()
    return render(request, 'vino_actualizar_stock.html', {'form': form, 'vino': vino})

@login_required
def verificar_vino(request):
    if request.method == 'POST':
        # Obtén el valor del botón presionado
        boton_presionado = request.POST.get('boton_presionado', None)

        # Verifica cuál de los botones se presionó
        if boton_presionado == 'verificar':
            # Obtener los datos del formulario
            codigo_barras = request.POST.get('codigo')

            if codigo_barras == '':
                messages.error(request, 'Debe ingresar un código de barras')
                return render(request, 'vino_verificar.html')
            
            else:
                #traemos el vino que tiene ese dato
                vino = Vino.objects.filter(codigo=codigo_barras)

                # Consultar si ya existe un objeto Vino con los mismos datos
                if vino.exists():
                    # Si ya existe, redirigir a la pagina para incrementar el stock
                    return redirect(f'/vino/incrementar/{vino.first().pk}/')
                else:
                    # Si no existe, redirigir a la página de creación de Vino
                    return redirect(f'/vino/{codigo_barras}/')

        elif boton_presionado == 'camera':
            codigo = bar_code_scanner()
            return redirect(f'/vino/verificar/?codigo={codigo}')

    # Si no se presionó ningún botón o se accedió a la vista mediante GET, renderiza el formulario
    return render(request, 'vino_verificar.html')



#Bodega:
@method_decorator(login_required, name='dispatch')
class BodegaList(ListView): #Listar
    login_url = 'login'
    model = Bodega
    template_name = 'bodega_list.html'
    context_object_name = 'bodegas_list'

    def get_queryset(self): #Funcion para el buscador
        queryset = super().get_queryset()
        query = self.request.GET.get('search')
        if query:
            queryset = queryset.filter(Q(bodega__icontains=query))
        return queryset

@method_decorator(login_required, name='dispatch')
class BodegaCreate(CreateView): #Crear
    login_url = 'login'
    model = Bodega
    template_name = 'bodega_create.html'
    form_class = BodegaForm
    success_url = "/bodega"

@method_decorator(login_required, name='dispatch')
class BodegaUpdate(UpdateView): #Modificar
    login_url = 'login'
    model = Bodega
    template_name = 'bodega_create.html'
    form_class = BodegaForm
    success_url = "/bodega"

@method_decorator(login_required, name='dispatch')
class BodegaDelete(DeleteView): #Eliminar
    login_url = 'login'
    model = Bodega
    template_name = 'eliminar.html'
    form_class = BodegaForm
    success_url = "/bodega"

#Origen:
@method_decorator(login_required, name='dispatch')
class OrigenList(ListView): #Listar
    login_url = 'login'
    model = Origen
    template_name = 'origen_list.html'
    context_object_name = 'origen_list'

    def get_queryset(self): #Funcion para el buscador
        queryset = super().get_queryset()
        query = self.request.GET.get('search')
        if query:
            queryset = queryset.filter(Q(origen__icontains=query))
        return queryset

@method_decorator(login_required, name='dispatch')
class OrigenCreate(CreateView): #Crear
    login_url = 'login'
    model = Origen
    template_name = 'origen_create.html'
    form_class = OrigenForm
    success_url = "/origen"

@method_decorator(login_required, name='dispatch')
class OrigenUpdate(UpdateView): #Modificar
    login_url = 'login'
    model = Origen
    template_name = 'origen_create.html'
    form_class = OrigenForm
    success_url = "/origen"

@method_decorator(login_required, name='dispatch')
class OrigenDelete(DeleteView): #Eliminar
    login_url = 'login'
    model = Origen
    template_name = 'eliminar.html'
    form_class = OrigenForm
    success_url = "/origen"

#Variedad:
@method_decorator(login_required, name='dispatch')
class VariedadList(ListView): #Listar
    login_url = 'login'
    model = Variedad
    template_name = 'variedad_list.html'
    context_object_name = 'variedad_list'

    def get_queryset(self): #Funcion para el buscador
        queryset = super().get_queryset()
        query = self.request.GET.get('search')
        if query:
            queryset = queryset.filter(Q(variedad__icontains=query))
        return queryset

@method_decorator(login_required, name='dispatch')
class VariedadCreate(CreateView): #Crear
    login_url = 'login'
    model = Variedad
    template_name = 'variedad_create.html'
    form_class = VariedadForm
    success_url = "/variedad"

@method_decorator(login_required, name='dispatch')
class VariedadUpdate(UpdateView): #Modificar
    login_url = 'login'
    model = Variedad
    template_name = 'variedad_create.html'
    form_class = VariedadForm
    success_url = "/variedad"

@method_decorator(login_required, name='dispatch')
class VariedadDelete(DeleteView): #Eliminar
    login_url = 'login'
    model = Variedad
    template_name = 'eliminar.html'
    form_class = VariedadForm
    success_url = "/variedad"

#Estante:
@method_decorator(login_required, name='dispatch')
class EstanteList(ListView): #Listar
    login_url = 'login'
    model = Estante
    template_name = 'estante_list.html'
    context_object_name = 'estente_list'

    def get_queryset(self): #Funcion para el buscador
        queryset = super().get_queryset()
        query = self.request.GET.get('search')
        if query:
            queryset = queryset.filter(Q(estante__icontains=query))
        return queryset

@method_decorator(login_required, name='dispatch')
class EstanteCreate(CreateView): #Crear
    login_url = 'login'
    model = Estante
    template_name = 'estante_create.html'
    form_class = EstanteForm
    success_url = "/estante"

@method_decorator(login_required, name='dispatch')
class EstanteUpdate(UpdateView): #Modificar
    login_url = 'login'
    model = Estante
    template_name = 'estante_create.html'
    form_class = EstanteForm
    success_url = "/estante"

@method_decorator(login_required, name='dispatch')
class EstanteDelete(DeleteView): #Eliminar
    login_url = 'login'
    model = Estante
    template_name = 'eliminar.html'
    form_class = EstanteForm
    success_url = "/estante"