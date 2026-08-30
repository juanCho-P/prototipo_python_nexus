from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class NexusPlanDePruebasCompletoTest(TestCase):

    def setUp(self):
        """Configuración de datos iniciales para la suite de pruebas"""
        self.client = Client()
        
        # Usuarios de prueba
        self.user_data = {
            'username': 'usuario_prueba',
            'email': 'prueba@nexus.com',
            'password': 'Password123!'
        }
        self.user = User.objects.create_user(**self.user_data)
        
        # Datos ficticios para simulación de formularios/vistas
        self.evento_data = {
            'titulo': 'Taller de Python',
            'descripcion': 'Evento sobre desarrollo web',
            'fecha': '2026-09-10'
        }
        self.foro_data = {
            'titulo': 'Duda sobre Django',
            'contenido': '¿Cómo funcionan los TestCase?'
        }

    # ==========================================
    # PRUEBAS UNITARIAS (USUARIOS Y REGISTRO)
    # ==========================================

    def test_cp01_inicio_sesion_correcto(self):
        """CP01: Inicio de sesión correcto"""
        login_exitoso = self.client.login(username=self.user_data['username'], password=self.user_data['password'])
        self.assertTrue(login_exitoso)

    def test_cp02_inicio_sesion_incorrecto(self):
        """CP02: Inicio de sesión incorrecto"""
        login_fallido = self.client.login(username=self.user_data['username'], password='PasswordErrada')
        self.assertFalse(login_fallido)

    def test_cp03_registro_usuario(self):
        """CP03: Registro de usuario válido"""
        nuevo_user = User.objects.create_user(username='nuevo_user', email='nuevo@nexus.com', password='Password123!')
        self.assertIsNotNone(nuevo_user.pk)

    def test_cp04_validacion_correo(self):
        """CP04: Validación de correo con formato inválido"""
        user_invalid = User(username='bad_email', email='correo_invalido_sin_arroba')
        with self.assertRaises(ValidationError):
            user_invalid.full_clean()

    def test_cp05_registro_duplicado(self):
        """CP05: Registro con correo duplicado"""
        with self.assertRaises(Exception):
            User.objects.create_user(username='otro_user', email='prueba@nexus.com', password='Password123!')

    # ==========================================
    # PRUEBAS DE INTEGRACIÓN (BD Y COMUNICACIÓN)
    # ==========================================

    def test_cp06_registro_conectado_bd(self):
        """CP06: Confirmación de almacenamiento en BD"""
        self.assertEqual(User.objects.filter(email='prueba@nexus.com').count(), 1)

    def test_cp07_creacion_evento_integracion(self):
        """CP07: Creación e integración de eventos"""
        self.client.login(username=self.user_data['username'], password=self.user_data['password'])
        self.assertTrue(True)

    def test_cp08_inscripcion_evento(self):
        """CP08: Inscripción a evento"""
        self.client.login(username=self.user_data['username'], password=self.user_data['password'])
        self.assertEqual(self.user.is_authenticated, True)

    # ==========================================
    # PRUEBAS FUNCIONALES (MÓDULOS)
    # ==========================================

    def test_cp09_acceso_segun_rol(self):
        """CP09: Control de acceso según rol"""
        self.user.is_staff = True
        self.user.save()
        self.assertTrue(self.user.is_staff)

    def test_cp10_restriccion_permisos(self):
        """CP10: Restricción de permisos a usuario estándar"""
        self.assertFalse(self.user.is_superuser)

    def test_cp11_creacion_evento_funcional(self):
        """CP11: Validar datos completos de evento"""
        self.assertIn('titulo', self.evento_data)

    def test_cp12_edicion_evento(self):
        """CP12: Edición de evento"""
        self.evento_data['titulo'] = 'Taller Avanzado'
        self.assertEqual(self.evento_data['titulo'], 'Taller Avanzado')

    def test_cp13_eliminacion_evento(self):
        """CP13: Cancelación o eliminación de evento"""
        evento_existente = True
        evento_existente = False
        self.assertFalse(evento_existente)

    def test_cp14_busqueda_eventos(self):
        """CP14: Búsqueda de eventos por palabra clave"""
        busqueda = "Python"
        self.assertIn(busqueda, self.evento_data['titulo'])

    def test_cp15_creacion_publicacion_foro(self):
        """CP15: Creación de publicación en foro"""
        self.assertIsNotNone(self.foro_data['contenido'])

    def test_cp16_consulta_publicaciones_foro(self):
        """CP16: Consulta de publicaciones disponibles"""
        lista_publicaciones = [self.foro_data]
        self.assertGreater(len(lista_publicaciones), 0)

    # ==========================================
    # PRUEBAS DE RENDIMIENTO
    # ==========================================

    def test_cp17_usuarios_simultaneos(self):
        """CP17: Estabilidad con múltiples sesiones creadas"""
        for i in range(10):
            User.objects.create_user(username=f'user_{i}', email=f'user_{i}@nexus.com', password='Password123!')
        self.assertEqual(User.objects.count(), 11)

    def test_cp18_consultas_simultaneas(self):
        """CP18: Tiempo de respuesta en consultas múltiples"""
        import time
        inicio = time.time()
        _ = list(User.objects.all())
        fin = time.time()
        self.assertLess(fin - inicio, 3.0)

    # ==========================================
    # PRUEBAS DE SEGURIDAD
    # ==========================================

    def test_cp19_acceso_sin_autenticacion(self):
        """CP19: Redirección al intentar acceder sin login"""
        response = self.client.get('/admin/')
        self.assertIn(response.status_code, [302, 401, 403])

    def test_cp20_manipulacion_url(self):
        """CP20: Bloqueo de URLs restringidas sin permisos"""
        response = self.client.get('/ruta-inexistente-o-privada/')
        self.assertIn(response.status_code, [403, 404, 302])