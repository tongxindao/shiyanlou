from flask import render_template, flash

from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import AppBuilder, expose, has_access, BaseView, ModelView, MultipleView, MasterDetailView, SimpleFormView
from flask_appbuilder.fieldwidgets import BS3TextFieldWidget
from flask_appbuilder.forms import DynamicForm
from flask_appbuilder.widgets import ListThumbnail
from flask_appbuilder.actions import action
from flask_appbuilder.charts.views import DirectByChartView
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from flask_babel import lazy_gettext as _

from wtforms import Form, StringField
from wtforms.validators import DataRequired

from app import appbuilder, db

from .models import College, Department, Major, MClass, Teacher, Student, ContactGroup, Contact

"""
    Create your Views::


    class MyModelView(ModelView):
        datamodel = SQLAInterface(MyModel)


    Next, register your Views::


    appbuilder.add_view(MyModelView, "My View", icon="fa-folder-open-o", category="My Category", category_icon='fa-envelope')
"""

"""
    Application wide 404 error handler
"""
@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', base_template=appbuilder.base_template, appbuilder=appbuilder), 404

db.create_all()

class MyView(BaseView):
    default_view = 'hello'

    @expose('/hello/')
    @has_access
    def hello(self):
        return 'Hello World!'

    @expose('/message/<string:msg>')
    @has_access
    def message(self, msg):
        msg = 'Hello %s' % (msg)
        return msg
 
    @expose('/welcome/<string:msg>')
    @has_access
    def welcome(self, msg):
        msg = 'Hello %s' % (msg)
        return self.render_template('index.html', msg=msg)

appbuilder.add_view(MyView, "Hello", category='My View')
appbuilder.add_link("Message", href='/myview/message/join', category='My View')
appbuilder.add_link("Welcome", href='/myview/welcome/student', category='My View')

class ContactModelView(ModelView):
    datamodel = SQLAInterface(Contact)

    label_columns = {'contact_group': 'Contacts Group'}
    list_columns = ['name', 'personal_cellphone', 'birthday', 'contact_group']
    show_fieldsets = [
        (
            'Summary',
            {'fields': ['name', 'address', 'contact_group']}
        ),
        (
            'Personal Info',
            {'fields': ['birthday', 'personal_phone', 'personal_cellphone'],
                'expanded': False}
        ),
    ]

# 在联系人组视图中，我们使用related_views来关联联系人视图，F.A.B.将自动处理他们之间的关系。
class GroupModelView(ModelView):
    datamodel = SQLAInterface(ContactGroup)
    related_views = [ContactModelView]

# 现在我们就差最后一步工作就要完成本次实验了。
# 首先使用db.create_all()根据数据库模型创建表，然后再将视图添加到菜单。
db.create_all()
appbuilder.add_view(GroupModelView,
                    "List Groups",
                    icon = "fa-address-book-o",
                    category = "Contacts",
                    category_icon = "fa-envelope")
appbuilder.add_view(ContactModelView,
                    "List Contacts",
                    icon = "fa-address-card-o",
                    category = "Contacts")

# 这里定义了学院、部门、专业、班级、教师和学生的相关视图。
# 代码比较简单，直接关联我们定义好的模型就可以了，代码如下：
class CollegeView(ModelView):
    datamodel = SQLAInterface(College)

class DepartmentView(ModelView):
    datamodel = SQLAInterface(Department)

class MajorView(ModelView):
    datamodel = SQLAInterface(Major)

class MClassView(ModelView):
    datamodel = SQLAInterface(MClass)

class TeacherView(ModelView):
    datamodel = SQLAInterface(Teacher)

class StudentView(ModelView):
    datamodel = SQLAInterface(Student)

db.create_all()

# 这里将6个视图作为子菜单添加到了`School Manage`菜单中：
appbuilder.add_view(CollegeView, "College", icon="gear", category='School Manage',)
appbuilder.add_view(DepartmentView, "Department", icon="gear",category='School Manage')
appbuilder.add_view(MajorView, "Major", icon="gear", category='School Manage')
appbuilder.add_view(MClassView, "MClass", icon="gear", category='School Manage')
appbuilder.add_view(TeacherView, "Teacher", icon="gear",category='School Manage')
appbuilder.add_view(StudentView, "Student", icon="gear",category='School Manage')
