

function vimide#load()
    py3 << EOF
_vim_ide = __import__('vimide', fromlist = ['ide']).ide.Ide()
EOF
endfunction

