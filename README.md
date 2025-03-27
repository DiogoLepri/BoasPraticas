# Task Manager - Refatoração e Boas Práticas

Este projeto é um exemplo prático da importância da organização e aplicação de boas práticas em desenvolvimento web.

## Estrutura do Projeto

Este repositório está dividido em duas branches principais:

- **main**: Código inicial monolítico que exemplifica problemas comuns na organização de projetos.
- **refatorado**: Código reorganizado e otimizado com as melhores práticas.

Para acessar o código original:
```bash
git checkout main
```

Para acessar o código refatorado:
```bash
git checkout refatorado
```

## Sobre o Projeto

O **Task Manager** é um aplicativo web desenvolvido em Python usando Flask para gerenciar tarefas do dia a dia. Possui recursos básicos como cadastro e login, além da criação, edição e exclusão de tarefas. Cada tarefa pode ter título, descrição, prioridade, status e data de vencimento.

## Problemas Encontrados

Ao revisar o código original, identifiquei alguns pontos críticos:

- **Monolítico**: Tudo concentrado num único arquivo.
- **Mistura de responsabilidades**: Uma única função fazia muitas coisas diferentes.
- **Valores fixos no código**: Configurações sensíveis diretamente no código.
- **Desorganização**: Templates e arquivos estavam misturados sem uma estrutura clara.
- **Duplicação**: Código repetitivo em várias partes do sistema.
- **Dificuldade de expansão**: A falta de modularização dificultava adicionar recursos novos.
- **Funções muito grandes**: Difícil leitura e manutenção das funções extensas.

## Melhorias Implementadas

### Organização Modular

Criei uma nova estrutura mais clara e organizada:
```
task_manager/
├── app/
│   ├── __init__.py         # Criação da aplicação usando Factory Pattern
│   ├── config.py           # Configurações centralizadas
│   ├── db.py               # Acesso ao banco de dados
│   ├── auth/               # Autenticação
│   ├── tasks/              # Gestão de tarefas
│   ├── utils/              # Ferramentas auxiliares
│   ├── templates/          # Templates organizados por recurso
│   └── static/             # CSS, JS e imagens
└── run.py                  # Entrada da aplicação
```

### Separação clara (MVC)

O código foi reorganizado para que cada função tenha uma única responsabilidade:

- **Rotas**: Lidam apenas com requisições HTTP e renderização de páginas.
- **Modelos**: Lidam com operações no banco de dados.
- **Configuração**: Centralização das variáveis de ambiente e configurações sensíveis.

### Exemplo antes e depois da refatoração:

**Antes**:
```python
@app.route('/edit_task/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    # validações, lógica de banco de dados e renderização em uma só função
```

**Depois**:
```python
# Rotas:
@tasks_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    task = get_task(id)
    if request.method == 'POST':
        update_task(request.form)
    return render_template('tasks/edit.html', task=task)

# Modelos:
def update_task(data):
    # atualiza a tarefa no banco de dados
```

### Uso de Flask Blueprints

Separei as rotas em Blueprints, facilitando a organização por módulos:

```python
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
```

### Organização de Templates

Templates agora estão organizados por funcionalidades:
```
templates/
  ├── base.html
  ├── auth/
  │   ├── login.html
  │   └── register.html
  └── tasks/
      ├── index.html
      ├── add.html
      └── edit.html
```

### Tratamento de Erros e Feedback

Adicionei mensagens claras para o usuário usando Flash e melhorei a forma como os erros são tratados internamente.

### Documentação

Incluí comentários e docstrings claras em todos os módulos para facilitar futuras manutenções.

## Resultados

Após a refatoração, obtive:
- **Código mais limpo e legível**.
- **Facilidade de manutenção e expansão**.
- **Maior segurança e clareza das configurações**.
- **Facilidade para testes**.

## Contribuições

Este projeto foi desenvolvido individualmente, sendo responsável por:

- Análise e identificação dos problemas no código original.
- Planejamento da nova arquitetura.
- Implementação das melhorias e documentação do processo.

## Executando o Projeto

### Requisitos
- Python 3.8+
- pip

### Instalação
```bash
git clone https://github.com/seu-usuario/task-manager.git
cd task-manager

git checkout refatorado
pip install -r requirements.txt

python run.py
```

