
function vimide#load()
py3 << EOF
_vim_ide = __import__('vimide', fromlist = ['ide']).ide.Ide()
_vim_ide.SetupUI()
EOF
call airline#extensions#tabline#buflist#invalidate()
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

function vimide#toggle(layout)
py3 << EOF
_vim_ide[vim.eval("a:layout")].Toggle()
EOF
endfunction

function vimide#delbuf(name)
py3 << EOF
_vim_ide.BufferClose(vim.eval("a:name"))
EOF
endfunction

function vimide#autoload()
    let g:vimide_autoload = 1
endfunction

