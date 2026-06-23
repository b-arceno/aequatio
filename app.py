"""
Aequatio - Backend (Flask)
API para o app de cálculo mental rápido "Esportes da Mente".

Rotas:
    GET  /                  -> serve o frontend (index.html)
    POST /gerar-questao     -> gera uma questão matemática
    POST /validar-resposta  -> valida a resposta do usuário

Rodar com:
    pip install flask
    python app.py

Depois acesse http://localhost:5000 no navegador (o próprio Flask já serve o
index.html). Não é necessário nenhum servidor frontend separado.
"""

import random
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder=".", static_url_path="")


@app.after_request
def liberar_cors(response):
    """
    Libera CORS manualmente (sem depender do pacote flask-cors), permitindo
    que o index.html seja aberto tanto via http://localhost:5000 (servido
    pelo próprio Flask) quanto via outra origem/porta durante o desenvolvimento.
    """
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

@app.route("/gerar-questao", methods=["OPTIONS"])
@app.route("/validar-resposta", methods=["OPTIONS"])
def preflight_cors():
    return "", 204


# CONFIGURAÇÃO DE DIFICULDADE
# Iniciante:     1 dígito  (1-9)      operando com 1 dígito  (1-9)
# Intermediário: 2 dígitos (10-99)    operando com 1 dígito  (1-9)
# Avançado:      2-3 dígitos (10-999) operando com 2-3 dígitos (10-999)
RANGES = {
    "iniciante": {
        "a": (1, 9),
        "b": (1, 9),
    },
    "intermediario": {
        "a": (10, 99),
        "b": (1, 9),
    },
    "avancado": {
        "a": (10, 999),
        "b": (10, 999),
    },
}

OPERADORES_VALIDOS = ["soma", "subtracao", "multiplicacao", "divisao", "misto"]

# Frases motivacionais por faixa de desempenho (taxa de acerto na rodada)
FRASES_ACERTO = [
    "Resposta certeira! Continue nesse ritmo.",
    "Isso aí, atleta! Reflexo de campeão.",
    "Cálculo na veia! Próxima.",
    "Mente afiada como navalha!",
    "Boa! Você está voando.",
]

FRASES_ERRO = [
    "Quase! Respira e tenta a próxima.",
    "Errou, mas todo campeão erra no treino.",
    "Foco! A próxima é sua.",
    "Sem problema, ajusta a mira e segue.",
    "Não desanima, o treino é assim mesmo.",
]


# LÓGICA DE GERAÇÃO DE QUESTÕES
def _gerar_operandos(dificuldade: str):
    """Retorna (a, b) dentro do range configurado para a dificuldade."""
    cfg = RANGES.get(dificuldade, RANGES["iniciante"])
    a_min, a_max = cfg["a"]
    b_min, b_max = cfg["b"]
    a = random.randint(a_min, a_max)
    b = random.randint(b_min, b_max)
    return a, b


def _gerar_divisao_exata(dificuldade: str):
    """
    Gera uma divisão com resultado inteiro exato (sem resto), respeitando
    a magnitude esperada pela dificuldade. Constrói o dividendo a partir
    de divisor x quociente, para garantir divisão exata.

    O divisor e o quociente são escolhidos com faixas próprias (menores que
    o range geral de operandos), para que o dividendo final fique numa
    magnitude condizente com cálculo mental, em vez de números gigantes.
    """
    if dificuldade == "iniciante":
        divisor = random.randint(2, 9)
        quociente = random.randint(1, 9)
    elif dificuldade == "intermediario":
        divisor = random.randint(2, 12)
        quociente = random.randint(2, 12)
    else:  # avancado
        divisor = random.randint(2, 30)
        quociente = random.randint(10, 40)

    dividendo = divisor * quociente
    return dividendo, divisor, quociente


def gerar_questao(operador: str, dificuldade: str):
    """
    Monta a string da pergunta e calcula a resposta correta.
    Retorna (pergunta: str, resposta: int|float).
    """
    dificuldade = dificuldade if dificuldade in RANGES else "iniciante"

    if operador == "misto":
        operador_real = random.choice(["soma", "subtracao", "multiplicacao", "divisao"])
    else:
        operador_real = operador if operador in OPERADORES_VALIDOS else "soma"
        if operador_real == "misto":
            operador_real = random.choice(["soma", "subtracao", "multiplicacao", "divisao"])

    if operador_real == "soma":
        a, b = _gerar_operandos(dificuldade)
        pergunta = f"{a} + {b}"
        resposta = a + b

    elif operador_real == "subtracao":
        a, b = _gerar_operandos(dificuldade)
        # garante resultado não-negativo (mais pedagógico para cálculo mental)
        if b > a:
            a, b = b, a
        pergunta = f"{a} - {b}"
        resposta = a - b

    elif operador_real == "multiplicacao":
        # multiplicação usa operandos um pouco menores para não ficar absurda
        if dificuldade == "iniciante":
            a, b = _gerar_operandos("iniciante")
        elif dificuldade == "intermediario":
            a = random.randint(10, 99)
            b = random.randint(2, 9)
        else:  # avancado
            a = random.randint(10, 99)
            b = random.randint(2, 99)
        pergunta = f"{a} x {b}"
        resposta = a * b

    elif operador_real == "divisao":
        dividendo, divisor, quociente = _gerar_divisao_exata(dificuldade)
        pergunta = f"{dividendo} / {divisor}"
        resposta = quociente

    else:
        a, b = _gerar_operandos(dificuldade)
        pergunta = f"{a} + {b}"
        resposta = a + b

    return pergunta, resposta, operador_real


# "BANCO" DE QUESTÕES EM MEMÓRIA
# Como o cálculo da resposta certa não pode ser confiado ao cliente (o usuário
# poderia inspecionar o JS e trapacear), guardamos a resposta correta no
# servidor, associada a um question_id, e só validamos contra esse cache.
QUESTOES_ATIVAS = {}
_proximo_id = 1


def _novo_question_id():
    global _proximo_id
    qid = _proximo_id
    _proximo_id += 1
    return qid


# ROTAS
@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route("/gerar-questao", methods=["POST"])
def rota_gerar_questao():
    """
    Body esperado (JSON):
        {
            "operador": "soma" | "subtracao" | "multiplicacao" | "divisao" | "misto",
            "dificuldade": "iniciante" | "intermediario" | "avancado"
        }

    Resposta (JSON):
        {
            "question_id": int,
            "pergunta": "45 + 9",
            "operador_aplicado": "soma"
        }
    """
    dados = request.get_json(silent=True) or {}
    operador = dados.get("operador", "soma")
    dificuldade = dados.get("dificuldade", "iniciante")

    pergunta, resposta, operador_real = gerar_questao(operador, dificuldade)

    qid = _novo_question_id()
    QUESTOES_ATIVAS[qid] = resposta

    # evita que o cache cresça indefinidamente numa sessão longa
    if len(QUESTOES_ATIVAS) > 500:
        chaves_antigas = sorted(QUESTOES_ATIVAS.keys())[:250]
        for k in chaves_antigas:
            QUESTOES_ATIVAS.pop(k, None)

    return jsonify(
        {
            "question_id": qid,
            "pergunta": pergunta,
            "operador_aplicado": operador_real,
        }
    )


@app.route("/validar-resposta", methods=["POST"])
def rota_validar_resposta():
    """
    Body esperado (JSON):
        {
            "question_id": int,
            "resposta_usuario": number,
            "acertos_rodada": int,    # opcional, para personalizar a frase
            "total_rodada": int       # opcional
        }

    Resposta (JSON):
        {
            "correta": bool,
            "resposta_certa": number,
            "frase": "Isso aí, atleta! Reflexo de campeão."
        }
    """
    dados = request.get_json(silent=True) or {}
    qid = dados.get("question_id")
    resposta_usuario = dados.get("resposta_usuario", None)
    acertos_rodada = dados.get("acertos_rodada", 0)
    total_rodada = dados.get("total_rodada", 0)

    resposta_certa = QUESTOES_ATIVAS.get(qid)

    if resposta_certa is None:
        return jsonify(
            {
                "correta": False,
                "resposta_certa": None,
                "frase": "Essa questão expirou. Vamos para a próxima!",
                "erro": "question_id desconhecido ou expirado",
            }
        ), 200

    try:
        resposta_usuario_num = float(resposta_usuario)
        correta = resposta_usuario_num == float(resposta_certa)
    except (TypeError, ValueError):
        correta = False

    # taxa de acerto até agora na rodada, para escolher o tom da frase
    taxa = (acertos_rodada / total_rodada) if total_rodada else None

    if correta:
        frase = random.choice(FRASES_ACERTO)
        if taxa is not None and taxa >= 0.8:
            frase = "Sequência impecável! Você está em ritmo de pódio."
    else:
        frase = random.choice(FRASES_ERRO)
        if taxa is not None and taxa <= 0.3 and total_rodada >= 3:
            frase = "Desacelera um pouco e confere a conta com calma."

    # questão já respondida: remove do cache para não permitir reenvio
    QUESTOES_ATIVAS.pop(qid, None)

    return jsonify(
        {
            "correta": correta,
            "resposta_certa": resposta_certa,
            "frase": frase,
        }
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
