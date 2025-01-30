<h1 align="center" style="font-weight: bold;">Meu C$50 Finance</h1>

<div align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white&style=for-the-badge" alt="Python Badge">
  <img src="https://img.shields.io/badge/Flask-000000?logo=flask&logoColor=white&style=for-the-badge" alt="Flask Badge">
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5 Badge">
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite Badge">
</div>

#

_Outras versões:_
[_Click here for English_](./README.md)

<h4 align="center"> 
     Status: Concluído
</h4>

<p align="center">
 <a href="#sobre-ℹ️">Sobre</a> •
 <a href="#funcionalidades-🌟">Funcionalidades</a> •
 <a href="#demonstração-do-projeto-🖥️">Demonstração</a> •
 <a href="#arquitetura-da-aplicação-🏗️">Arquitetura da Aplicação</a> •
 <a href="#configuração-⚙️">Configuração</a>  • 
 <a href="#autor-👨🏻‍💻">Autor</a> •
 <a href="#licença-📝">Licença</a>
</p>

#

<h6 align="justify"><b>Aviso Importante:</b> Este projeto foi desenvolvido como parte do curso CS50x. Se você está atualmente fazendo o curso, por favor, não visualize ou copie este código, pois isso pode violar a política de honestidade acadêmica do curso. Use este repositório apenas como referência após ter concluído o curso.
</h6>

#

## Sobre ℹ️
C$50 Finance é uma aplicação web construída utilizando Flask, ela permite aos usuários simular a negociação de ações. Os usuários podem se registrar e fazer login com um nome de usuário e senha únicos. A aplicação busca os preços atuais das ações e permite que os usuários comprem, vendam ou mantenham ações. Ela mantém um histórico de transações para cada usuário, rastreando seu portfólio e atualizando-o com base nas mudanças de preços das ações em tempo real. Além disso, os usuários podem adicionar mais dinheiro à sua conta e alterar suas senhas. A aplicação original foi construída usando um endpoint de API que fornecia dados em CSV, que não está mais disponível. Por conta disso, ela foi ajustada para usar um novo endpoint de API que retorna dados em JSON.

## Funcionalidades 🌟
- Registro e autenticação de usuários
- Simular compra e venda de ações com preços atuais
- Visualizar histórico de transações
- Gerenciar portfólio e visualizar preços atuais das ações
- Adicionar dinheiro à conta do usuário
- Permitir que os usuários alterem a senha

## Demonstração do Projeto 🖥️
[veja a demonstração clicando aqui](https://youtu.be/nAXZgyfQJnw)

## Arquitetura da Aplicação 🏗️

O backend é projetado usando Flask e SQLite. Os principais módulos incluem:
- `app.py`: Contém as rotas e a lógica principal da aplicação.
- `helpers.py`: Contém funções auxiliares para a aplicação, incluindo a função `lookup` para consultar preços de ações.
- `templates/`: Contém templates HTML para renderizar as páginas web. Usa um template de layout e Jinja para gerar dinamicamente o conteúdo.
- `static/`: Contém arquivos estáticos como CSS para estilização.

### Fluxo de Dados
1. **Registro/Login de Usuário**: Os usuários podem se registrar e fazer login na aplicação.
2. **Transações de Ações**: Os usuários podem comprar e vender ações. A aplicação consulta a API do Yahoo Finance para obter os preços mais recentes das ações.
3. **Gerenciamento de Portfólio**: Os usuários podem visualizar seu portfólio, incluindo o valor atual de suas ações e o histórico de transações.
4. **Banco de Dados**: Todos os dados dos usuários, transações e informações de ações são armazenados em um banco de dados SQLite.

## Configuração ⚙️
Para configurar o projeto localmente, siga estes passos:

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/rafaelmeller/finance-cs50.git
   cd finance-cs50
   ```

2. **Crie um ambiente virtual (Mac)**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Instale os pacotes necessários**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute a aplicação**:
   ```bash
   flask run
   ```

## Autor 👨🏻‍💻

#### Rafael Meller, Equipe CS50
<h6><i>Este projeto foi um conjunto de problemas para o curso de Introdução à Ciência da Computação de HarvardX (CS50x), sendo parcialmente desenvolvido pela equipe do CS50 e depois finalizado por Rafael Meller</i></h6>

[![Linkedin Badge](https://img.shields.io/badge/-Rafael_Meller-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/tgmarinho/)](https://www.linkedin.com/in/rafaelmeller/) 
[![Gmail Badge](https://img.shields.io/badge/-rafaelmeller.dev@gmail.com-c14438?style=flat-square&logo=Gmail&logoColor=white&link=rafaelmeller.dev@gmail.com)](mailto:rafaelmeller.dev@gmail.com)

## Licença 📝

Este projeto está licenciado sob a [MIT](./LICENSE) License. O "problem set" original é propriedade do CS50.
