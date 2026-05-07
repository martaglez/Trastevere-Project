import os

FROM_EMAIL = os.environ.get("RESEND_FROM", "Trastevere <onboarding@resend.dev>")
APP_URL    = os.environ.get("APP_URL", "https://trastevere.onrender.com")


def _send(payload: dict):
    import resend
    resend.api_key = os.environ.get("RESEND_API_KEY", "")
    resend.Emails.send(payload)


def send_welcome_email(to_email: str, username: str, lang: str = 'es'):
    if lang == 'en':
        subject = "Welcome to Trastevere! 🍅"
        body = f"""
        <div style="font-family:sans-serif;max-width:500px;margin:0 auto;padding:32px 24px;background:#fdf6ee;border-radius:16px;">
            <h1 style="font-family:Georgia,serif;color:#ff6347;font-size:2rem;margin-bottom:8px;">Trastevere 🍅</h1>
            <h2 style="color:#222;font-size:1.3rem;margin-bottom:16px;">Hi, {username}!</h2>
            <p style="color:#555;line-height:1.6;">
                Welcome to <strong>Trastevere</strong>, your recipe social network.<br>
                You can now share your dishes, follow other cooks and discover amazing recipes.
            </p>
            <a href="{APP_URL}" style="display:inline-block;margin-top:24px;padding:12px 28px;
               background:#ff6347;color:white;border-radius:10px;text-decoration:none;font-weight:700;">
                Start cooking →
            </a>
            <p style="color:#aaa;font-size:0.8rem;margin-top:32px;">
                © Trastevere Team · If you didn't create this account, please ignore this email.
            </p>
        </div>"""
    else:
        subject = "¡Bienvenido a Trastevere! 🍅"
        body = f"""
        <div style="font-family:sans-serif;max-width:500px;margin:0 auto;padding:32px 24px;background:#fdf6ee;border-radius:16px;">
            <h1 style="font-family:Georgia,serif;color:#ff6347;font-size:2rem;margin-bottom:8px;">Trastevere 🍅</h1>
            <h2 style="color:#222;font-size:1.3rem;margin-bottom:16px;">¡Hola, {username}!</h2>
            <p style="color:#555;line-height:1.6;">
                Bienvenido a <strong>Trastevere</strong>, tu red social de recetas.<br>
                Ya puedes compartir tus platos, seguir a otros cocineros y descubrir recetas increíbles.
            </p>
            <a href="{APP_URL}" style="display:inline-block;margin-top:24px;padding:12px 28px;
               background:#ff6347;color:white;border-radius:10px;text-decoration:none;font-weight:700;">
                Empezar a cocinar →
            </a>
            <p style="color:#aaa;font-size:0.8rem;margin-top:32px;">
                © Trastevere Team · Si no creaste esta cuenta, ignora este email.
            </p>
        </div>"""
    _send({"from": FROM_EMAIL, "to": [to_email], "subject": subject, "html": body})


def send_reset_email(to_email: str, username: str, token: str, lang: str = 'es'):
    reset_url = f"{APP_URL}/auth/reset-password/{token}"
    if lang == 'en':
        subject = "Reset your Trastevere password"
        body = f"""
        <div style="font-family:sans-serif;max-width:500px;margin:0 auto;padding:32px 24px;background:#fdf6ee;border-radius:16px;">
            <h1 style="font-family:Georgia,serif;color:#ff6347;font-size:2rem;margin-bottom:8px;">Trastevere 🍅</h1>
            <h2 style="color:#222;font-size:1.2rem;margin-bottom:16px;">Hi, {username}</h2>
            <p style="color:#555;line-height:1.6;">
                We received a request to reset your password.<br>
                This link expires in <strong>1 hour</strong>.
            </p>
            <a href="{reset_url}" style="display:inline-block;margin-top:24px;padding:12px 28px;
               background:#ff6347;color:white;border-radius:10px;text-decoration:none;font-weight:700;">
                Reset password →
            </a>
            <p style="color:#aaa;font-size:0.8rem;margin-top:32px;">
                If you didn't request this, ignore this email. Your password won't change.<br>
                © Trastevere Team
            </p>
        </div>"""
    else:
        subject = "Recupera tu contraseña de Trastevere"
        body = f"""
        <div style="font-family:sans-serif;max-width:500px;margin:0 auto;padding:32px 24px;background:#fdf6ee;border-radius:16px;">
            <h1 style="font-family:Georgia,serif;color:#ff6347;font-size:2rem;margin-bottom:8px;">Trastevere 🍅</h1>
            <h2 style="color:#222;font-size:1.2rem;margin-bottom:16px;">Hola, {username}</h2>
            <p style="color:#555;line-height:1.6;">
                Recibimos una solicitud para restablecer tu contraseña.<br>
                Este enlace expira en <strong>1 hora</strong>.
            </p>
            <a href="{reset_url}" style="display:inline-block;margin-top:24px;padding:12px 28px;
               background:#ff6347;color:white;border-radius:10px;text-decoration:none;font-weight:700;">
                Restablecer contraseña →
            </a>
            <p style="color:#aaa;font-size:0.8rem;margin-top:32px;">
                Si no solicitaste esto, ignora este email. Tu contraseña no cambiará.<br>
                © Trastevere Team
            </p>
        </div>"""
    _send({"from": FROM_EMAIL, "to": [to_email], "subject": subject, "html": body})


def send_delete_email(to_email: str, username: str, token: str, lang: str = 'es'):
    delete_url = f"{APP_URL}/auth/confirm-delete/{token}"
    if lang == 'en':
        subject = "Confirm your Trastevere account deletion"
        body = f"""
        <div style="font-family:sans-serif;max-width:500px;margin:0 auto;padding:32px 24px;background:#fdf6ee;border-radius:16px;">
            <h1 style="font-family:Georgia,serif;color:#ff6347;font-size:2rem;margin-bottom:8px;">Trastevere 🍅</h1>
            <h2 style="color:#222;font-size:1.2rem;margin-bottom:16px;">Hi, {username}</h2>
            <p style="color:#555;line-height:1.6;">
                We received a request to <strong>delete your account</strong>.<br>
                This action is <strong>irreversible</strong> — all your recipes and data will be deleted.<br>
                The link expires in <strong>1 hour</strong>.
            </p>
            <a href="{delete_url}" style="display:inline-block;margin-top:24px;padding:12px 28px;
               background:#e05252;color:white;border-radius:10px;text-decoration:none;font-weight:700;">
                Yes, delete my account →
            </a>
            <p style="color:#aaa;font-size:0.8rem;margin-top:32px;">
                If you didn't request this, ignore this email. Your account is safe.<br>
                © Trastevere Team
            </p>
        </div>"""
    else:
        subject = "Confirma la eliminación de tu cuenta de Trastevere"
        body = f"""
        <div style="font-family:sans-serif;max-width:500px;margin:0 auto;padding:32px 24px;background:#fdf6ee;border-radius:16px;">
            <h1 style="font-family:Georgia,serif;color:#ff6347;font-size:2rem;margin-bottom:8px;">Trastevere 🍅</h1>
            <h2 style="color:#222;font-size:1.2rem;margin-bottom:16px;">Hola, {username}</h2>
            <p style="color:#555;line-height:1.6;">
                Recibimos una solicitud para <strong>eliminar tu cuenta</strong>.<br>
                Esta acción es <strong>irreversible</strong> — se borrarán todas tus recetas y datos.<br>
                El enlace expira en <strong>1 hora</strong>.
            </p>
            <a href="{delete_url}" style="display:inline-block;margin-top:24px;padding:12px 28px;
               background:#e05252;color:white;border-radius:10px;text-decoration:none;font-weight:700;">
                Sí, eliminar mi cuenta →
            </a>
            <p style="color:#aaa;font-size:0.8rem;margin-top:32px;">
                Si no solicitaste esto, ignora este email. Tu cuenta está segura.<br>
                © Trastevere Team
            </p>
        </div>"""
    _send({"from": FROM_EMAIL, "to": [to_email], "subject": subject, "html": body})