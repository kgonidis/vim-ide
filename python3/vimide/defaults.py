
LEFTBAR_DEFAULTS = {
    "layout": {
        "location": "vertical topleft",
        "vertical": True,
        "hidden": True,
        "autoclose": True,
        "size": 40
    },
    "plugins": {
        "nerdtree": {
            'open_command': 'NERDTree',
            'size': 50,
            'opens_by_default': 'current',
        }
    }

}

RIGHTBAR_DEFAULTS = {
    "layout": {
        "location": "vertical botright",
        "vertical": True,
        "hidden": True,
        "autoclose": True,
        "size": 40
    },
    "plugins": {
        "tagbar": {
            'open_command': 'execute "Tagbar" | wincmd j',
            'goto_command': 'TagbarOpen',
            'size': 50,
            'opens_by_default': 'belowright',
        }
    }

}

GITBAR_DEFAULTS = {
    "layout": {
        "location": "vertical botright",
        "vertical": True,
        "hidden": True,
        "autoclose": True,
        "autoload": False,
        "size": 40
    },
    "plugins": {
        "git": {
            'open_command': 'belowright G',
            'size': 50,
            'opens_by_default': 'belowright',
        }
    }
}

BOTBAR_DEFAULTS = {
    "layout": {
        "location": "botright",
        "vertical": False,
        "hidden": True,
        "autoclose": True,
        "size": 40
    },
    "plugins": {
        "terminal": {
            'open_command': 'terminal ++curwin',
            'size': 50,
            'opens_by_default': 'current'
        }
    }
}



LAYOUT_DEFAULTS = {
    "botbar": BOTBAR_DEFAULTS,
    "leftbar": LEFTBAR_DEFAULTS,
    "gitbar": GITBAR_DEFAULTS,
    "rightbar": RIGHTBAR_DEFAULTS,
}
