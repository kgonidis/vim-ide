
function vimide#idequit()
    call vimide#delbuf("terminal")
    :qa
endfunction

nmap <Plug>VimideQuit :call vimide#idequit()

command! -bar -nargs=1 VimideShow call vimide#show(<f-args>)
command! -bar -nargs=1 VimideHide call vimide#hide(<f-args>)
command! -bar -nargs=1 VimideToggle call vimide#toggle(<f-args>)
command! -bar -nargs=1 VimideGoTo call vimide#goto(<f-args>)
command! -bar -nargs=1 VimideBufDel call vimide#delbuf(<f-args>)


