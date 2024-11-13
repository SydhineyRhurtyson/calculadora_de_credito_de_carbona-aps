from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def calcular_emissoes(dados):
    # Extrair os dados do formulário
    distancia_km = float(dados.get("distancia_km", 0))
    tipo_transporte = dados.get("tipo_transporte", "carro")
    # voos_domesticos = int(dados.get("voos_domesticos", 0))
    # voos_internacionais = int(dados.get("voos_internacionais", 0))
    consumo_kwh = float(dados.get("consumo_kwh", 0))
    consumo_gas = float(dados.get("consumo_gas", 0))
    # dieta = dados.get("dieta", "vegana")
    quantidade_residuos = float(dados.get("quantidade_residuos", 0))
    arvores_plantadas = int(dados.get("arvores_plantadas", 0))
    energia_renovavel = float(dados.get("energia_renovavel", 0))

    # Fatores de emissão
    fatores_emissao_transporte = {"carro": 0.19, "moto": 0.0711, "onibus": 0.0160,"metro":0.0035,"bicicleta": 0, "a pe": 0}
    # fator_emissao_voo_domestico = 110.0
    # fator_emissao_voo_internacional = 300
    fator_emissao_energia = 0.0385
    fator_emissao_gas = 0.048
    # fatores_emissao_dieta = {"vegana": 1500, "vegetariana": 2000, "pouca carne": 2500, "muita carne": 3300}
    fator_emissao_residuos = 52.0

    # Cálculos das emissões
    emissao_transporte = distancia_km * 12 * fatores_emissao_transporte.get(tipo_transporte, 0)
    # emissao_voo = (voos_domesticos * fator_emissao_voo_domestico) + (voos_internacionais * fator_emissao_voo_internacional)
    emissao_energia = consumo_kwh * 12 * fator_emissao_energia
    emissao_gas = consumo_gas * 12 * fator_emissao_gas
    # emissao_alimentacao = fatores_emissao_dieta.get(dieta, 0)
    emissao_residuos = quantidade_residuos * 12 * fator_emissao_residuos

    # emissao_total = emissao_transporte + emissao_voo + emissao_energia + emissao_gas + emissao_alimentacao + emissao_residuos
    emissao_total = emissao_transporte  + emissao_energia + emissao_gas  + emissao_residuos

    # Cálculo dos créditos de carbono
    fator_sequestro_arvore = 20  # kg de CO₂ por árvore por ano
    fator_energia_renovavel = 0.085  # kg de CO₂ evitado por kWh de energia renovável

    credito_arvores = arvores_plantadas * fator_sequestro_arvore
    credito_energia_renovavel = energia_renovavel * fator_energia_renovavel

    credito_total = credito_arvores + credito_energia_renovavel

    # Emissão líquida considerando os créditos de carbono
    emissao_liquida = emissao_total - credito_total

    # Cálculo do número de árvores necessárias para compensação
    arvores_necessarias = max(0, emissao_liquida / fator_sequestro_arvore)

    # Cálculo do custo em reais para compensação
    preco_credito_por_tonelada = 20  # valor em dólares por tonelada de CO₂
    taxa_cambio = 5.00  # taxa de câmbio do dólar para real
    custo_compensacao_real = max(0, (emissao_liquida / 1000) * preco_credito_por_tonelada * taxa_cambio)

    # Dicas baseadas nas emissões
    dicas = [
        "Informação: Cada árvore plantada pode sequestrar cerca de 20 kg de CO₂ por ano.",
        "Informação: Cada kWh de energia renovável evita aproximadamente 0,085 kg de CO₂."
    ]
    if emissao_transporte > 1000:
        dicas.append("Considere usar transporte coletivo, bicicleta ou andar mais.")
    # if emissao_voo > 500:
    #     dicas.append("Reduza o número de voos, especialmente internacionais.")
    if emissao_energia > 1000:
        dicas.append("Economize energia em casa e considere instalar painéis solares.")
    if emissao_gas > 500:
        dicas.append("Reduza o consumo de gás usando aquecimento eficiente.")
    # if emissao_alimentacao > 2000:
    #     dicas.append("Reduza o consumo de carne e produtos de origem animal.")
    # if emissao_residuos > 600:
    #     dicas.append("Reduza, reutilize e recicle para diminuir a geração de lixo.")

    return {
        "emissao_total": round(emissao_total, 2),
        "credito_total": round(credito_total, 2),
        "emissao_liquida": round(emissao_liquida, 2),
        "arvores_necessarias": round(arvores_necessarias),
        "custo_compensacao_real": round(custo_compensacao_real, 2),
        "dicas": dicas
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calcular', methods=['POST'])
def calcular():
    dados = request.json
    resultado = calcular_emissoes(dados)
    return jsonify(resultado)

# Nova rota para "Como Funciona"
@app.route('/como-funciona')
def como_funciona():
    return render_template('comofunciona.html')

if __name__ == '__main__':
    app.run(debug=True)
