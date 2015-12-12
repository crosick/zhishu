.. _design:


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



