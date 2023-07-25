from fastapi import FastAPI
from fastapi.exceptions import ResponseValidationError
from fastapi.responses import Response
from sqladmin import Admin

from apps.auth import router as auth_router
from apps.auth.admin import CertificateAdmin, ProfessionAdmin, UserAdmin
from apps.courses import router as courses_router
from core.admin import AdminAuth
from core.database import engine

from core.settings import settings


app = FastAPI(
    title="DevDynamos",
    description="Project created for hackathos",
    version="1.0",
)

# Configuring admin panel
authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)
admin = Admin(app=app, engine=engine,
              authentication_backend=authentication_backend)
admin.add_view(UserAdmin)
admin.add_view(ProfessionAdmin)
admin.add_view(CertificateAdmin)


# Including routers

app.include_router(auth_router.router, tags=["Auth"])
app.include_router(courses_router.router, tags=["Courses"])
