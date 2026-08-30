 // Toggle Sidebar
        const sidebar = document.getElementById("sidebar");
        document.getElementById("sidebarToggle").addEventListener("click", () => sidebar.classList.toggle("collapsed"));
        document.getElementById("mobileMenu").addEventListener("click", () => sidebar.classList.toggle("mobile-open"));

        // Modal Flotante de Notificaciones
        const notifBtn = document.getElementById("notifBtn");
        const notifPopover = document.getElementById("notifPopover");

        notifBtn.addEventListener("click", (e) => {
            e.stopPropagation();
            notifPopover.classList.toggle("active");
        });

        document.addEventListener("click", (e) => {
            if (!notifPopover.contains(e.target) && !notifBtn.contains(e.target)) {
                notifPopover.classList.remove("active");
            }
        });

        // Marcar Notificaciones como leídas AJAX
        const markAllBtn = document.getElementById("markAllReadBtn");
        if (markAllBtn) {
            markAllBtn.addEventListener("click", () => {
                fetch("{% url 'marcar_notificaciones_leidas' %}", {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": "{{ csrf_token }}",
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
                "X-CSRFToken": "{{ csrf_token }}",
                "X-Requested-With": "XMLHttpRequest"
            }
        }).then(res => {
            if (res.ok) {
                const item = btn.closest(".notif-item");
                item.classList.remove("unread");
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
                    "X-CSRFToken": "{{ csrf_token }}",
                    "X-Requested-With": "XMLHttpRequest"
                }
            }).then(res => {
                if (res.ok) {
                    btn.closest(".notif-item").remove();
                }
            });
        });
    });


    document.querySelectorAll(".delete-notif").forEach(btn => {
    btn.addEventListener("click", (e) => {
        e.stopPropagation();
        const id = btn.dataset.id;
        fetch(`/notification/eliminar/${id}/`, {
            method: "POST",
            headers: { 
                "X-CSRFToken": "{{ csrf_token }}",
                "X-Requested-With": "XMLHttpRequest"
            }
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === 'success') {
                // Eliminar el elemento visualmente
                btn.closest(".notif-item").remove();

                // Actualizar o remover el badge del contador
                const badge = document.getElementById("notifBadge");
                if (badge) {
                    if (data.unread_count > 0) {
                        badge.textContent = data.unread_count;
                    } else {
                        badge.remove();
                    }
                }

                // Si ya no quedan elementos, mostrar mensaje de vacío
                const notifList = document.getElementById("notifList");
                if (notifList && notifList.querySelectorAll(".notif-item").length === 0) {
                    notifList.innerHTML = '<div class="empty-notif">No tienes notificaciones.</div>';
                }
            }
        });
    });
});