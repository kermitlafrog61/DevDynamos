from decouple import config as conf
from fastapi import FastAPI
from sqladmin import Admin

from apps.auth import router as auth_router
from apps.auth.admin import UserAdmin, ProfessionAdmin, CertificateAdmin
from core.admin import AdminAuth
from core.database import engine

app = FastAPI(
    title="DevDynamos",
    description="Project created for hackathos",
    version="1.0",
)

# Configuring admin panel
authentication_backend = AdminAuth(secret_key=conf("SECRET_KEY"))
admin = Admin(app=app, engine=engine,
              authentication_backend=authentication_backend)
admin.add_view(UserAdmin)
admin.add_view(ProfessionAdmin)
admin.add_view(CertificateAdmin)


# Including routers

app.include_router(auth_router.router, tags=["Auth"])
