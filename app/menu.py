import sys, re

from .utils import Console, random_str
from .executor import run_subprocess

FIELD_REGEX = r"\{[_a-zA-Z][_a-zA-Z0-9]*\}"

class MenuException(Exception):
    pass

class MenuManager:
    menus = {}
    current: str = None
    initial: str = None
    back:list[str] = []
    
    def gen_id() -> id:
        id = random_str(10)
        while id in MenuManager.menus.keys():
            id = random_str(10)
        return id

    def check_options(menu_options:list[dict]) -> None:
        names = []
        if (not isinstance(menu_options, list)) or (len(menu_options)) == 0:
            raise MenuException("O menu deve ter pelo menos uma opção")
        
        for option in menu_options:
            if (not isinstance(option, dict)):
                raise MenuException("Todas as opções do menu devem ser dicionários")
            
            name = option.get("name")
            if (name is None) or (not isinstance(name, str)) or (name == '') or (name in names):
                raise MenuException("Todos as opções do menu devem ter um nome único")
            names.append(names)
            
            option_type = option.get("type")
            if (option_type is None) or (not isinstance(option_type, str)) or (option_type not in ["menu", "command"]):
                raise MenuException("Todas as opções devem ser do tipo 'Menu' ou 'Command'")
            
            if (option_type == "command"):
                command_data = option.get("command")
                if (command_data is None) or (not isinstance(command_data, dict)):
                    raise MenuException("Uma opção do tipo 'Command' deve ter um campo 'command' com as instruções do comando")
                
                command = command_data.get("command")
                if (command is None) or (not isinstance(command, str)) or (command == ''):
                    raise MenuException("Comando da opção do tipo 'Command' não especificado")
                
                command_fields = [match[1:-1] for match in re.findall(FIELD_REGEX, command)]
                if len(command_fields) > 0:
                    fields = command_data.get("fields")
                    if (fields is None) or (not isinstance(fields, dict)):
                        raise MenuException(f"O commando '{command_data['name']}' possui {len(command_fields)} parâmetros, mas há instruções de como pega-los")
                    
                    for field in command_fields:
                        if field not in fields.keys():
                            raise MenuException(f"O parâmetro {field} não possui um conjuto de instruções sobre como pega-lo")
                        field_text = fields[field].get("text")
                        if (field_text is None) or (not isinstance(field_text, str)):
                            raise MenuException(f"O parâmetro {field} não possui um texto de aquisição")        
            
            enable = option.get("enable")
            if (enable is not None):
                if (not isinstance(enable, bool)):
                    raise MenuException("O campo 'enable' de uma opção deve ser um boolean")
            else:
                option["enable"] = True
    
    def add_menu(title:str, menu_options:list[dict], description:str="", id:str=None) -> str:
        MenuManager.check_options(menu_options)
        if (title is None) or (not isinstance(title, str)):
            raise MenuException("Todo menu deve ter um titulo")
        elif (description is not None) and (not isinstance(description, str)):
            raise MenuException("A descrição de um menu deve ser uma string")
        
        if (id is not None):
            if (not isinstance(id, str)) or (id in MenuManager.menus.keys()):
                raise MenuException("o id de um menu deve ser uma string única")
        else: id = MenuManager.gen_id()
        
        MenuManager.menus[id] = {
            "title": title,
            "description": description,
            "options": menu_options
        }
        
    def to_menu(menu:str) -> None:
        if menu not in MenuManager.menus.keys():
            raise MenuException(f"menu '{menu}' não encontrado")
        MenuManager.back.append(MenuManager.current)
        MenuManager.current = menu
        
    def back_menu() -> None:
        if len(MenuManager.back) == 0:
            sys.exit()
        MenuManager.current = MenuManager.back[-1]
        MenuManager.back.pop()
        
    def back_to_init() -> None:
        MenuManager.current = MenuManager.initial
        MenuManager.back = []
        
    def menu_option(name:str, enable:bool=True) -> dict:
        return {
            "name": name, 
            "type": 'menu', 
            "enable": enable
        }
    
    def command_option(name: str, command_data:dict) -> dict:
        return {
            "name": name,
            "type": "command",
            "command": command_data,
        }
        
    def write_menu() -> None:
        menu_data = MenuManager.menus[MenuManager.current]
        
        print()
        Console.span("MENU", Console.style(menu_data["title"], bold=True), "cyan")
        if menu_data["description"] != "":
            Console.print(menu_data["description"])
        
        
        for i, option in enumerate(menu_data["options"]):
            if option["enable"]:
                Console.span(f"{i+1:2}", option["name"], "cyan", tab="\t")
            else:
                Console.print(f"[{i+1:2}] {option['name']}", "gray", tab="\t")
    
        Console.span(
            f"{0:2}", 
            "Voltar para o Menu anterior" if len(MenuManager.back) != 0 else "Sair", 
            "cyan", 
            tab="\t"
        )
                
    def select_input() -> None:
        menu = MenuManager.current
        menu_data = MenuManager.menus[menu]
        
        options = menu_data["options"]
        selected = -1
        while True:
            selected = Console.input("Selecione uma opção", r"^\d+$", int, f"0-{len(options)}")-1
            if selected < len(options) and menu_data["options"][selected]["enable"]:
                break
            Console.span("INVALID", "Ecolha o número de uma das opções ativas acima", "yellow", tab="\t")
            
        if selected == -1:
            return MenuManager.back_menu() 
        
        option = options[selected]
        if option["type"] == "menu":
            return MenuManager.to_menu(option["name"])
        elif option["type"] == "command":
            return MenuManager.exec_command(option["command"])
        
    def run(start_menu:str="start") -> None:
        menu_data = MenuManager.menus.get(start_menu)
        if menu_data is None:
            raise MenuException(f"menu '{start_menu}' não encontrado")
        
        MenuManager.initial = start_menu
        MenuManager.current = start_menu
        
        while True:
            MenuManager.write_menu()
            MenuManager.select_input()
            
    def exec_command(command:dict[str, str|dict]) -> None:
        try:
            args = {field: Console.input(**field_args) for field, field_args in command["fields"].items()}
            print()
            run_subprocess(command["command"], args)
            print()
            Console.input("Pressione [ENTER] para continuar")
            MenuManager.back_to_init()
        except KeyboardInterrupt:
            print()
            Console.warning("Cancelando Comando a pedido do usuário (Ctrl+C)...", tab="\t")
            
            
def generate_menu_by_command_group(command_group:dict) -> None:
    options:list[dict] = []
    
    command_groups:list[dict] = command_group.get("command_groups", [])
    for other_command_group in command_groups:
        generate_menu_by_command_group(other_command_group)
        options.append(
            MenuManager.menu_option(other_command_group["name"])
        )
        
    commands:list[dict] = command_group.get("commands", [])
    for command in commands:
        options.append(
            MenuManager.command_option(command["name"], command)
        )
        
    if len(options) == 0: return
        
    MenuManager.add_menu(
        command_group["name"], 
        options, 
        command_group.get("description", ""), 
        id=command_group["name"]
    )  
        
        
def generate_menu_by_packages(packages:dict[str, dict]) -> None:
    MenuManager.add_menu(
        "Selecione uma ferramenta", 
        [
            MenuManager.menu_option(package["name"], package["status"]) 
                for package in packages.values() 
                    if package.get("commands") is not None
        ],
        "Escolha uma ferramenta para coletar informações dos alvos",
        id="start"
    )
    for package in packages.values():
        if package.get("commands") is not None:
            generate_menu_by_command_group(package)
        
        
        
        
        
        
        
    
        