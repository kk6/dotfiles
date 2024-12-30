let $CACHE = expand('~/.cache')
if !($CACHE->isdirectory())
  call mkdir($CACHE, 'p')
endif
if &runtimepath !~# '/dein.vim'
  let s:dir = 'dein.vim'->fnamemodify(':p')
  if !(s:dir->isdirectory())
    let s:dir = $CACHE .. '/dein/repos/github.com/Shougo/dein.vim'
    if !(s:dir->isdirectory())
      execute '!git clone https://github.com/Shougo/dein.vim' s:dir
    endif
  endif
  execute 'set runtimepath^='
        \ .. s:dir->fnamemodify(':p')->substitute('[/\\]$', '', '')
endif

filetype plugin indent on
syntax enable

" ##### True color support
" from: https://github.com/rakr/vim-one#true-color-support 
" Credit joshdick
" Use 24-bit (true-color) mode in Vim/Neovim when outside tmux.
" If you're using tmux version 2.2 or later, you can remove the outermost $TMUX check and use tmux's 24-bit color support
" (see < http://sunaku.github.io/tmux-24bit-color.html#usage > for more information.)
if (empty($TMUX))
  if (has("nvim"))
  " For Neovim 0.1.3 and 0.1.4 < https://github.com/neovim/neovim/pull/2198 >
  let $NVIM_TUI_ENABLE_TRUE_COLOR=1
  endif
  " For Neovim > 0.1.5 and Vim > patch 7.4.1799 < https://github.com/vim/vim/commit/61be73bb0f965a895bfb064ea3e55476ac175162 >
  " Based on Vim patch 7.4.1770 (`guicolors` option) < https://github.com/vim/vim/commit/8a633e3427b47286869aa4b96f2bfc1fe65b25cd >
  " < https://github.com/neovim/neovim/wiki/Following-HEAD#20160511 >
  if (has("termguicolors"))
    set termguicolors
  endif
endif

" 行番号を表示
set number

" マウスを有効化
set mouse=a

" ヤンク時にクリップボードにいれる
set clipboard+=unnamedplus

" 文字コード関連
set fileencodings=utf-8,cp932,euc-jp,sjis
set encoding=utf-8
set fileformats=unix,dos,mac


set smarttab
set expandtab
set tabstop=4
set smartindent
set virtualedit=block
set shiftwidth=4

set ignorecase
set smartcase
set incsearch
set nohlsearch
set wrapscan

" for Python
let g:python_host_prog = $PYENV_ROOT.'/versions/2.7.15/bin/python'
let g:python3_host_prog = $PYENV_ROOT.'/versions/3.7.1/bin/python'
