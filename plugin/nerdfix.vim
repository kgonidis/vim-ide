
if !exists(":NERDTree")
    autocmd VimEnter * execute "function! g:NERDTreeCreator._createTreeWin() \<C-j>
                \let l:splitLocation = g:NERDTreeWinPos ==# 'left' ? 'topleft ' : 'botright ' \<C-j>
                \let l:splitSize = g:NERDTreeWinSize \<C-j>
                \if !g:NERDTree.ExistsForTab() \<C-j>
                \    let t:NERDTreeBufName = self._nextBufferName() \<C-j>
                \    if g:NERDTreeCurwin == 1 \<C-j>
                \        silent! execute 'edit ' . t:NERDTreeBufName \<C-j>
                \    else \<C-j>
                \        silent! execute l:splitLocation . 'vertical ' . l:splitSize . ' new' \<C-j>
                \        silent! execute 'edit ' . t:NERDTreeBufName \<C-j>
                \        silent! execute 'vertical resize '. l:splitSize \<C-j>
                \    endif \<C-j>
                \    else \<C-j>
                \        if g:NERDTreeCurwin == 1 \<C-j>
                \            silent! execute 'edit ' . t:NERDTreeBufName \<C-j>
                \        else \<C-j>
                \            silent! execute l:splitLocation . 'vertical ' . l:splitSize . ' split' \<C-j>
                \            silent! execute 'buffer ' . t:NERDTreeBufName \<C-j>
                \        endif \<C-j>
                \    endif \<C-j>
                \
                \setlocal winfixwidth \<C-j>
                \call self._setCommonBufOptions() \<C-j>
                \if has('patch-7.4.1925') \<C-j>
                \    clearjumps \<C-j>
                \endif \<C-j>
                \endfunction\<CR>"
else
    execute "function! g:NERDTreeCreator._createTreeWin() \<C-j>
                \let l:splitLocation = g:NERDTreeWinPos ==# 'left' ? 'topleft ' : 'botright ' \<C-j>
                \let l:splitSize = g:NERDTreeWinSize \<C-j>
                \if !g:NERDTree.ExistsForTab() \<C-j>
                \    let t:NERDTreeBufName = self._nextBufferName() \<C-j>
                \    if g:NERDTreeCurwin == 1 \<C-j>
                \        silent! execute 'edit ' . t:NERDTreeBufName \<C-j>
                \    else \<C-j>
                \        silent! execute l:splitLocation . 'vertical ' . l:splitSize . ' new' \<C-j>
                \        silent! execute 'edit ' . t:NERDTreeBufName \<C-j>
                \        silent! execute 'vertical resize '. l:splitSize \<C-j>
                \    endif \<C-j>
                \    else \<C-j>
                \        if g:NERDTreeCurwin == 1 \<C-j>
                \            silent! execute 'edit ' . t:NERDTreeBufName \<C-j>
                \        else \<C-j>
                \            silent! execute l:splitLocation . 'vertical ' . l:splitSize . ' split' \<C-j>
                \            silent! execute 'buffer ' . t:NERDTreeBufName \<C-j>
                \        endif \<C-j>
                \    endif \<C-j>
                \
                \setlocal winfixwidth \<C-j>
                \call self._setCommonBufOptions() \<C-j>
                \if has('patch-7.4.1925') \<C-j>
                \    clearjumps \<C-j>
                \endif \<C-j>
                \endfunction\<CR>"
endif

let g:NERDTreeCurwin = 1
