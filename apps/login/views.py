from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


def inicio_sesion(request):
    error = None

    if request.method == 'POST':
        correo = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        if not correo:
            error = 'El correo es obligatorio'
        elif not password:
            error = 'La contraseña es obligatoria'
        else:
            user = authenticate(request, username=correo, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                error = 'Correo o contraseña son incorrectos'

    context = {'error': error}
    
    return render(request, 'login.html', context)