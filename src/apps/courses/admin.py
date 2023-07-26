from sqladmin import ModelView

from .models import Course, Lection


class CourseAdmin(ModelView, model=Course):
    column_list = [Course.id, Course.name]


class LectionAdmin(ModelView, model=Lection):
    column_list = [Lection.id, Lection.name, Lection.course_id]
