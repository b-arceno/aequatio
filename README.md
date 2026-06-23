# Aequatio — Arena de Cálculo Mental

Protótipo funcional de software educacional para desenvolvimento do cálculo mental rápido, inspirado no conceito de "Esportes da Mente". Treine soma, subtração, multiplicação e divisão contra o relógio e acompanhe sua evolução.

* **Backend:** Python (Flask)
* **Frontend:** HTML + Tailwind CSS (compilado, sem dependência de internet) + JavaScript puro

## Objetivo Educacional

O Aequatio foi desenvolvido para auxiliar estudantes no aprimoramento do cálculo mental por meio de atividades gamificadas. O sistema busca estimular o raciocínio lógico, a agilidade matemática e a prática contínua das quatro operações fundamentais, fornecendo feedback imediato sobre o desempenho do usuário.

## Como rodar

### 1. Clone o repositório

```bash
git clone https://github.com/b-arceno/aequatio.git
cd aequatio
```

### 2. Instale as dependências

**Linux / Mac:**

```bash
pip3 install -r requirements.txt
```

Se aparecer o erro `externally-managed-environment` (comum em versões recentes do Ubuntu e Debian):

```bash
pip3 install -r requirements.txt --break-system-packages
```

**Windows** (Prompt de Comando ou PowerShell):

```bash
pip install -r requirements.txt
```

### 3. Execute o servidor

**Linux / Mac:**

```bash
python3 app.py
```

**Windows:**

```bash
python app.py
```

Você deverá visualizar no terminal:

```text
 * Running on http://127.0.0.1:5000
```

### 4. Acesse o sistema

Abra o navegador em:

```text
http://localhost:5000
```

> **Importante:** não abra o arquivo `index.html` diretamente pelo Explorer, Finder ou gerenciador de arquivos do sistema operacional. O Aequatio depende do servidor Python em execução para gerar e validar as questões matemáticas. Sempre acesse a aplicação pelo endereço acima, mantendo o terminal aberto.

## Estrutura do projeto

```text
.
├── app.py            # servidor Flask (API + frontend)
├── index.html        # interface completa (SPA), com CSS embutido
├── requirements.txt  # dependências Python
└── README.md
```

## API

### POST /gerar-questao

Recebe:

```json
{
  "operador": "+",
  "dificuldade": "iniciante"
}
```

Retorna:

```json
{
  "question_id": "abc123",
  "pergunta": "8 + 7",
  "operador_aplicado": "+"
}
```

### POST /validar-resposta

Recebe:

```json
{
  "question_id": "abc123",
  "resposta_usuario": 15,
  "acertos_rodada": 3,
  "total_rodada": 4
}
```

Retorna:

```json
{
  "correta": true,
  "resposta_certa": 15,
  "frase": "Excelente!"
}
```

A resposta correta de cada questão é armazenada temporariamente no servidor e não é enviada ao navegador antes da validação da resposta do usuário. Dessa forma, evita-se o acesso antecipado à solução por meio da inspeção do código da aplicação.

## Funcionalidades

* **Academia de Técnicas** — apresenta estratégias e truques de cálculo mental para as quatro operações fundamentais.
* **Arena de Competição** — permite escolher operador matemático, nível de dificuldade (Iniciante, Intermediário ou Avançado) e velocidade (Sem tempo, 10s, 5s ou 3s), respondendo a uma sequência de 10 questões com temporizador regressivo.
* **Painel de Evolução** — exibe histórico de partidas, percentual geral de acertos e melhor desempenho médio, armazenados localmente no navegador por meio do `localStorage`.
* **Interface Responsiva** — adaptação automática para computadores, tablets e smartphones, utilizando barra lateral em telas maiores e navegação fixa no rodapé em dispositivos móveis.

## Notas técnicas

* O Tailwind CSS é compilado e incorporado diretamente ao arquivo `index.html`, eliminando a dependência de CDNs ou conexões externas.
* O sistema funciona normalmente sem acesso à internet após sua instalação local.
* Não utiliza banco de dados. As informações de desempenho são armazenadas localmente no navegador por meio do `localStorage`, permitindo que cada usuário mantenha seu próprio histórico de utilização.
* A aplicação adota uma arquitetura simples cliente-servidor, em que o frontend se comunica com o backend Flask por meio de requisições HTTP.

## Tecnologias utilizadas

* Python
* Flask
* HTML5
* Tailwind CSS
* JavaScript
* LocalStorage (armazenamento local do navegador)

## Licença

Este projeto foi desenvolvido exclusivamente para fins educacionais.
