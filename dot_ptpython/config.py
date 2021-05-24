# Source: https://github.com/jonathanslenders/ptpython/blob/master/examples/ptpython_config/config.py
# Pygments CSS Themes: http://jwarby.github.io/jekyll-pygments-themes/languages/python.html


def configure(repl):
    repl.vi_mode = True
    repl.confirm_exit = False
    repl.highlight_matching_parenthesis = True
    repl.color_depth = "DEPTH_24_BIT"
    repl.use_code_colorscheme("native")
