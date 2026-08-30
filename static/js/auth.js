document.addEventListener('DOMContentLoaded', () => {
    // --- 1. TRANSICIÓN DE PANELES (LOGIN / REGISTRO) ---
    const container = document.getElementById('container');
    const registerBtn = document.getElementById('register');
    const loginBtn = document.getElementById('login');

    if (registerBtn && container) {
        registerBtn.addEventListener('click', () => container.classList.add("active"));
    }

    if (loginBtn && container) {
        loginBtn.addEventListener('click', () => container.classList.remove("active"));
    }

    // --- 2. VISTA PREVIA DE AVATAR ---
    const avatarInput = document.getElementById('avatar-input');
    if (avatarInput) {
        avatarInput.addEventListener('change', (e) => {
            const textSpan = document.getElementById('file-label-text');
            const previewImg = document.getElementById('avatar-preview');
            
            if (e.target.files.length > 0) {
                const file = e.target.files[0];
                if (textSpan) textSpan.textContent = file.name;
                if (previewImg) previewImg.src = URL.createObjectURL(file);
            }
        });
    }

    // --- 3. VALIDACIÓN DE CONTRASEÑA EN TIEMPO REAL ---
    const passInput = document.getElementById('reg-password');
    const confirmPassInput = document.getElementById('reg-confirm-password');
    const usernameInput = document.getElementById('reg-username');
    const matchMsg = document.getElementById('pass-match-msg');

    const reqLength = document.getElementById('req-length');
    const reqNumber = document.getElementById('req-number');
    const reqUser = document.getElementById('req-user');

    function checkMatch() {
        if (!confirmPassInput || !matchMsg) return;

        if (!confirmPassInput.value) {
            matchMsg.textContent = '';
            matchMsg.className = 'match-msg';
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

    if (passInput) {
        passInput.addEventListener('input', () => {
            const val = passInput.value;
            const userVal = usernameInput ? usernameInput.value.toLowerCase() : '';

            // Validar longitud (Mínimo 8)
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

            // Validar que no sea solo números
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

            // Validar que no contenga el nombre de usuario
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

    if (confirmPassInput) {
        confirmPassInput.addEventListener('input', checkMatch);
    }

    // --- 4. TOGGLE VISIBILIDAD DE CONTRASEÑA (OJOS) ---
    const toggleButtons = document.querySelectorAll('.toggle-password');
    toggleButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetId = button.getAttribute('data-target');
            const input = document.getElementById(targetId);

            if (input) {
                const isPassword = input.getAttribute('type') === 'password';
                input.setAttribute('type', isPassword ? 'text' : 'password');
                button.classList.toggle('fa-eye', !isPassword);
                button.classList.toggle('fa-eye-slash', isPassword);
            }
        });
    });

    // --- 5. NOTIFICACIONES TOAST ---
    const toastContainer = document.getElementById('toast-container');

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

    // --- 6. ENVÍO ASÍNCRONO DE FORMULARIOS (AJAX) ---
    async function handleFormSubmit(event) {
        event.preventDefault();
        
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