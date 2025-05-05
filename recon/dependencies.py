import importlib.metadata
import subprocess, json, os, sys

from .utils import Console


def check_dependencies_file(dependencies_file_path: str):
    if not os.path.isfile(dependencies_file_path):
        Console.error(
            f"Arquivo de dependências não encontrado, path: {dependencies_file_path}"
        )
    data: dict = json.load(open(dependencies_file_path))

    if ((installers := data.get("installers")) is None) or (
        not isinstance(installers, dict)
    ):
        Console.error("Campo 'installers' inexistente ou não é um dicionário")
    for installer_name, installer_data in installers.items():
        if isinstance(installer_data, dict):
            if not all(
                command_type in installer_data.keys()
                for command_type in ["install", "check"]
            ):
                print(installer_data)
                Console.error(
                    "Todos os métodos de instalação de pacotes devem ter comandos de 'install' e 'check' de pacote"
                )

            if not all(
                (isinstance(command, str) and "{package}" in command)
                for command in installer_data.values()
            ):
                Console.error(
                    "Todos os comandos devem ser strings com o campo '{package}' presente para ser substituido pelo nome/url do pacote"
                )
        else:
            Console.error(
                f"O installer '{installer_name} deve ser um dicionário com os campos 'install' e 'check'"
            )

    if ((packages := data.get("packages")) is None) or (not isinstance(packages, list)):
        Console.error("Campo 'packages' inexistente ou não é uma lista")
    for package in packages:
        if isinstance(package, dict):
            if not all(
                package_info in package.keys()
                for package_info in ["name", "installer", "package"]
            ):
                Console.error(
                    "Todos os pacotes devem ter as informações 'name', 'installer' e 'package', sendo 'package' o nome/url a ser utilizado pelo 'installer' para encontrar e instalar o pacote"
                )

            if not all(
                (isinstance(command, str) and "{package}" in command)
                for command in installer_data.values()
            ):
                Console.error("Todos as informações devem ser strings")
        else:
            Console.error(
                f"Todos os pacotes devem ser dicionários, o valor {package}, não é válido"
            )

    return data


def pip_is_installed(package: str) -> bool:
    try:
        importlib.metadata.version(package)
        return True
    except ImportError as e:
        print(e)
        return False


def is_installed(
    package: dict[str, str],
    command: str,
) -> bool:

    try:
        if command.startswith("function:"):
            command = command.replace("function:", "").format(
                package=package.get("package")
            )
            return eval(command)

        command = command.format(package=package.get("package"))
        subprocess.run(
            command.split(" "),
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return True
    except subprocess.CalledProcessError as e:
        print(e)
        return False
    except Exception as e:
        Console.error(
            f"Durante a verificação do pacote '{package.get('name')}' usando o comando '{command}', o seguinte erro ocorreu:\n{e}"
        )


def install_package(
    package: dict[str, str],
    command: str,
) -> bool:
    try:
        command = command.format(
            package=(
                package.get("url")
                if package.get("installer") == "pip"
                else package.get("package")
            )
        )
        subprocess.run(
            command.split(" "),
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return True
    except subprocess.CalledProcessError as e:
        print(e)
        return False
    except Exception as e:
        Console.error(
            f"Durante a instalação do pacote '{package.get('name')}' usando o comando '{command}', o seguinte erro ocorreu:\n{e}"
        )


def check_installed_packages(
    dependencies_data: dict,
    packages_status: dict[str, bool] = {},
    verbose: bool = True,
) -> None:
    if verbose:
        Console.info("Verificando pacotes de ferramentas necessários")

    for package in dependencies_data.get("packages"):
        command = dependencies_data["installers"][package.get("installer")]["check"]
        installed = is_installed(package, command)
        packages_status[package.get("name")] = installed
        if verbose:
            if installed:
                Console.span(
                    "INSTALLED",
                    f"Pacote '{package.get('name')}' já está instalado",
                    "green",
                    "\t",
                )
            else:
                Console.span(
                    "UNINSTALLED",
                    f"Pacote '{package.get('name')}' não está instalado",
                    "red",
                    "\t",
                )


def install_packages(
    dependencies_data: dict,
    packages_status: dict[str, bool] = {},
    verbose: bool = True,
) -> None:
    if verbose:
        Console.info("Instalando pacotes Faltantes")
    
    for package in dependencies_data.get("packages"):
        if not packages_status[package.get("name")]:
            command = dependencies_data["installers"][package.get("installer")][
                "install"
            ]
            installed = install_package(package, command)
            packages_status[package.get("name")] = installed
            if verbose:
                if installed:
                    Console.span(
                        "INSTALLED",
                        f"Pacote '{package.get('name')}' instalado com sucesso!",
                        "green",
                        "\t",
                    )
                else:
                    Console.span(
                        "UNINSTALLED",
                        f"Não foi possível instalar o pacote '{package.get('name')}!'. Por favor, verifique manualmente",
                        "red",
                        "\t",
                    )


def dependencies_checker(
    dependencies_file_path: str,
    install_dependencies: bool = False,
    verbose: bool = True,
) -> dict:
    
    if os.name == "nt":
        Console.error("O gerenciador de dependências não foi projetado para funcionar em Sistemas Windows, não será possível checar as dependências.", exit=False)
        if not Console.YNinput('Deseja prosseguir sem a verificação de dependências'):
            sys.exit(0)
    
    dependencies_data = check_dependencies_file(dependencies_file_path)

    if len(dependencies_data.get("packages")) == 0:
        Console.error(
            f"Nenhuma ferramenta presente no arquivo de dependências, path {dependencies_file_path}"
        )

    Console.info("Verificando dependências, por favor agurde um instante...")
    packages_status = {}
    check_installed_packages(dependencies_data, packages_status, verbose)
    
    if install_dependencies:
        if not all([status for status in packages_status.values()]):
            if any([not status for status in packages_status.values()]):
                if Console.YNinput("Deseja instalar os pacotes faltantes?"):
                    install_packages(dependencies_data, packages_status, verbose)
                elif any(packages_status.values()):
                    pass
            elif Console.YNinput(
                "Nenhuma ferramenta instalada, deseja instala-las manualmente?"
            ):
                install_packages(dependencies_data, packages_status, verbose)
            else:
                sys.exit(0)
        
    packages_data = {}
    for package in dependencies_data["packages"]:
        name = package["name"]
        packages_data[name] = package
        packages_data[name]["status"] = packages_status.get(name, False)
    
    return packages_data

if __name__ == "__main__":
    
    PATH = os.path.dirname(os.path.abspath(__file__))
    print(dependencies_checker(os.path.join(PATH, "packages.json"), verbose=False))
