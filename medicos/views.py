from django.shortcuts import render, redirect
from .models import PuestoSalud, RegistroUsuario
from .forms import RegistroUsuarioForm

def registrar_equipo(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_equipos')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'medicos/registrar_equipo.html', {'form': form})

def lista_equipos(request):
    puestos = ['Rodeo', 'Rivera', 'Petecuy']
    estadisticas = []

    for nombre_puesto in puestos:
        puesto_obj, _ = PuestoSalud.objects.get_or_create(nombre=nombre_puesto)
        usuarios = RegistroUsuario.objects.filter(puesto=puesto_obj)
        total_usuarios = usuarios.count()

        total_micro = usuarios.filter(microbiologia=True).count()
        total_bact = usuarios.filter(bacteriologia=True).count()
        total_quim = usuarios.filter(quimica=True).count()

        total_pruebas = total_micro + total_bact + total_quim

        pct_micro = (total_micro / total_pruebas * 100) if total_pruebas > 0 else 0
        pct_bact = (total_bact / total_pruebas * 100) if total_pruebas > 0 else 0
        pct_quim = (total_quim / total_pruebas * 100) if total_pruebas > 0 else 0

        estadisticas.append({
            'puesto': nombre_puesto,
            'total_usuarios': total_usuarios,
            'micro': total_micro,
            'bact': total_bact,
            'quim': total_quim,
            'pct_micro': round(pct_micro, 1),
            'pct_bact': round(pct_bact, 1),
            'pct_quim': round(pct_quim, 1),
            'total_pruebas': total_pruebas,
        })

    usuarios_registrados = RegistroUsuario.objects.all().order_by('-fecha_registro')

    return render(request, 'medicos/lista_equipos.html', {
        'estadisticas': estadisticas,
        'usuarios_registrados': usuarios_registrados
    })