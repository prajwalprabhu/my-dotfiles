" Specify a directory for plugins
call plug#begin('~/.vim/plugged')

Plug 'neoclide/coc.nvim', {'branch': 'release'}
Plug 'scrooloose/nerdtree'
"Plug 'tsony-tsonev/nerdtree-git-plugin'
Plug 'Xuyuanp/nerdtree-git-plugin'
Plug 'tiagofumo/vim-nerdtree-syntax-highlight'
Plug 'ryanoasis/vim-devicons'
Plug 'airblade/vim-gitgutter'
Plug 'ctrlpvim/ctrlp.vim' " fuzzy find files
Plug 'scrooloose/nerdcommenter'
"Plug 'prettier/vim-prettier', { 'do': 'yarn install' }
"Plug 'fatih/vim-go'
Plug 'christoomey/vim-tmux-navigator'

Plug 'morhetz/gruvbox'

Plug 'HerringtonDarkholme/yats.vim' " TS Syntax

" Initialize plugin system
call plug#end()

inoremap jk <ESC>
nmap <C-n> :NERDTreeToggle<CR>
vmap ++ <plug>NERDCommenterToggle
nmap ++ <plug>NERDCommenterToggle

" open NERDTree automatically
"autocmd StdinReadPre * let s:std_in=1
"autocmd VimEnter * NERDTree

let g:NERDTreeGitStatusWithFlags = 1
"let g:WebDevIconsUnicodeDecorateFolderNodes = 1
"let g:NERDTreeGitStatusNodeColorization = 1
"let g:NERDTreeColorMapCustom = {
    "\ "Staged"    : "#0ee375",  
    "\ "Modified"  : "#d9bf91",  
    "\ "Renamed"   : "#51C9FC",  
    "\ "Untracked" : "#FCE77C",  
    "\ "Unmerged"  : "#FC51E6",  
    "\ "Dirty"     : "#FFBD61",  
    "\ "Clean"     : "#87939A",   
    "\ "Ignored"   : "#808080"   
    "\ }                         


let g:NERDTreeIgnore = ['^node_modules$']

" vim-prettier
"let g:prettier#quickfix_enabled = 0
"let g:prettier#quickfix_auto_focus = 0
" prettier command for coc
command! -nargs=0 Prettier :CocCommand prettier.formatFile
" run prettier on save
"let g:prettier#autoformat = 0
"autocmd BufWritePre *.js,*.jsx,*.mjs,*.ts,*.tsx,*.css,*.less,*.scss,*.json,*.graphql,*.md,*.vue,*.yaml,*.html PrettierAsync


" ctrlp
let g:ctrlp_user_command = ['.git/', 'git --git-dir=%s/.git ls-files -oc --exclude-standard']

" j/k will move virtual lines (lines that wrap)
noremap <silent> <expr> j (v:count == 0 ? 'gj' : 'j')
noremap <silent> <expr> k (v:count == 0 ? 'gk' : 'k')

set relativenumber

set smarttab
set cindent
set tabstop=2
set shiftwidth=2
" always uses spaces instead of tab characters
set expandtab

colorscheme gruvbox

" sync open file with NERDTree
" " Check if NERDTree is open or active
function! IsNERDTreeOpen()        
  return exists("t:NERDTreeBufName") && (bufwinnr(t:NERDTreeBufName) != -1)
endfunction

" Call NERDTreeFind iff NERDTree is active, current window contains a modifiable
" file, and we're not in vimdiff
function! SyncTree()
  if &modifiable && IsNERDTreeOpen() && strlen(expand('%')) > 0 && !&diff
    NERDTreeFind
    wincmd p
  endif
endfunction

" Highlight currently open buffer in NERDTree
autocmd BufEnter * call SyncTree()

" coc config
let g:coc_global_extensions = [
  \ 'coc-snippets',
  \ 'coc-pairs',
  "\ 'coc-tsserver',
  "\ 'coc-eslint', 
  "\ 'coc-prettier', 
  \ 'coc-json',
  \ 'coc-go' 
  \ ]
" from readme
" if hidden is not set, TextEdit might fail.
set hidden " Some servers have issues with backup files, see #649 set nobackup set nowritebackup " Better display for messages set cmdheight=2 " You will have bad experience for diagnostic messages when it's default 4000.
set updatetime=300

" don't give |ins-completion-menu| messages.
set shortmess+=c

" always show signcolumns
set signcolumn=yes

" Use tab for trigger completion with characters ahead and navigate.
" Use command ':verbose imap <tab>' to make sure tab is not mapped by other plugin.
inoremap <silent><expr> <TAB>
      \ pumvisible() ? "\<C-n>" :
      \ <SID>check_back_space() ? "\<TAB>" :
      \ coc#refresh()
inoremap <expr><S-TAB> pumvisible() ? "\<C-p>" : "\<C-h>"

function! s:check_back_space() abort
  let col = col('.') - 1
  return !col || getline('.')[col - 1]  =~# '\s'
endfunction

" Use <c-space> to trigger completion.
inoremap <silent><expr> <c-space> coc#refresh()

" Use <cr> to confirm completion, `<C-g>u` means break undo chain at current position.
" Coc only does snippet and additional edit on confirm.
inoremap <expr> <cr> pumvisible() ? "\<C-y>" : "\<C-g>u\<CR>"
" Or use `complete_info` if your vim support it, like:
" inoremap <expr> <cr> complete_info()["selected"] != "-1" ? "\<C-y>" : "\<C-g>u\<CR>"

" Use `[g` and `]g` to navigate diagnostics
nmap <silent> [g <Plug>(coc-diagnostic-prev)
nmap <silent> ]g <Plug>(coc-diagnostic-next)

" Remap keys for gotos
nmap <silent> gd <Plug>(coc-definition)
nmap <silent> gy <Plug>(coc-type-definition)
nmap <silent> gi <Plug>(coc-implementation)
nmap <silent> gr <Plug>(coc-references)

" Use K to show documentation in preview window
nnoremap <silent> K :call <SID>show_documentation()<CR>

function! s:show_documentation()
  if (index(['vim','help'], &filetype) >= 0)
    execute 'h '.expand('<cword>')
  else
    call CocAction('doHover')
  endif
endfunction

" Highlight symbol under cursor on CursorHold
autocmd CursorHold * silent call CocActionAsync('highlight')

" Remap for rename current word
nmap <F2> <Plug>(coc-rename)

" Remap for format selected region
xmap <leader>f  <Plug>(coc-format-selected)
nmap <leader>f  <Plug>(coc-format-selected)

augroup mygroup
  autocmd!
  " Setup formatexpr specified filetype(s).
  autocmd FileType typescript,json setl formatexpr=CocAction('formatSelected')
  " Update signature help on jump placeholder
  autocmd User CocJumpPlaceholder call CocActionAsync('showSignatureHelp')
augroup end

" Remap for do codeAction of selected region, ex: `<leader>aap` for current paragraph
xmap <leader>a  <Plug>(coc-codeaction-selected)
nmap <leader>a  <Plug>(coc-codeaction-selected)

" Remap for do codeAction of current line
nmap <leader>ac  <Plug>(coc-codeaction)
" Fix autofix problem of current line
nmap <leader>qf  <Plug>(coc-fix-current)

" Create mappings for function text object, requires document symbols feature of languageserver.
xmap if <Plug>(coc-funcobj-i)
xmap af <Plug>(coc-funcobj-a)
omap if <Plug>(coc-funcobj-i)
omap af <Plug>(coc-funcobj-a)

" Use <C-d> for select selections ranges, needs server support, like: coc-tsserver, coc-python
nmap <silent> <C-d> <Plug>(coc-range-select)
xmap <silent> <C-d> <Plug>(coc-range-select)

" Use `:Format` to format current buffer
command! -nargs=0 Format :call CocAction('format')

" Use `:Fold` to fold current buffer
command! -nargs=? Fold :call     CocAction('fold', <f-args>)

" use `:OR` for organize import of current buffer
command! -nargs=0 OR   :call     CocAction('runCommand', 'editor.action.organizeImport')

" Add status line support, for integration with other plugin, checkout `:h coc-status`
set statusline^=%{coc#status()}%{get(b:,'coc_current_function','')}

" Using CocList
" Show all diagnostics
nnoremap <silent> <space>a  :<C-u>CocList diagnostics<cr>
" Manage extensions
nnoremap <silent> <space>e  :<C-u>CocList extensions<cr>
" Show commands
nnoremap <silent> <space>c  :<C-u>CocList commands<cr>
" Find symbol of current document
nnoremap <silent> <space>o  :<C-u>CocList outline<cr>
" Search workspace symbols
nnoremap <silent> <space>s  :<C-u>CocList -I symbols<cr>
" Do default action for next item.
nnoremap <silent> <space>j  :<C-u>CocNext<CR>
" Do default action for previous item.
nnoremap <silent> <space>k  :<C-u>CocPrev<CR>
" Resume latest coc list
nnoremap <silent> <space>p  :<C-u>CocListResume<CR>


" Gopi's _gvimrc file https://github.com/GopinathMR
" This file has been modified to make it work on both Windows and Linux
" Github gist location : https://gist.github.com/1100054
" If you find any issues or add any enhancements, please submit revised version as gist
"----------------------------------------------------------------------------------------------------------

" 1. OS specific

    if ($OS == 'Windows_NT')
        " Windows specific settings

        let $MY_DIR=$VIM " Setup where current user can write some data in Vim

        let $MY_VIM="$VIM/xtra-vim-scripts" "Where custom downloaded Vim scripts are available
        set viminfo='10,\"100,:20,%,n$MY_DIR/.viminfo

        " 1.1 executing OS command within Vim
        set shell=c:\Windows\system32\cmd.exe
        " shell command flag
        set shellcmdflag=/c

        " 1.2 set font
        " Use courier-new font
        set guifont=Consolas:h10
        " set guifont=Courier_New:h11
        " set guifont=Terminal:h6
        " set guifont=Courier:h10
    else
        " Unix specific settings
        let $MY_DIR=$HOME " Setup where current user can write some data in Vim
        let $MY_VIM="$HOME/xtra-vim-scripts" "Where custom downloaded Vim scripts are available
        " 1.1 executing OS command within Vim
        set shell=/bin/bash

        " 1.2 set font
        set guifont=Monospace\ 8
    endif
    " 1.3 Restore cursor to file position in previous editing session http://vim.wikia.com/wiki/VimTip80
    set viminfo='10,\"100,:20,%,n$MY_DIR/.viminfo

"----------------------------------------------------------------------------------------------------------

" 2. File compatibility and configuration issues
    " Do not keep a backup or .swp file. I don't like to have junk files, my source is anyway in cvs/svn/p4/git.
    set nobackup
    set nowritebackup
    set noswapfile
    set nocompatible " Use Vim defaults (much better!), Vi is for 70's programmers!
    set viminfo='20,\"50 " read/write a .viminfo file, don't store more than 50 lines of registers - http://vim.wikia.com/wiki/Restore_cursor_to_file_position_in_previous_editing_session
    set ts=4 " tabstop - how many columns should the cursor move for one tab
    set sw=4 " shiftwidth - how many columns should the text be indented
    set expandtab " always expands tab to spaces. It is good when peers use different editor.
    set wrap " wraps longs lines to screen size

"----------------------------------------------------------------------------------------------------------

" 3. Color, Look&Feel Configuration

    " set colorscheme to midnight. Use the command :colorscheme <schemeName> for setting other color schemes
    " colorscheme darkbone
    colorscheme darkblue
    " Use different color schemes for different set of files.
    " au BufEnter *.* colorscheme zellner
    au BufEnter *.log colorscheme desert
    au BufEnter *.build colorscheme darkbone
    "au BufEnter *.txt colorscheme darkbone
    au BufEnter *.gradle colorscheme peachpuff
    au BufNewFile,BufRead *.gradle setf groovy
    au BufNewFile,BufRead *.json set ft=javascript

    " Customize Status line color of current window & non-current windows
    highlight StatusLineNC guifg=SlateBlue guibg=Yellow
    highlight StatusLine guifg=Gray guibg=White

    set vb t_vb= " stop beeping or flashing the screen

"----------------------------------------------------------------------------------------------------------

" 4. Display specific (screen resolution dependent settings. Adjust these if your screen resolution will be too less or you have bigger monitor)
    if ($OS == 'Windows_NT')
        win 260 92 " The window height
    else
        win 200 40 " The window height
    endif
    set laststatus=2 " Show the status line even if only one file is being edited
    set ruler " Show ruler
    set go-=T " Following line removes the toolbar, As I usually dont need it.  Gives me extra lines for editor. If you have big monitor and you think you need toolbar, comment this line.
    " Make command line two lines high
    set ch=2

"----------------------------------------------------------------------------------------------------------

" 5. Working with split windows and tabs
    " 5.1 Working with tabs
    "~~~~~~~~~~~~~~~~~~~~~~~
    if version >= 700
        " always enable Vim tabs
        set showtabline=2
        " set tab features just like browser
        " open tab, close tab, next tab, previous tab (just like Chrome and Firefox keyboard shortcuts)
      map <C-t> <Esc>:tabnew<CR>
      map <C-F4> <Esc>:tabclose<CR>
      map <C-Tab> <Esc>:tabnext<CR>
      map <C-S-Tab> <Esc>:tabprev<CR>
    endif

    " 5.2 Working with windows 
    "~~~~~~~~~~~~~~~~~~~~~~~
    " Switch between splits very fast (for multi-file editing) by maximizing target split - http://vim.wikia.com/wiki/VimTip173
    map <C-J> <C-W>j<C-W>_
    map <C-K> <C-W>k<C-W>_
    map <C-H> <C-W>h<C-W>|
    map <C-L> <C-W>l<C-W>|
    map <C-=> <C-W>=

"----------------------------------------------------------------------------------------------------------

" 6. General file editing
    " 6.1 Common Settings to enable better editing
    "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        set bs=2 " allow backspacing over everything in insert mode
        set ai " always set autoindenting on

        set showmatch " show matching brackets
        syntax on " Switch on syntax highlighting.
        set hidden " This option allows you to switch between multiple buffers without saving a changed buffer
        set hlsearch " Switch on search pattern highlighting.
        set mousehide " Hide the mouse pointer while typing.

        
        " Easy pasting to windows apps - http://vim.wikia.com/wiki/VimTip21
        " yank always copies to unnamed register, so it is available in windows clipboard for other applications.
        set clipboard=unnamed

        "Set the history size to maximum. by default it is 20 - http://vim.wikia.com/wiki/VimTip45
        set history=80

        "Plugins config - http://vim.sourceforge.net/script.php?script_id=448
        :filetype plugin on 
        
        " Always change the directory to working directory of file in current buffer - http://vim.wikia.com/wiki/VimTip64
        autocmd BufEnter * call CHANGE_CURR_DIR()

        " See Help documentation by entering command :help 'sessionoptions'
        set sessionoptions+=resize
        set sessionoptions+=winpos
        set sessionoptions+=folds
        set sessionoptions+=tabpages

        set hlsearch " highlights the previously searched string
        set incsearch " higlight search string as search pattern is entered
        :hi Search ctermfg=red ctermbg=gray
        set suffixes+=.class,.exe,.obj,.dat,.dll " Show these file types at the end while using :edit command

        " Configuration for explorer.vim to open the new file by doing vertical split and opening it in right window.
        " For more info use command :help file-explorer
        let g:explVertical=1    " Split vertically
        let g:explSplitRight=1  " Put new window right of the explorer window
        let c_comment_strings=1 " I like highlighting strings inside C comments

        " Buffer Explorer - http://vim.sourceforge.net/scripts/script.php?script_id=159
        let g:miniBufExplMapWindowNavVim = 1 
        let g:miniBufExplMapWindowNavArrows = 1 
        let g:miniBufExplMapCTabSwitchBuffs = 1

        " On Opening Vim, restore previous session - http://vim.runpaint.org/editing/managing-sessions/
        " I'm setting up a global session file. If you need project specific one, invoke below functions within Vim to save & restore.
        autocmd VimLeavePre * call SaveSession("$MY_DIR/.session.vim")
        "autocmd VimEnter * call RestoreSession("$MY_DIR/.session.vim")

    " 6.2 Common shortcuts
    "~~~~~~~~~~~~~~~~~~~~~~~

        " Don't use Ex mode, use Q for formatting
        map Q gq

        " save the current file
        map <F2> :w!<CR>
        map <C-S> :w<CR>

        " go to next file in the open file list.
        map <F3> :n<CR>
        
        " go to previous file in the open file list.
        map <S-F3> :previous<CR>

        " Show the list of all functions in current file - http://vim.wikia.com/wiki/VimTip79
        nmap <F4> :call ShowFunc()<CR>

        " Reload the current file
        map <F5> :e!<CR>
        map <M-r> :e!<CR>

        " split the current file (horizontal split)
        map <F6> :split<CR>

        " Shift F6 will do vertical split
        map <S-F6> : vsplit<CR>

        " to execute Ant build tool.
        map <F7> :!ant<CR>

        " delete buffer
        map <F8> :bdelete<CR>

        " Shift F8 will delete buffer without saving
        map <S-F8> : bdelete!<CR>

        " Quit without saving
        map <C-Q> :q!<CR>

        " Quit after saving
        map <C-X> :x<CR>

        " show current word under cursor match lines in the file 
        " map <F8> :g/<C-R><C-W>/#<CR>

        " Comment-ify the visually selected block using C style comments
        vmap \/* omxomy<ESC>`xO/*<ESC>`yo*/<ESC>

        "Copy current filename with path to clipboard
        map     <F8> :let @* = expand('%:p')<cr>
        map!    <F8> <Esc>:let @* = expand('%:p')<cr>

        " WOK: CTRL-SPACE: keyword completion, Just like Eclipse :)
        map  <C-space> <C-n>
        map! <C-space> <C-n>
        map  <C-S-space> <C-p>
        map! <C-S-space> <C-p>

        " Folding shortcuts
        map - v%zf
        map = v%zd

        " Select All
        map <C-a> ggVG

    " 6.3 Setup for quick jump to sections of file
    "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        " Tag settings - http://vim.wikia.com/wiki/VimTip94
        " Vim will search for the file named 'tags', starting with the current directory and then going to the parent directory and then 
        " recursively to the directory one level above, till it either locates the 'tags' file or reaches the root '/' directory. 
        set tags=tags;/
        set tagstack

        " For "gf" to open a file  where complete path is available in current file. (useful in C/C++ programming to open *.h files).
        " "**" matches a subtree, up to 100 directories deep.  Example:
        ":set path=/home/user_x/src/**
        " means search in the whole subtree under "/home/usr_x/src".
        :set path=.,./**

        " To jump between the '=' and ';' in an assignment using <S-%>. Useful for languages like C/C++ and Java.
        :au FileType c,cpp,java set mps+==:;
        " Including '<' and '>' (HTML): >
        :set mps+=<:>

        " Bookmark feature in Vim - http://vim.wikia.com/wiki/VimTip42
        " To save all book marks in 100 files.It will save local marks (a-z) by default. The '100 tells Vim to save marks and other information for up to 100 files. The f1 directive tells Vim to also save global marks (A-Z) when it exits. If you don't want Vim to do this, set it to f0 instead.
        " :marks give all marks
        " ma  - book mark "a"
        " `a  - go to bookmark "a"
        set viminfo='100,f1

"----------------------------------------------------------------------------------------------------------

" 7. Programming language specific 

" 7.1 Generic Programming Language setup
  "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    augroup prog
    au!
        " When starting to edit a file:
        " For *.c, *.cpp, *.java and *.h files set formatting of comments and set C-indenting on.
        " For other files switch it off.
        " Don't change the order, it's important that the line with * comes first.
        autocmd BufNewFile,BufRead,BufReadPost *       set formatoptions=tcql nocindent comments&
        autocmd BufNewFile,BufRead,BufReadPost *.c,*.h,*.cpp,*.java set formatoptions=croql cindent comments=sr:/*,mb:*,el:*/,://
        autocmd BufNewFile,BufRead *.fun,*.pks,*.pkb,*.sql,*.pls,*.plsql    setf plsql
    augroup END
" 7.2 Java shortcuts
  "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    augroup jprog
    au!
        abbr Sysl/ System.out.println(
        abbr Sys/ System.out.print(
        abbr Syse/ System.exit(1);
        abbr mark/ //TODO: Shambu
        abbr todo/ //TODO: Gopi<NL><BS>
        abbr op out.println("
        abbr main/ public static void main(String[] args) throws Exception {<NL><BS>
        abbr dbg/ Debug\.println(2,"");<NL><BS>
        abbr trace/ catch (Exception e) {<NL><Tab>e.printStackTrace();<NL><BS><BS><BS><BS>}<NL><BS>
        abbr impx/ import org.xml.sax.*;<NL>import org.xml.sax.helpers.*;<NL><BS>
        abbr msgbox/ MessageBox.Show("text", "caption", MessageBoxButtons.OK, MessageBoxIcon.Error);

        " When starting to .java a file, set formatting of comments and set C-indenting on.
        " For other files switch it off.
        " Don't change the order, it's important that the line with * comes first.
        autocmd BufRead *       set formatoptions=tcql nocindent comments&
        autocmd BufRead *.java, set formatoptions=croql cindent comments=sr:/*,mb:*,el:*/,://
    augroup END

" 7.3 C/C++ shortcuts
  "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  " Note : to work on C/C++ Windows, download windows version of cscope from http://iamphet.nm.ru/cscope/index.html
  
  " (logging macros)
    augroup cprog
    au!
        abbr log0/ LOG_ENTER(L"");
        abbr log1/ LOG_EXIT(L"");
        abbr logi/ LOG_INFO(L"");
        "cs add s:\btbuild\scripts\cscope.out
        let g:buildFile = 'default.build' 
        let g:antOption = '-verbose' 
    augroup END

" 7.4 HTML shortcuts
  "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    augroup html
        " bold
        vmap \b y:s/\<<c-r>"\>/<b>&<\/b>/g<CR>
        " bold - global
        vmap \B y:%s/\<<c-r>"\>/<b>&<\/b>/g<CR>
        " italics
        vmap \i y:s/\<<c-r>"\>/<i>&<\/i>/g<CR>
        " italics - global
        vmap \I y:%s/\<<c-r>"\>/<i>&<\/i>/g<CR>
        " fixed width font
        vmap \tt y:s/\<<c-r>"\>/<tt>&<\/tt>/g<CR>
        " fixed width font - global
        vmap \TT y:%s/\<<c-r>"\>/<tt>&<\/tt>/g<CR>
    augroup END

"----------------------------------------------------------------------------------------------------------

" 8 Custom inline scripts
    " 8.1 Show the list of all functions in current file - http://vim.wikia.com/wiki/VimTip79
    "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    function! ShowFunc()
        
        let gf_s = &grepformat
        let gp_s = &grepprg
        
        let &grepformat = '%*\k%*\sfunction%*\s%l%*\s%f %*\s%m'
        let &grepprg = 'ctags -x --c++-types=f --sort=no -o -'
        " for java. TODO: update it to handle all .java, .c, .cpp
        "let &grepprg = 'ctags -x --java-types=cfimp --sort=no -o -'

        write
        silent! grep %
        cwindow

        "let &grepformat = gf_s
        let &grepprg = gp_s
    endfunc

    "8.2 Always change the directory to working directory of file in current buffer - http://vim.wikia.com/wiki/VimTip64
    "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    function! CHANGE_CURR_DIR()
        let _dir = expand("%:p:h")
        exec "cd " . _dir
        unlet _dir
    endfunction

    "8.3 Save & Restore Vim Sessions in session files.
        "Save a session of Vim in specific sessionFile
        function! SaveSession(sessionFile)
            let $f=a:sessionFile
            mksession! $f
        endfunction

        "Restore a session of Vim from specific sessionFile
        function! RestoreSession(sessionFile)
            let $f=a:sessionFile
            source  $f
        endfunction

"----------------------------------------------------------------------------------------------------------

" 9 Custom Vim Setup to create new files/download other files.
    " 9.1 Default copyright header
    "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            " Whenever I create a new class in Java /C# , I want copyright header :).  Disable this if you don't want.
            au BufNewFile *.cs 0r $VIM/Header.cs
            au BufNewFile *.java 0r $VIM/Header.java

    " 9.2 Vim scripts - Install and uncomment below lines. By default these scripts are not part of Vim distribution.
    "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        " NOTE : Reason why downloaded scripts are kept separate from Vim distribution folder is to make sure we can upgrade to new version of
        " Vim easily and know which vim script files to be explicitly backedup/copied when you setup Vim on different machine
        " 9.2.1 Tags menu for various programming language source files 
            " http://www.vim.org/scripts/script.php?script_id=215
            "source $MY_VIM/FuncMenu.vim
        " 9.3 FTP Plugins
            "source $MY_VIM/intellisense.vim
            "source $MY_VIM/ftplugin/cs_vis.vim
            "source $MY_VIM/ftplugin/java_vis.vim
            "source $MY_VIM/ftplugin/html_vis.vim
        " 9.4 Jad Plugin - When .class file is opened with Vim, decompile it using jad.exe and show the source code.
        " Downlaod jad from http://www.varaneckas.com/jad and make sure jad " executable is in your system path. 
            "source $MY_VIM\jad.vim
        " 9.5 Favourites menu - Download from http://www.vim.org/scripts/script.php?script_id=161
            "source $MY_VIM/FavMenu.vim


let g:loaded_clipboard_provider = 1





