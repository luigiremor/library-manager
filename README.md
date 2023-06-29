# Analise de Requisitos - Sistema Library Manager

## 1. Introdução

O objetivo deste documento é estabelecer a descrição completa dos requisitos do sistema Library Manager. O Library Manager é um sistema de gerenciamento de bibliotecas desenvolvido para auxiliar bibliotecários e usuários na gestão e acesso a recursos da biblioteca.

## 2. Descrição Geral

### 2.1 Perspectiva do produto

O sistema Library Manager será uma aplicação autônoma que proporcionará uma interface intuitiva para gerenciar todos os recursos de uma biblioteca. Ele permitirá aos bibliotecários manterem o controle sobre o acervo da biblioteca, bem como gerenciar empréstimos de itens aos usuários.

### 2.2 Funções do produto

O Library Manager deverá permitir:

- Gestão de itens: Os bibliotecários poderão adicionar, atualizar e excluir itens da biblioteca. Eles poderão consultar a lista de todos os itens disponíveis.
- Gestão de usuários: O sistema permitirá o registro, atualização e exclusão de usuários. Além disso, será possível visualizar uma lista de todos os usuários registrados.
- Gestão de empréstimos: Os bibliotecários poderão criar, atualizar e excluir empréstimos de itens para os usuários.

## 3. Requisitos Específicos

### 3.1 Requisitos Funcionais

- **RF01** - O sistema deve permitir a adição de itens ao acervo da biblioteca.
- **RF02** - O sistema deve permitir a atualização dos dados de um item do acervo.
- **RF03** - O sistema deve permitir a exclusão de um item do acervo.
- **RF04** - O sistema deve permitir a consulta de todos os itens do acervo.
- **RF05** - O sistema deve permitir a criação de novos usuários.
- **RF06** - O sistema deve permitir a atualização das informações de um usuário.
- **RF07** - O sistema deve permitir a exclusão de um usuário.
- **RF08** - O sistema deve permitir a consulta de todos os usuários registrados.
- **RF09** - O sistema deve permitir o registro de empréstimos de itens para usuários.
- **RF10** - O sistema deve permitir o registro de devolução de itens para usuários.
- **RF11** - O sistema deve permitir a cobrança do valor de atraso na devolução de items dos usuários.
- **RF12** - O sistema deve permitir a quitação da dívida do usuário.
- **RF13** - O sistema deve permitir a consulta de todos os empréstimos registrados.
- **RF14** - O sistema deve permitir o cadastramento de novos bibliotecários.
- **RF15** - O sistema deve permitir o cadastro criptografado de senhas dos bibliotecários.
- **RF16** - O sistema deve permitir a autenticação de bibliotecários.

### 3.2 Requisitos Não Funcionais

- **RNF01** - O sistema deve ser desenvolvido em Python, utilizando a biblioteca tkinter para a interface gráfica.
- **RNF02** - O sistema deve fornecer uma interface amigável e intuitiva para facilitar sua utilização pelos bibliotecários.
- **RNF03** - O sistema deve ser robusto o suficiente para lidar com uma grande quantidade de itens e usuários.
- **RNF04** - O sistema deve ser capaz de manipular e armazenar os dados de forma segura e eficiente por meio de banco de dados.
- **RNF05** - O sistema deve ser capaz de armazenar as senhas dos bibliotecários de forma criptografada.
- **RNF06** - O sistema deve ser capaz de autenticar os bibliotecários por meio de suas senhas criptografadas.
- **RNF07** - O sistema deve possuir uma grande cobertura de testes automatizados.

## 4. Conclusão

A implementação deste sistema ajudará a melhorar a eficiência e a eficácia do gerenciamento de bibliotecas, proporcionando aos bibliotecários uma maneira fácil de gerenciar o acervo e aos usuários uma maneira conveniente de acessar os recursosda biblioteca.

## 5. Como executar o projeto

### 5.1 Pré-requisitos

- Python 3.8.5
- Pip 20.0.2
- Virtualenv 20.0.2

### 5.2 Instalação

1. Clone o repositório

   ```sh
   git clone https://github.com/luigiremor/library-manager.git
   ```

2. Crie um ambiente virtual

   ```sh
   python3 -m venv venv
   ```

3. Ative o ambiente virtual

   ```sh
   source venv/bin/activate
   ```

4. Instale as dependências

   ```sh
   pip install -r requirements.txt
   ```

5. Execute o projeto

   ```sh
   python3 main.py
   ```

## 6. Como executar os testes

1. Execute o comando abaixo para executar todos os testes

   ```sh
   python3 -m unittest discover
   ```
