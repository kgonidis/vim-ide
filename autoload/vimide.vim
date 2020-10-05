
py3 << EOF
_vim_ide = __import__('vimide', fromlist = ['ide']).ide.Ide()
EOF
function vimide#load()
py3 << EOF
_vim_ide.SetupUI()
EOF
endfunction

function vimide#where()
py3 << EOF
_vim_ide.Where()
EOF
    return g:return
endfunction

function vimide#goto(name)
py3 << EOF
_vim_ide.GoToWindow(vim.eval("a:name"))
EOF
endfunction

function vimide#hide(layout)
py3 << EOF
_vim_ide[vim.eval("a:layout")].Hide()
EOF
endfunction

function vimide#show(layout)
py3 << EOF
_vim_ide[vim.eval("a:layout")].Show()
EOF
endfunction


