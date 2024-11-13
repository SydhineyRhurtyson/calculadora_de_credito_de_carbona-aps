function calcularCarbono() {
    const dados = {
        distancia_km: document.getElementById("distanciaKm").value,
        tipo_transporte: document.getElementById("tipoTransporte").value,
        // voos_domesticos: document.getElementById("voosDomesticos").value,
        // voos_internacionais: document.getElementById("voosInternacionais").value,
        consumo_kwh: document.getElementById("consumoKwh").value,
        consumo_gas: document.getElementById("consumoGas").value,
        // dieta: document.getElementById("dieta").value,
        quantidade_residuos: document.getElementById("quantidadeResiduos").value,
        arvores_plantadas: document.getElementById("arvoresPlantadas").value,
        energia_renovavel: document.getElementById("energiaRenovavel").value
    };

    fetch('/calcular', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dados)
    })
    .then(response => response.json())
    .then(resultado => {
        document.getElementById("resultado").innerHTML = `
            <h3>Resultados</h3>
            <p>Emissão total: ${resultado.emissao_total} kg de CO₂</p>
            <p>Créditos de carbono: ${resultado.credito_total} kg de CO₂</p>
            <p>Emissão líquida: ${resultado.emissao_liquida} kg de CO₂</p>
            <p>Árvores necessárias para compensação: ${resultado.arvores_necessarias}</p>
            <p>Custo para compensação: R$ ${resultado.custo_compensacao_real}</p>
        `;

        const dicasContainer = document.getElementById("dicas");
        dicasContainer.innerHTML = "<h3>Dicas para Reduzir Emissões</h3>";
        resultado.dicas.forEach(dica => {
            dicasContainer.innerHTML += `<p>${dica}</p>`;
        });
    })
    .catch(error => {
        console.error('Erro:', error);
        document.getElementById("resultado").innerHTML = "<p>Erro ao calcular emissões. Tente novamente mais tarde.</p>";
    });
}
