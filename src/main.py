from fastapi import FastAPI
from sqladmin import Admin

from apps.auth import router as auth_router
from apps.auth.admin import CertificateAdmin, ProfessionAdmin, UserAdmin
from apps.courses import router as courses_router
<<<<<<< HEAD
from apps.courses.admin import CourseAdmin, LectionAdmin
from apps.library import router as library_router
from apps.library.admin import LibraryAdmin
=======
from apps.profile import router as profile_router
>>>>>>> b0194f4 (fixing)
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
admin.add_view(CourseAdmin)
admin.add_view(LectionAdmin)
admin.add_view(LibraryAdmin)

# Including routers

app.include_router(auth_router.router, tags=["Auth"])
app.include_router(courses_router.router, tags=["Courses"])
<<<<<<< HEAD
app.include_router(library_router.router, tags=["Library"])
=======
app.include_router(profile_router.router, tags=["Profile"])
>>>>>>> b0194f4 (fixing)
