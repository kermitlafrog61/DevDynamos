from sqladmin import ModelView

from .models import User, Profession, Certificate


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username]


class ProfessionAdmin(ModelView, model=Profession):
    column_list = [Profession.id, Profession.name]
    column_details_list = [Profession.id, Profession.name]



class CertificateAdmin(ModelView, model=Certificate):
    column_list = [Certificate.id, Certificate.name]
