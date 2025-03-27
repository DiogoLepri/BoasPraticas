# Task Manager - Refatoração e Aplicação de Boas Práticas

## Estrutura do Repositório

Este repositório está organizado em duas branches principais:

- **main**: Contém o código original monolítico, demonstrando problemas comuns de organização
- **refatorado**: Contém o código após a refatoração, aplicando boas práticas de desenvolvimento

Para ver o código original:
```bash
git checkout main
```

Para ver o código refatorado:
```bash
git checkout refatorado
```

## O Projeto e seu Propósito

O **Task Manager** é um aplicativo web desenvolvido em Python com Flask que permite aos usuários gerenciar suas tarefas diárias. O sistema oferece funcionalidades de cadastro e autenticação de usuários, além de permitir criar, visualizar, editar e excluir tarefas. Cada tarefa possui atributos como título, descrição, prioridade, status e data de vencimento.

### Propósito Original
O sistema foi originalmente desenvolvido como um único arquivo monolítico, priorizando a funcionalidade em detrimento da organização do código. O projeto atendia às necessidades básicas dos usuários, mas apresentava limitações significativas em termos de manutenibilidade e escalabilidade.

## Análise Crítica do Código Original

Após revisar o código existente, identificamos os seguintes problemas relacionados à organização e estrutura:

### 1. Código Monolítico
Todo o sistema estava contido em um único arquivo `app.py`, misturando configurações, modelos de dados, lógica de negócios, autenticação e rotas. Isso dificultava a manutenção e o entendimento do código.

```python
# Exemplo do código original monolítico - app.py
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import sqlite3
# [+ diversos outros imports]

app = Flask(__name__)
app.secret_key = "very-secret-key-should-be-changed"
DATABASE = "tasks.db"

# Definição de banco de dados, modelos, autenticação, rotas - tudo em um único arquivo
# [400+ linhas de código misturadas]

if __name__ == '__main__':
    app.run(debug=True)
```

### 2. Ausência de Separação de Responsabilidades
O código violava o Princípio da Responsabilidade Única (SRP), com funções realizando múltiplas tarefas:

```python
# Exemplo de rota com múltiplas responsabilidades
@app.route('/add_task', methods=['GET', 'POST'])
@login_required
def add_task():
    # Lógica de validação de formulário
    # Manipulação direta de banco de dados
    # Renderização de templates
    # Redirecionamento
    # Tudo na mesma função!
```

### 3. Valores Hardcoded
Informações sensíveis e configurações estavam codificadas diretamente no código-fonte:

```python
app.secret_key = "very-secret-key-should-be-changed"
DATABASE = "tasks.db"
```

### 4. Falta de Organização de Templates
Todos os templates HTML estavam no mesmo nível, sem organização por funcionalidade.

### 5. Código Duplicado
Várias rotas continham lógica similar para validação, autenticação e acesso ao banco de dados.

### 6. Ausência de Modularização
Não havia separação lógica entre componentes do sistema, dificultando o isolamento de bugs e a implementação de novos recursos.

### 7. Funções Extensas
Algumas funções de rota eram muito longas e realizavam muitas operações, dificultando os testes e a manutenção.

## Implementação das Melhorias

Com base nos problemas identificados, realizamos uma refatoração completa do código aplicando boas práticas de desenvolvimento:

### 1. Adoção de uma Estrutura Modular

Reorganizamos o projeto seguindo uma estrutura por pacotes:

```
task_manager/
├── app/
│   ├── __init__.py             # Factory Pattern para criação da aplicação
│   ├── config.py               # Configurações centralizadas
│   ├── db.py                   # Utilitários de banco de dados
│   ├── auth/                   # Módulo de autenticação
│   ├── tasks/                  # Módulo de gerenciamento de tarefas
│   ├── utils/                  # Utilitários e decoradores
│   ├── templates/              # Templates organizados por feature
│   └── static/                 # Arquivos estáticos (CSS, JS)
└── run.py                      # Ponto de entrada da aplicação
```

### 2. Separação de Responsabilidades (Padrão MVC)

**ANTES:**
```python
@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    db = get_db()
    cursor = db.cursor()
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        priority = request.form['priority']
        due_date = request.form['due_date']
        status = request.form['status']
        
        cursor.execute(
            "UPDATE tasks SET title = ?, description = ?, status = ?, priority = ?, due_date = ? WHERE id = ? AND user_id = ?",
            (title, description, status, priority, due_date, task_id, session['user_id'])
        )
        db.commit()
        db.close()
        
        return redirect(url_for('home'))
    
    cursor.execute("SELECT * FROM tasks WHERE id = ? AND user_id = ?", (task_id, session['user_id']))
    task = cursor.fetchone()
    db.close()
    
    if not task:
        return redirect(url_for('home'))
    
    return render_template('edit_task.html', task=task)
```

**DEPOIS:**
```python
# app/tasks/routes.py - Controlador
@tasks_bp.route('/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    """Edit an existing task"""
    task = get_task(task_id, session['user_id'])
    
    if not task:
        flash('Task not found or you do not have permission to edit it.', 'error')
        return redirect(url_for('tasks.index'))
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        priority = request.form['priority']
        due_date = request.form['due_date']
        status = request.form['status']
        
        success = update_task(
            task_id=task_id,
            title=title,
            description=description,
            status=status,
            priority=priority,
            due_date=due_date,
            user_id=session['user_id']
        )
        
        if success:
            flash('Task updated successfully!', 'success')
        else:
            flash('Error updating task.', 'error')
        
        return redirect(url_for('tasks.index'))
    
    return render_template('tasks/edit.html', task=task)

# app/tasks/models.py - Modelo
def update_task(task_id, title, description, status, priority, due_date, user_id):
    """
    Update an existing task
    
    Args:
        task_id (int): Task ID
        title (str): Task title
        description (str): Task description
        status (str): Task status
        priority (str): Task priority
        due_date (str): Task due date
        user_id (int): User ID
        
    Returns:
        bool: True if successful, False otherwise
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE tasks SET title = ?, description = ?, status = ?, priority = ?, due_date = ? WHERE id = ? AND user_id = ?",
        (title, description, status, priority, due_date, task_id, user_id)
    )
    db.commit()
    return cursor.rowcount > 0
```

### 3. Centralização das Configurações

**ANTES:**
```python
app = Flask(__name__)
app.secret_key = "very-secret-key-should-be-changed"
DATABASE = "tasks.db"
```

**DEPOIS:**
```python
# app/config.py
import os
from datetime import timedelta

class Config:
    """Base configuration class for the application"""
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database settings
    DATABASE = os.path.join(os.getcwd(), 'instance', 'tasks.db')
    
    # Session settings
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
    
    # Application settings
    TASK_STATUSES = ['todo', 'in-progress', 'done']
    TASK_PRIORITIES = ['low', 'medium', 'high']
```

### 4. Implementação de Flask Blueprints

Utilizamos Blueprints para organizar rotas por domínio:

```python
# app/auth/routes.py
from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Lógica de login
```

### 5. Reorganização dos Templates

**ANTES:**
```
templates/
  ├── index.html
  ├── login.html
  ├── register.html
  ├── add_task.html
  └── edit_task.html
```

**DEPOIS:**
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

### 6. Melhoria no Tratamento de Erros

Implementamos um sistema de mensagens flash para fornecer feedback ao usuário e melhoramos o tratamento de exceções em toda a aplicação.

### 7. Documentação Abrangente

Adicionamos docstrings detalhadas a todas as funções, classes e módulos, seguindo as convenções PEP 257.

## Resultados Obtidos

A refatoração resultou em:

1. **Maior Modularidade**: O código agora é organizado por funcionalidade, facilitando a localização e manutenção.
2. **Melhor Legibilidade**: Funções mais curtas e com responsabilidades únicas.
3. **Manutenibilidade Aprimorada**: Mudanças em um componente não afetam outros componentes.
4. **Escalabilidade**: Novos recursos podem ser adicionados como módulos independentes.
5. **Melhor Segurança**: Configurações sensíveis centralizadas e possibilidade de usar variáveis de ambiente.
6. **Código mais Testável**: Componentes isolados podem ser testados independentemente.

## Contribuições

Este projeto foi desenvolvido individualmente, sendo responsável por:

1. Análise do código original e identificação de problemas
2. Planejamento da nova arquitetura
3. Implementação da refatoração
4. Documentação do processo e das melhorias

## Como Executar o Projeto

### Pré-requisitos
- Python 3.8+
- pip (gerenciador de pacotes Python)

### Instalação
```bash
# Clone o repositório
git clone https://github.com/seu-usuario/task-manager.git
cd task-manager

# Para o código refatorado
git checkout refatorado

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
python run.py
```