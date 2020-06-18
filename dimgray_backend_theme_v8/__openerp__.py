# -*- encoding: utf-8 -*-

{
    # Module information
    'name': 'Dimgray Backend Theme V8',
    'sequence': -4,
    'version': '2.0',
    'category': 'Themes/Backend',

    # Your information
    'author': 'RAZAFIMIANDRISOA Noarison Léonce',
    'website': 'kheluc@yahoo.com',
    'license': 'OPL-1',
    'summary': 'Dimgray Backend Theme V8',
    'images': [
        'images/screen.png'
    ],

    # Dependencies
    'depends': [
        'web',
    ],

    # Views templates, pages, menus, options and snippets
    'data': [
        'views/backend.xml',
    ],

    # Qweb templates
    'qweb': [
        'static/src/xml/backend.xml',
    ],

    # Technical options
    'installable': True,
    'auto_install': True,
}
