from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.contrib import messages
from django.db import transaction
from django.urls import reverse
# Importamos las funciones de autenticación real
from django.contrib.auth import login, logout, authenticate
import json
from collections import Counter
import re 
from django.conf import settings 

# --- IMPORTACIONES LOCALES ---
# Asegúrate de que crypto_utils y models existan
from .crypto_utils import generate_rsa_keys, sign_vote, encrypt_vote_aes, verify_signature
from .models import VoterProfile, Vote 
# IMPORTANTE: Importamos los nuevos formularios que creamos en forms.py
from .forms import CustomRegisterForm, CustomLoginForm, KeyCheckForm

from Crypto.PublicKey import RSA

# --- Funciones Auxiliares (Para el Dashboard) ---
def parse_vote_content(vote_option):
    """Extrae las respuestas P1 a P4 de la cadena de voto (P#:VALOR)."""
    results = {}
    # Patrón: (P#):(VALOR)
    matches = re.findall(r'(P\d+):([A-Z0-9\-]+)', vote_option)
    for key, value in matches:
        results[key] = value
    return results

def get_legible_label(key, value):
    """Mapea valores de código a etiquetas legibles."""
    if key == 'P1': 
        return {'ALTO': 'Alto', 'MEDIO': 'Medio', 'BAJO': 'Bajo'}.get(value, value)
    if key == 'P2': 
        return {'FACIL': 'Fáciles', 'ADECUADO': 'Adecuados', 'DIFICIL': 'Difíciles'}.get(value, value)
    if key == 'P3': 
        return {'MUCHO': 'Sí, mucho', 'TAL-VEZ': 'Tal vez', 'NO-DUDA': 'No, lo dudo'}.get(value, value)
    if key == 'P4': 
        return {'RAPIDO': 'Muy rápido', 'ADECUADO': 'Adecuados', 'LENTO': 'Muy lento'}.get(value, value)
    return value
# --- Fin de Funciones Auxiliares ---


# --- VISTA DE PORTADA (index_view) ---
def index_view(request):
    """Renderiza la portada o redirige a la guía."""
    if request.user.is_authenticated:
        # CAMBIO: Si entra al inicio y ya es usuario, va a la guía
        return redirect('voting:guide') 
        
    context = {
        'github_url': getattr(settings, 'GITHUB_REPO_URL', '#'), 
    }
        
    return render(request, 'voting/index.html', context)


# --- VISTA DEDICADA DE CRÉDITOS ---
def credits_view(request):
    """Renderiza la página dedicada a los créditos del proyecto."""
    context = {
        'github_url': getattr(settings, 'GITHUB_REPO_URL', '#'), 
        'materia': 'Criptografía',
        'profesor': 'Dr. Alfonso Francisco De Abiega L Eglisse',
        'grupo_semestre': '02 / 2026-1',
        'institucion': 'Facultad de Ingeniería UNAM',
        'integrantes': ['Roja Mares Luis Iván', 'Lee Obando Ileana Verónica'],
        'descripcion': 'Proyecto final de la materia.',
    }
    return render(request, 'voting/credits.html', context)


# --- NUEVA VISTA DE LOGIN (Soluciona el fallo de seguridad) ---
# En voting/views.py

def login_view(request):
    """
    Maneja el inicio de sesión y fuerza la redirección a la GUÍA.
    """
    # 1. Si ya está logueado, mándalo a la guía (evita bucles)
    if request.user.is_authenticated:
        return redirect('voting:guide') 

    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user() 
            login(request, user)
            messages.success(request, f"Bienvenido de nuevo.")
            
            # --- CAMBIO CRÍTICO ---
            # NO uses 'next'. Forzamos la redirección a 'voting:guide'
            # Esto evita que si intentaste entrar a /vote/, te lleve allí.
            return redirect('voting:guide') 
            
        else:
            messages.error(request, "Correo electrónico o contraseña incorrectos.")
    else:
        form = CustomLoginForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    """Cierra la sesión del usuario de forma segura."""
    logout(request)
    messages.info(request, "Has cerrado sesión exitosamente.")
    return redirect('login')


# --- VISTA DE REGISTRO MODIFICADA (register_view) ---
def register_view(request):
    """
    Maneja el registro usando el nuevo formulario CustomRegisterForm.
    Valida correos, bloquea dominios temporales y caracteres raros.
    """
    if request.user.is_authenticated:
        return redirect('voting:vote_submit')

    if request.method == 'POST':
        # Usamos CustomRegisterForm en lugar de UserCreationForm
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, '¡Registro exitoso! Tu cuenta ha sido creada con tu correo electrónico.')
            return redirect('login') 
        else:
            messages.error(request, 'Hubo un error en el registro. Revisa las alertas en el formulario.')
    else:
        form = CustomRegisterForm()
        
    # Renderiza el template que está en templates/register.html
    return render(request, 'register.html', {'form': form})


# --- Vista para la Generación de Llaves (key_generation_view) ---
@login_required
def key_generation_view(request):
    """
    Genera el par de llaves RSA. Permite la regeneración SOLO si el usuario
    NO ha emitido su voto previamente.
    """
    profile = get_object_or_404(VoterProfile, user=request.user)

    # 🛑 RESTRICCIÓN DE INTEGRIDAD CRIPTOGRÁFICA 🛑
    if profile.has_voted:
        messages.error(request, 
                       "Tu voto ya ha sido emitido: No es posible generar una nueva llave pública una vez que se ha registrado un voto.")
        return redirect('voting:verification_page') 

    # Si el usuario NO ha votado:
    if request.method == 'POST':
        public_key_pem, private_key_pem = generate_rsa_keys()
        
        # Guardar la nueva llave pública
        profile.public_key = public_key_pem
        profile.save()
        
        # Usamos el username (que ahora es el email) para el nombre del archivo, 
        # limpiando caracteres para que sea un nombre de archivo válido.
        safe_filename = "".join([c for c in request.user.username if c.isalpha() or c.isdigit() or c==' ']).rstrip()
        filename = f"{safe_filename}_private.key"
        
        response = HttpResponse(private_key_pem, content_type='application/x-pem-file')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        messages.success(request, "Llave privada generada y descargada con éxito. Guárdala de forma segura. Ya puedes votar.")
        return response 
    
    return render(request, 'voting/key_generation.html', {'profile': profile})


# --- Vista de Emisión de Voto y Firma (vote_submission_view) ---
@login_required
def vote_submission_view(request):
    """Procesa el voto, genera la firma digital y lo registra."""
    profile = get_object_or_404(VoterProfile, user=request.user)
    
    if profile.has_voted:
        messages.warning(request, "Ya has votado. No puedes votar de nuevo.")
        return redirect('voting:success_page') 

    if not profile.public_key:
        messages.error(request, "No tienes una llave pública registrada. Por favor, genera tu llave primero.")
        return redirect('voting:generate_keys')


    if request.method == 'POST':
        # CAPTURA DE LAS 4 PREGUNTAS
        pregunta_1 = request.POST.get('pregunta_1')
        pregunta_2 = request.POST.get('pregunta_2')
        pregunta_3 = request.POST.get('pregunta_3')
        pregunta_4 = request.POST.get('pregunta_4')
        private_key_file = request.FILES.get('private_key') 

        if not all([pregunta_1, pregunta_2, pregunta_3, pregunta_4]) or not private_key_file:
            messages.error(request, "Debes responder todas las preguntas y subir tu llave privada.")
            return render(request, 'voting/vote_form.html', {'profile': profile})

        try:
            private_key_pem = private_key_file.read().decode('utf-8')

            # CONCATENACIÓN DE LAS 4 RESPUESTAS
            vote_content = (
                f"USUARIO:{request.user.username}|P1:{pregunta_1}|P2:{pregunta_2}|P3:{pregunta_3}|P4:{pregunta_4}"
            )

            # Lógica de firma y verificación
            signature_hex = sign_vote(vote_content, private_key_pem)
            
            if not verify_signature(vote_content, signature_hex, profile.public_key):
                 messages.error(request, "La llave privada subida no corresponde a su llave pública registrada.")
                 return redirect(reverse('voting:vote_submit')) 

            encrypted_vote_hex = encrypt_vote_aes(vote_content)

            with transaction.atomic():
                Vote.objects.create(
                    voter=profile,
                    option=vote_content, 
                    digital_signature=signature_hex,
                    encrypted_vote=encrypted_vote_hex
                )
                profile.has_voted = True
                profile.save()
            
            messages.success(request, "¡Voto firmado y procesado con éxito!")
            request.session['last_signature'] = signature_hex
            return redirect('voting:success_page')

        except Exception as e:
            messages.error(request, f"Error Criptográfico o de Archivo: {e}")
            return render(request, 'voting/vote_form.html', {'profile': profile})

    return render(request, 'voting/vote_form.html', {'profile': profile})


# --- VISTA DE PÁGINA DE ÉXITO (success_page) ---
@login_required
def success_page(request):
    """Muestra la página de éxito con el comprobante digital."""
    signature = request.session.pop('last_signature', "Comprobante no disponible.")
    
    return render(request, 'voting/success.html', {'signature': signature})


# --- LÓGICA DE CONTEO PARA GRÁFICOS ---
def get_counts_for_question(question_key, votes):
    """Función auxiliar para contar votos por pregunta y preparar el JSON."""
    results = []
    for vote in votes:
        parsed_data = parse_vote_content(vote.option)
        if question_key in parsed_data:
            results.append(parsed_data[question_key])
    
    counts = Counter(results)
    options = [get_legible_label(question_key, key) for key in counts.keys()]
    
    return {
        'options': json.dumps(options), 
        'counts': json.dumps(list(counts.values()))
    }

# --- VISTA DE TABLERO PÚBLICO (results_dashboard_view) ---
@login_required 
def results_dashboard_view(request):
    """Muestra los gráficos de resultados (Tablero Público)."""
    is_admin = request.user.is_staff
    all_votes = Vote.objects.all().select_related('voter').order_by('id') 
    
    # Datos para los 4 gráficos
    data_p1 = get_counts_for_question('P1', all_votes)
    data_p2 = get_counts_for_question('P2', all_votes)
    data_p3 = get_counts_for_question('P3', all_votes)
    data_p4 = get_counts_for_question('P4', all_votes)

    total_votes = len(all_votes)

    context = {
        'total_votes': total_votes,
        'options_json_p1': data_p1['options'], 'counts_json_p1': data_p1['counts'],
        'options_json_p2': data_p2['options'], 'counts_json_p2': data_p2['counts'],
        'options_json_p3': data_p3['options'], 'counts_json_p3': data_p3['counts'],
        'options_json_p4': data_p4['options'], 'counts_json_p4': data_p4['counts'],
        
        'is_admin': is_admin, 
        'is_verification_page': False, 
        'is_audit_page': False, 
    }
    
    return render(request, 'voting/results_dashboard.html', context)


# --- NUEVA VISTA DE AUDITORÍA DETALLADA (audit_view) ---
@login_required
def audit_view(request):
    """Muestra el registro inmutable de auditoría completo (Solo para staff/admin)."""
    if not request.user.is_staff:
        messages.error(request, "Acceso Denegado: Solo el personal de administración puede acceder a la auditoría.")
        return redirect('voting:results_dashboard')
        
    all_votes = Vote.objects.all().select_related('voter').order_by('id') 
    
    processed_votes = []
    for vote in all_votes:
        parsed_data = parse_vote_content(vote.option)
        
        processed_votes.append({
            'id': vote.id,
            'voter_username': vote.voter.user.username,
            'encrypted_vote': vote.encrypted_vote,
            'digital_signature': vote.digital_signature,
            'timestamp': vote.timestamp,
            'P1': get_legible_label('P1', parsed_data.get('P1', 'N/A')),
            'P2': get_legible_label('P2', parsed_data.get('P2', 'N/A')),
            'P3': get_legible_label('P3', parsed_data.get('P3', 'N/A')),
            'P4': get_legible_label('P4', parsed_data.get('P4', 'N/A')),
        })
    
    context = {
        'votes': processed_votes, 
        'is_admin': True, 
        'is_verification_page': False, 
        'is_audit_page': True, 
    }
    
    return render(request, 'voting/results_dashboard.html', context)


# --- VISTA DE VERIFICACIÓN INDIVIDUAL (verification_page) ---
@login_required
def verification_page(request):
    """Muestra la tabla de verificación (hash y firma) del voto del usuario actual."""
    user_votes = Vote.objects.filter(voter__user=request.user).select_related('voter').order_by('-timestamp')
    
    context = {
        'votes': user_votes,
        'is_admin': False, 
        'is_verification_page': True, 
        'is_audit_page': False,
    }
    
    return render(request, 'voting/results_dashboard.html', context)

# --- VISTA DE GUÍA DE USUARIO ---
def guide_view(request):
    """Renderiza la guía paso a paso de cómo votar."""
    return render(request, 'voting/guide.html')

# --- VISTA DE VALIDACIÓN DE ESTADO DE LLAVE (check_key_status) ---
@login_required
def check_key_status(request):
    """
    Permite al usuario subir su llave para verificar:
    1. Si es una llave RSA válida.
    2. Si corresponde a su usuario.
    3. Si ya fue utilizada para votar.
    """
    profile = get_object_or_404(VoterProfile, user=request.user)
    key_status = None # Puede ser: 'valid_ready', 'valid_used', 'invalid_format', 'mismatch', 'no_key_registered'
    
    if request.method == 'POST':
        form = KeyCheckForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['private_key']
            try:
                # 1. Intentamos leer la llave (Detectar si es Falsa/Corrupta)
                key_content = uploaded_file.read().decode('utf-8')
                private_key_obj = RSA.import_key(key_content)
                
                # 2. Verificamos si el usuario tiene una llave registrada en el sistema
                if not profile.public_key:
                    key_status = 'no_key_registered'
                else:
                    # 3. Derivamos la pública de la privada subida y comparamos (Detectar si es de otro usuario)
                    # Normalizamos quitando espacios en blanco extras
                    uploaded_public_pem = private_key_obj.publickey().export_key('PEM').decode('utf-8').strip()
                    stored_public_pem = profile.public_key.strip()
                    
                    if uploaded_public_pem != stored_public_pem:
                        key_status = 'mismatch' # Es una llave válida, pero no es la de este usuario
                    else:
                        # 4. Verificar si ya se usó
                        if profile.has_voted:
                            key_status = 'valid_used'
                        else:
                            key_status = 'valid_ready'

            except (ValueError, IndexError, TypeError) as e:
                # Si RSA.import_key falla, el archivo no es una llave válida
                key_status = 'invalid_format'
    else:
        form = KeyCheckForm()

    return render(request, 'voting/check_key.html', {
        'form': form, 
        'key_status': key_status,
        'profile': profile
    })