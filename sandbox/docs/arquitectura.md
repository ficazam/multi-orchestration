# Arquitectura

El servicio de auth valida contra la tabla `users`.
La columna de ultimo acceso se llama `last_seen_at`, no `last_login`.
El correo se guarda tal cual lo escribe el usuario, sin normalizar.
