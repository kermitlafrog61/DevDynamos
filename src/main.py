from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin

from apps.auth import router as auth_router
from apps.auth.admin import CertificateAdmin, ProfessionAdmin, UserAdmin
from apps.courses import router as courses_router
from apps.courses.admin import CourseAdmin, LectionAdmin
from core.admin import AdminAuth
from core.database import engine
from core.settings import settings

app = FastAPI(
    title="DevDynamos",
    description="Project created for hackathos",
    version="1.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuring admin panel
authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)
admin = Admin(app=app, engine=engine,
              authentication_backend=authentication_backend)
admin.add_view(UserAdmin)
admin.add_view(ProfessionAdmin)
admin.add_view(CertificateAdmin)
admin.add_view(CourseAdmin)
admin.add_view(LectionAdmin)


# Including routers

app.include_router(auth_router.router, tags=["Auth"])
app.include_router(courses_router.router, tags=["Courses"])
