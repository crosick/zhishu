.. _design:

***************
应用架构说明
***************



后端：

+ flask
插件：

+ flask-login
+ flask-sqlalchemy
+ flask-pagedown-mathjax
+ flask-moment
+ flask-wtf
+ flask-whooshalchemy
+ ...

前端：

+ bootstrap
插件：

+ bootstrap-tagsinput
+ mathjax



***************
目录文件结构与说明
***************

.. _file-structure:

目录结构（隐藏部分细节）
=============================
::


    ├── ENV             - python环境
    ├── app             - 应用文件夹
    │   ├── auth        - 管用户注册登录的app
    │   ├── main        - 主app
    │   ├── static      - 放静态文件,css,js,image
    │   ├── templates   - 放jinja2模板
    │   │   └── auth
    │   └── models.py   - 数据库模型    
    ├── doc             - sphinx文档文件夹
    ├── migrations      - 做数据库版本控制的
    │   └── versions
    ├── requirements    - 运行需要的python包
    ├── search.db       - whoosh那个搜索库需要的数据库文件
    │   ├── Post
    │   ├── Question
    │   └── Tag
    ├── config.py       - 配置文件
    └── tests           - 测试都放这里


.. _file-description:

部分文件说明
=============================
::

    views.py            - 控制路由，处理主要逻辑的文件
    forms.py            - 表单类文件


***************
数据库模型说明
***************

.. _model:

ORM 概念
=============================

对象关系映射（英语：Object Relational Mapping，简称ORM，或O/RM，或O/R mapping），是一种程序设计技术，用于实现面向对象编程语言里不同类型系统的数据之间的转换。从效果上说，它其实是创建了一个可在编程语言里使用的“虚拟对象数据库”。

这里使用sqlalchemy 作为 Object Relational 映射器。


数据模型可视化
=============================

由 sadisplay 生成，变量函数名足够解释自身的功能。。。。

.. image:: _static/schema   .png


***************
视图函数注解
***************

main视图函数
=============================
.. automodule:: app.main.views
    :members:
    :undoc-members:

auth视图函数
=============================
.. automodule:: app.auth.views
    :members:
    :undoc-members:


    

