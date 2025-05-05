# **recon-app**
`Applicativo CLI de Reconhecimento de Alvo PenTest` desenvolvido em `python` para a disciplina de Tecnologias Hacker (Insper 2025.1).

## **Funcionalidades**
- Verificação e instalação automática de dependências
- Adição fácil de novos ferramentas e comandos por meio do arquivo [`packages.json`](recon/packages.json)
- 9 ferramentas pré-configuradas:
    - **Port-Scanner** proprietário (código fonte disponível em [rafaeldbo/port-scan](https://github.com/rafaeldbo/recon-app))
    - **WHOIS lookup**
    - **DNS utilities**
    - **WAFW00F**
    - **Nikto**
    - **SSLyze**
    - **Dirb**
    - **Nmap** (script vuln)
    - **Wappalyzer CLI** (código fonte disponível em [gokulapap/wappalyzer-cli]()https://github.com/gokulapap/wappalyzer-cli)

## **Como Instalar**
Faça a instalação diretamente em seu terminal por meio do `pip`

```
pip install git+https://github.com/rafaeldbo/recon-app
```
⚠️ **AVISO** ⚠️

Este programa foi desenvolvido utilizando **Python 3.13**, por isso, pode não funcionar corretamente para versões anteriores,

## **Como Utilizar**
Esse programa funciona apenas por linha de comando, utilize o comando a baixo para executar:
```
$ recon [-h] [-i] [-v]
```
Após executar, será vaerificado quais dependências estão instaladas (por meio do comando `apt list {package}`). Em seguida o menu com as ferramentas irá aparecer. Utilize os números para se mover entre os menus.

 **Flags  Opcionais**
- `-i` ou `--install`: ativa a instalação automática de dependências (por meio do comando `sudo apt install {package}`).
- `-v` ou `--verbose`: exibe mensagens adicionais durante a execução do aplicativo (WIP)

## **Desenvolvedor**

- Rafael Dourado Bastos de Oliveira [[Linkedin]](https://www.linkedin.com/in/rafael-dourado-rdbo/)