import argparse
import os, sys

from .dependencies import dependencies_checker
from .utils import Console
from .menu import MenuManager, generate_menu_by_packages


TITLE = r"""
    ____                        ___    ____  ____ 
   / __ \___  _________  ____  /   |  / __ \/ __ \
  / /_/ / _ \/ ___/ __ \/ __ \/ /| | / /_/ / /_/ /
 / _, _/  __/ /__/ /_/ / / / / ___ |/ ____/ ____/ 
/_/ |_|\___/\___/\____/_/ /_/_/  |_/_/   /_/      
"""
SUBTITLE = r"""
Seu aplicativo de reconhecimento de Alvo
V1.0.0 Copyright © Rafael Dourado Bastos de Oliveira
"""

def main() -> None:
    try:
        PATH = os.path.dirname(os.path.abspath(__file__))
        
        parser = argparse.ArgumentParser(
                        description="Agrupa e e facilita o uso de ferramentas básicas de reconhecimento de um alvo",
                        epilog="Use com moderação")
        # group = parser.add_mutually_exclusive_group()
        parser.add_argument("-i", "--install", action="store_true", help="Permite que a aplicação tente instalar as dependências faltantes automaticamente")
        parser.add_argument("-v", "--verbose", action="store_true",  help="Permite a exebição de todas as mensagem, aumentado a quantidade de informação passada para o usuário. Pode causar poluição visual")
        args = parser.parse_args()

        packages = dependencies_checker(os.path.join(PATH, "packages.json"), args.install, args.verbose)
        
        generate_menu_by_packages(packages)
        
        Console.print(TITLE, "cyan")
        Console.print(SUBTITLE)
        
        MenuManager.run()
        
    except KeyboardInterrupt:
        print()
        Console.warning("Encerrando programa a pedido do usuário (Ctrl+C)...")
        sys.exit(0)
        

if __name__ == "__main__":
    main()