from sqladmin import ModelView
from .models import Library

class LibraryAdmin(ModelView, model=Library):
    column_list = [Library.id]