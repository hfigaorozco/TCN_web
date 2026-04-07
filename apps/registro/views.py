from django.shortcuts import render, redirect
from apps.login.models import Usuario

def registro(request):
    error = None

    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        correo = request.POST.get('correo', '').strip()
        password = request.POST.get('password', '').strip()
        rol = request.POST.get('rol', '').strip()

        if not nombre:
            error = 'El nombre es obligatorio'
        elif not correo:
            error = 'El correo es obligatorio'
        elif not password:
            error = 'La contraseña es obligatoria'
        elif not rol:
            error = 'El rol es obligatorio'
        elif Usuario.objects.filter(email=correo).exists():
            error = f'Ya existe una cuenta con el correo {correo}'
        else:
            Usuario.objects.create_user(
                email=correo,
                password=password,
                nombre=nombre,
                rol=rol,
            )
            return redirect('login')

    context = {'error': error}
    
    return render(request, 'registro.html', context)