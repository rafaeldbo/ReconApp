from typing import Callable
import sys, re, random, string


class Console:
    colors = {
        'gray': '\033[{bold}90m',
        'red': '\033[{bold}91m',
        'green': '\033[{bold}92m',
        'dark green': '\033[{bold}38;2;0;100;0m',
        'yellow': '\033[{bold}93m',
        'blue': '\033[{bold}94m',
        'cyan': '\033[{bold}96m',
        'purple': '\033[{bold}95m',
    }
    reset_color = '\033[0m'
    bold_style = '\033[1m'
    
    def style(text:str, color:str='', bold:bool=False) -> str:
        if text == '': return ''
        color = color.strip().lower()
        _bold = "1;" if bold else ""
        if color in Console.colors.keys():
            return Console.colors[color].format(bold=_bold) + text + Console.reset_color
        elif bold:
            return Console.bold_style + text + Console.reset_color
        return text


    def print(text:str, color:str='', tab:str='') -> None:
        print(tab + Console.style(text, color))
    
    def error(text:str, exit:bool=True, tab:str='') -> None:
        print(tab + Console.style('[ERRO] ', 'red') + text)
        if exit: sys.exit(1)

    def success(text:str, tab:str='') -> None:
        print(tab + Console.style('[SUCESSO] ', 'green') + text)

    def warning(text:str, tab:str='') -> None:
        print(tab + Console.style('[AVISO] ', 'yellow') + text)
        
    def info(text:str, tab:str='') -> None:
        print(tab + Console.style('[INFO] ', 'cyan') + text)
    
    def span(title:str, text:str, color:str, tab:str='') -> None:
        print(tab + Console.style(f'[{title.upper()}] ', color) + text)

    def input(text:str, pattern:str|re.Pattern[str]=None, parser:Callable[[str], any]=lambda x: x, instruction:str=None, default:str=None) -> any:
        instruction_text = Console.style(f' [ {instruction} ]', 'cyan') if instruction is not None else ''
        default_text = Console.style(f' [DEFAULT: {default} ]', 'cyan') if default is not None else '' 
        input_text = Console.style('[INPUT] ', 'cyan') + text + instruction_text + default_text + ': '
        if pattern is None:
            return parser(input(input_text))
        resp = None
        while (resp is None) or (re.fullmatch(pattern, resp) is None):
            resp = input(input_text)
            if (default is not None) and (resp == ""):
                return parser(default)
        return parser(resp)
    
    def YNinput(text:str) -> bool:
        yn = r'^(yes|y|sim|s|no|nao|não|n)$'
        input_text = Console.style('[INPUT] ', 'cyan') + text +  Console.style(' [ y | n ]', 'cyan') + ': '
        resp = ''
        while re.fullmatch(yn, resp) is None:
            resp = input(input_text).lower()
        return 'n' not in resp
    
    
ALPHA_NUMERIC = string.ascii_letters + string.digits
def random_str(length:int):
    return ''.join(random.choices(ALPHA_NUMERIC, k=length))