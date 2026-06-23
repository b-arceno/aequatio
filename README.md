# 🧠 Aequatio — Arena de Cálculo Mental

Protótipo funcional de app pedagógico de cálculo mental rápido, com tema de
"Esportes da Mente". Treine soma, subtração, multiplicação e divisão contra
o relógio, e acompanhe sua evolução.

- **Backend**: Python (Flask)
- **Frontend**: HTML + Tailwind CSS (compilado, sem dependência de internet) + JavaScript puro

## Como rodar

### 1. Clone o repositório
```bash
git clone https://github.com/SEU-USUARIO/NOME-DO-REPOSITORIO.git
cd NOME-DO-REPOSITORIO
```

### 2. Instale as dependências

**Linux / Mac:**
```bash
pip3 install -r requirements.txt
```
Se aparecer erro `externally-managed-environment` (comum em Ubuntu/Debian
recentes):
```bash
pip3 install -r requirements.txt --break-system-packages
```

**Windows** (no Prompt de Comando ou PowerShell):
```bash
pip install -r requirements.txt
```

### 3. Rode o servidor

**Linux / Mac:**
```bash
python3 app.py
```

**Windows:**
```bash
python app.py
```

Você deve ver no terminal:
```
 * Running on http://127.0.0.1:5000
```

### 4. Jogue
Abra o navegador em:
```
http://localhost:5000
```

**Importante:** não abra o `index.html` direto pelo Explorer/Finder — o jogo
precisa do servidor Python rodando para gerar e validar as questões. Sempre
acesse pelo endereço acima, com o terminal aberto.

## Estrutura do projeto

```
.
├── app.py              # servidor Flask (API + serve o frontend)
├── index.html           # interface completa (SPA), com CSS já embutido
├── requirements.txt      # dependências Python
└── README.md
```

## API

- `POST /gerar-questao` → recebe `{operador, dificuldade}`, retorna
  `{question_id, pergunta, operador_aplicado}`.
- `POST /validar-resposta` → recebe `{question_id, resposta_usuario,
  acertos_rodada, total_rodada}`, retorna `{correta, resposta_certa,
  frase}`.

A resposta correta de cada questão fica guardada em memória no servidor,
nunca é enviada ao navegador antes da validação — evita que a resposta seja
"lida" inspecionando o código do navegador.

## Funcionalidades

- **Academia de Técnicas** — truques de cálculo mental para os 4 operadores.
- **Arena de Competição** — escolha operador, dificuldade (Iniciante /
  Intermediário / Avançado) e velocidade (Sem tempo / 10s / 5s / 3s), e
  responda 10 questões em sequência com timer visual regressivo.
- **Painel de Evolução** — histórico de rodadas, taxa de acerto geral e
  melhor tempo médio, salvos localmente no navegador (`localStorage`).

Totalmente responsivo: layout em sidebar no desktop/tablet, e barra de
navegação fixa no rodapé (estilo app nativo) em celulares.

## Notas técnicas

- O CSS do Tailwind vem **compilado e embutido** no próprio `index.html`
  (não depende de CDN externo), então o app funciona normalmente mesmo sem
  internet ou atrás de firewalls restritivos.
- Sem banco de dados — o histórico fica no navegador de cada pessoa. Cada
  colega que testar terá seu próprio histórico, separado.
