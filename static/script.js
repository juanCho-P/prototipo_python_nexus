// --- TRANSICIÓN DE PANELES (LOGIN / REGISTRO) ---
const container = document.getElementById('container');
const registerBtn = document.getElementById('register');
const loginBtn = document.getElementById('login');

if (registerBtn && container) {
    registerBtn.addEventListener('click', () => {
        container.classList.add("active");
    });
}

if (loginBtn && container) {
    loginBtn.addEventListener('click', () => {
        container.classList.remove("active");
    });
}

// --- EVENTOS AL CARGAR EL DOM ---
document.addEventListener('DOMContentLoaded', () => {
    const toastContainer = document.getElementById('toast-container');
    const passInput = document.getElementById('reg-password');
    const confirmPassInput = document.getElementById('reg-confirm-password');
    const matchMsg = document.getElementById('pass-match-msg');
    const reqLength = document.getElementById('req-length');
    const reqNumber = document.getElementById('req-number');
    const avatarInput = document.getElementById('avatar-input');

    // 1. Mostrar nombre de archivo al subir avatar
    if (avatarInput) {
        avatarInput.addEventListener('change', (e) => {
            const textSpan = document.getElementById('file-label-text');
            if (textSpan) {
                textSpan.textContent = e.target.files.length > 0 ? e.target.files[0].name : 'Subir foto de perfil';
            }
        });
    }

    // 2. Validación de Contraseña en Tiempo Real
    if (passInput) {
        passInput.addEventListener('input', () => {
            const val = passInput.value;

            // Validar longitud
            if (reqLength) {
                const iconLength = reqLength.querySelector('i');
                if (val.length >= 8) {
                    reqLength.className = 'valid';
                    if (iconLength) iconLength.className = 'fa-solid fa-check';
                } else {
                    reqLength.className = 'invalid';
                    if (iconLength) iconLength.className = 'fa-solid fa-xmark';
                }
            }

            // Validar que no contenga únicamente números
            if (reqNumber) {
                const iconNumber = reqNumber.querySelector('i');
                if (val.length > 0 && !/^\d+$/.test(val)) {
                    reqNumber.className = 'valid';
                    if (iconNumber) iconNumber.className = 'fa-solid fa-check';
                } else {
                    reqNumber.className = 'invalid';
                    if (iconNumber) iconNumber.className = 'fa-solid fa-xmark';
                }
            }

            checkMatch();
        });
    }

    if (confirmPassInput) {
        confirmPassInput.addEventListener('input', checkMatch);
    }

    function checkMatch() {
        if (!confirmPassInput || !matchMsg) return;

        if (!confirmPassInput.value) {
            matchMsg.textContent = '';
            return;
        }

        if (passInput && passInput.value === confirmPassInput.value) {
            matchMsg.textContent = '✓ Las contraseñas coinciden';
            matchMsg.className = 'match-msg success';
        } else {
            matchMsg.textContent = '✕ Las contraseñas no coinciden';
            matchMsg.className = 'match-msg error';
        }
    }

    // 3. Notificaciones Toast Flotantes
    function showToast(message, type = 'error') {
        if (!toastContainer) return;

        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerText = message;
        
        toastContainer.appendChild(toast);
        
        setTimeout(() => toast.classList.add('show'), 50);

        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 4000);
    }

    // 4. Envío Asíncrono de Formularios (AJAX / Fetch)
    async function handleFormSubmit(event) {
        event.preventDefault(); // Evita la recarga de página
        
        const formElement = event.target;
        const formData = new FormData(formElement);

        try {
            const response = await fetch(formElement.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            const data = await response.json();

            if (response.ok && data.success) {
                showToast(data.message, 'success');
                if (data.redirect_url) {
                    setTimeout(() => window.location.href = data.redirect_url, 1200);
                } else {
                    formElement.reset();
                    const fileText = document.getElementById('file-label-text');
                    if (fileText) fileText.textContent = 'Subir foto de perfil';
                    if (matchMsg) matchMsg.textContent = '';
                }
            } else {
                showToast(data.message || 'Error en el formulario.', 'error');
            }
        } catch (err) {
            showToast('Error de comunicación con el servidor.', 'error');
        }
    }

    const loginForm = document.getElementById('form-login');
    const registerForm = document.getElementById('form-register');

    if (loginForm) loginForm.addEventListener('submit', handleFormSubmit);
    if (registerForm) registerForm.addEventListener('submit', handleFormSubmit);
});


const passInput = document.getElementById('reg-password');
const confirmPassInput = document.getElementById('reg-confirm-password');
const usernameInput = document.getElementById('reg-username');
const matchMsg = document.getElementById('pass-match-msg');

const reqLength = document.getElementById('req-length');
const reqNumber = document.getElementById('req-number');
const reqUser = document.getElementById('req-user');

if (passInput) {
    passInput.addEventListener('input', () => {
        const val = passInput.value;
        const userVal = usernameInput ? usernameInput.value.toLowerCase() : '';

        // 1. Validar longitud
        if (reqLength) {
            const icon = reqLength.querySelector('i');
            if (val.length >= 8) {
                reqLength.className = 'valid';
                if (icon) icon.className = 'fa-solid fa-check';
            } else {
                reqLength.className = 'invalid';
                if (icon) icon.className = 'fa-solid fa-xmark';
            }
        }

        // 2. Validar que no contenga únicamente números
        if (reqNumber) {
            const icon = reqNumber.querySelector('i');
            if (val.length > 0 && !/^\d+$/.test(val)) {
                reqNumber.className = 'valid';
                if (icon) icon.className = 'fa-solid fa-check';
            } else {
                reqNumber.className = 'invalid';
                if (icon) icon.className = 'fa-solid fa-xmark';
            }
        }

        // 3. Validar que no contenga el nombre de usuario
        if (reqUser) {
            const icon = reqUser.querySelector('i');
            if (val.length > 0 && userVal.length >= 3 && val.toLowerCase().includes(userVal)) {
                reqUser.className = 'invalid';
                if (icon) icon.className = 'fa-solid fa-xmark';
            } else if (val.length > 0) {
                reqUser.className = 'valid';
                if (icon) icon.className = 'fa-solid fa-check';
            } else {
                reqUser.className = 'invalid';
                if (icon) icon.className = 'fa-solid fa-xmark';
            }
        }

        checkMatch();
    });
}

// Alternar visibilidad de contraseña (Ojo)
const toggleButtons = document.querySelectorAll('.toggle-password');

toggleButtons.forEach(button => {
    button.addEventListener('click', () => {
        const targetId = button.getAttribute('data-target');
        const input = document.getElementById(targetId);

        if (input) {
            // Alterna el tipo de input
            const isPassword = input.getAttribute('type') === 'password';
            input.setAttribute('type', isPassword ? 'text' : 'password');

            // Cambia el icono entre ojo abierto y ojo tachado
            button.classList.toggle('fa-eye', !isPassword);
            button.classList.toggle('fa-eye-slash', isPassword);
        }
    });
});