wechat_robot
├── config.py               # project configure file
├── controller              # controller, every controller is a packet
│   ├── action              # action controller
│   │   ├── __init__.py     # packet file
│   │   ├── urls.py         # url bind
│   │   └── views.py        # view logic
│   ├── index
│   │   ├── __init__.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── login
│   │   ├── __init__.py
│   │   ├── urls.py
│   │   └── views.py
│   └── user
│       ├── __init__.py
│       ├── urls.py
│       └── views.py
├── core                    # core module
│   ├── base_view.py        # view module
│   └── wechat_manager.py   # wechat module
├── itchat                  # itchat module
├── main.py                 # app entrance
├── message.dict            # auto reply information configure file
├── README.md
├── static                  # static resource file 
│   ├── fonts               # fonts directory
│   ├── head                # wechat login user all of the image directory
│   ├── image               # page image resource directory
│   ├── index               # index controller resource directory
│   ├── login               # login controller resource directory
│   ├── public              # public resource directory
│   ├── qr_image            # QR code image directory
│   ├── skin                # layer front end plugin's style skin directory
│   └── user                # user controller resource directory
└── template                # template file
    ├── index               # index controller template
    ├── login               # login controller template
    └── user                # user controller template
