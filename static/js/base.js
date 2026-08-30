
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

// Toggle Sidebar
const sidebar = document.getElementById("sidebar");
const sidebarToggle = document.getElementById("sidebarToggle");
const mobileMenu = document.getElementById("mobileMenu");

if (sidebarToggle) {
    sidebarToggle.addEventListener("click", () => sidebar.classList.toggle("collapsed"));
}
if (mobileMenu) {
    mobileMenu.addEventListener("click", () => sidebar.classList.toggle("mobile-open"));
}

// Modal Flotante de Notificaciones
const notifBtn = document.getElementById("notifBtn");
const notifPopover = document.getElementById("notifPopover");

if (notifBtn && notifPopover) {
    notifBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        notifPopover.classList.toggle("active");
    });

    document.addEventListener("click", (e) => {
        if (!notifPopover.contains(e.target) && !notifBtn.contains(e.target)) {
            notifPopover.classList.remove("active");
        }
    });
}

// Marcar Notificaciones como leídas AJAX
const markAllBtn = document.getElementById("markAllReadBtn");
if (markAllBtn) {
    markAllBtn.addEventListener("click", () => {
        fetch("/notification/marcar-todas/", { // Ajusta esta ruta si es diferente en tu urls.py
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken,
                "Content-Type": "application/json"
            }
        }).then(res => {
            if (res.ok) {
                const badge = document.getElementById("notifBadge");
                if (badge) badge.remove();
                document.querySelectorAll(".notif-item.unread").forEach(el => el.classList.remove("unread"));
            }
        });
    });
}

// Marcar individual como leída
document.querySelectorAll(".mark-read").forEach(btn => {
    btn.addEventListener("click", (e) => {
        e.stopPropagation();
        const id = btn.dataset.id;
        fetch(`/notification/marcar/${id}/`, {
            method: "POST",
            headers: { 
                "X-CSRFToken": csrftoken,
                "X-Requested-With": "XMLHttpRequest"
            }
        }).then(res => {
            if (res.ok) {
                const item = btn.closest(".notif-item");
                if (item) item.classList.remove("unread");
                btn.remove();
            }
        });
    });
});

// Eliminar notificación individual
document.querySelectorAll(".delete-notif").forEach(btn => {
    btn.addEventListener("click", (e) => {
        e.stopPropagation();
        const id = btn.dataset.id;
        
        fetch(`/notification/eliminar/${id}/`, {
            method: "POST",
            headers: { 
                "X-CSRFToken": csrftoken,
                "X-Requested-With": "XMLHttpRequest"
            }
        }).then(async res => {
            if (res.ok) {
                let data = {};
                try {
                    data = await res.json();
                } catch (err) {
                    // Si la vista no devuelve JSON, se maneja de forma limpia
                }

                const item = btn.closest(".notif-item");
                if (item) item.remove();

                const badge = document.getElementById("notifBadge");
                if (badge) {
                    if (data.unread_count !== undefined && data.unread_count > 0) {
                        badge.textContent = data.unread_count;
                    } else if (data.unread_count === 0) {
                        badge.remove();
                    } else {
                        let currentCount = parseInt(badge.textContent) - 1;
                        if (currentCount > 0) {
                            badge.textContent = currentCount;
                        } else {
                            badge.remove();
                        }
                    }
                }

                const notifList = document.getElementById("notifList");
                if (notifList && notifList.querySelectorAll(".notif-item").length === 0) {
                    notifList.innerHTML = '<div class="empty-notif">No tienes notificaciones.</div>';
                }
            }
        });
    });
});