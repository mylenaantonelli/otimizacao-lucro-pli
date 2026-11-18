# Análise de sensibilidade - Cenário 3 - PROMOÇÃO DE 20% NOS SERVIÇOS DE MANICURE, PEDICURE, SOBRANCELHA E LIMPEZA DE PELE

import pulp


profissionais = [
    "Proprietaria_1", "Proprietaria_2", "Proprietaria_3", 
    "Colaboradora_1", "Colaboradora_2"
]

# Carga horária máxima mensal (T_k) em min
tempo_maximo = {
    "Proprietaria_1": 15840,
    "Proprietaria_2": 15840,
    "Proprietaria_3": 15840,
    "Colaboradora_1": 10560,
    "Colaboradora_2": 9240
}

# Subconjuntos de serviços que cada profissional realiza (S_k)
servicos_habilitados = {
    "Proprietaria_1": [
        "Escova", "Corte_Curto", "Corte_Medio_Longo", "Aplicacao_Coloracao",
        "Retoque_Coloracao", "Mechas_Curto", "Mechas_Medio_Longo", "Penteado"
    ],
    "Proprietaria_2": [
        "Cutilagem_Esmaltacao_Maos", "Cutilagem_Esmaltacao_Pes", "Limpeza_Pele",
        "Depilacao_Intima", "Depilacao_Rosto", "Depilacao_Axilas", "Sobrancelha"
    ],
    "Proprietaria_3": [
        "Escova", "Botox", "Progressiva_Pouco_Volume", "Progressiva_Volume_Medio",
        "Progressiva_Muito_Volume", "Cauterizacao", "Cutilagem_Esmaltacao_Pes",
        "Hidratacao_Sem_Escova", "Hidratacao_Com_Escova", "Retoque_Coloracao", "Relaxamento"
    ],
    "Colaboradora_1": [
        "Maquiagem", "Cutilagem_Esmaltacao_Maos", "Cutilagem_Esmaltacao_Pes",
        "Depilacao_Intima", "Depilacao_Axilas", "Depilacao_Buco", "Depilacao_Pernas",
        "Retoque_Coloracao_Sem_Escova", "Hidratacao_Sem_Escova"
    ],
    "Colaboradora_2": [
        "Escova", "Progressiva_Pouco_Volume", "Progressiva_Volume_Medio",
        "Progressiva_Muito_Volume", "Botox", "Cauterizacao", "Hidratacao_Com_Escova",
        "Hidratacao_Sem_Escova", "Escova_Com_Chapinha", "Aplicacao_Coloracao", "Retoque_Coloracao"
    ]
}

# Lucro Líquido unitário por profissional e serviço (L_{i,k})
# Valores ajustados proporcionalmente para preservação do sigilo dos dados comerciais reais
lucro = {
    # Proprietaria 1
    ("Proprietaria_1", "Escova"): 53.03, ("Proprietaria_1", "Corte_Curto"): 50.84, ("Proprietaria_1", "Corte_Medio_Longo"): 63.50,
    ("Proprietaria_1", "Aplicacao_Coloracao"): 124.77, ("Proprietaria_1", "Retoque_Coloracao"): 81.39, 
    ("Proprietaria_1", "Mechas_Curto"): 386.87, ("Proprietaria_1", "Mechas_Medio_Longo"): 456.95, ("Proprietaria_1", "Penteado"): 412.53,
    # Proprietaria 2
    ("Proprietaria_2", "Cutilagem_Esmaltacao_Maos"): (54 * 30.00 + 4 * 23.10) / 58, ("Proprietaria_2", "Cutilagem_Esmaltacao_Pes"): (30 * 30.00 + 4 * 23.10) / 34,
    ("Proprietaria_2", "Limpeza_Pele"): (2 * 57.00 + 4 * 43.50) / 6, ("Proprietaria_2", "Depilacao_Intima"): 42.00, ("Proprietaria_2", "Depilacao_Rosto"): 13.50,
    ("Proprietaria_2", "Depilacao_Axilas"): 18.75, ("Proprietaria_2", "Sobrancelha"): (7 * 36.75 + 4 * 29.25) / 11,
    # Proprietaria 3
    ("Proprietaria_3", "Escova"): 52.04, ("Proprietaria_3", "Botox"): 207.98, ("Proprietaria_3", "Progressiva_Pouco_Volume"): 214.35,
    ("Proprietaria_3", "Progressiva_Volume_Medio"): 237.60, ("Proprietaria_3", "Progressiva_Muito_Volume"): 258.77, 
    ("Proprietaria_3", "Cauterizacao"): 101.28, ("Proprietaria_3", "Cutilagem_Esmaltacao_Pes"): (8 * 30.00 + 4 * 23.10) / 12,
    ("Proprietaria_3", "Hidratacao_Sem_Escova"): 58.41, ("Proprietaria_3", "Hidratacao_Com_Escova"): 75.95,
    ("Proprietaria_3", "Retoque_Coloracao"): 81.39, ("Proprietaria_3", "Relaxamento"): 117.32,
    # Colaboradora 1
    ("Colaboradora_1", "Maquiagem"): 24.00, ("Colaboradora_1", "Cutilagem_Esmaltacao_Maos"): (23 * 7.50 + 4 * 0.60) / 27,
    ("Colaboradora_1", "Cutilagem_Esmaltacao_Pes"): (9 * 7.50 + 4 * 0.60) / 13, ("Colaboradora_1", "Depilacao_Intima"): 4.05,
    ("Colaboradora_1", "Depilacao_Axilas"): 2.10, ("Colaboradora_1", "Depilacao_Buco"): 1.50, ("Colaboradora_1", "Depilacao_Pernas"): 4.05,
    ("Colaboradora_1", "Retoque_Coloracao_Sem_Escova"): 28.50, ("Colaboradora_1", "Hidratacao_Sem_Escova"): 28.04,
    # Colaboradora 2
    ("Colaboradora_2", "Escova"): 16.04, ("Colaboradora_2", "Progressiva_Pouco_Volume"): 106.35,
    ("Colaboradora_2", "Progressiva_Volume_Medio"): 116.10, ("Colaboradora_2", "Progressiva_Muito_Volume"): 123.77,
    ("Colaboradora_2", "Botox"): 106.73, ("Colaboradora_2", "Cauterizacao"): 47.28, ("Colaboradora_2", "Hidratacao_Com_Escova"): 35.45,
    ("Colaboradora_2", "Hidratacao_Sem_Escova"): 28.04, ("Colaboradora_2", "Escova_Com_Chapinha"): 41.43,
    ("Colaboradora_2", "Aplicacao_Coloracao"): 43.77, ("Colaboradora_2", "Retoque_Coloracao"): 30.77
}

# Tempo médio de execução por profissional e serviço (T_i) em min
tempo_servico = {
    # Proprietaria 1
    ("Proprietaria_1", "Escova"): 45, ("Proprietaria_1", "Corte_Curto"): 30, ("Proprietaria_1", "Corte_Medio_Longo"): 60,
    ("Proprietaria_1", "Aplicacao_Coloracao"): 105, ("Proprietaria_1", "Retoque_Coloracao"): 90, 
    ("Proprietaria_1", "Mechas_Curto"): 300, ("Proprietaria_1", "Mechas_Medio_Longo"): 360, ("Proprietaria_1", "Penteado"): 120,
    # Proprietaria 2
    ("Proprietaria_2", "Cutilagem_Esmaltacao_Maos"): 60, ("Proprietaria_2", "Cutilagem_Esmaltacao_Pes"): 60,
    ("Proprietaria_2", "Limpeza_Pele"): 60, ("Proprietaria_2", "Depilacao_Intima"): 20, ("Proprietaria_2", "Depilacao_Rosto"): 15,
    ("Proprietaria_2", "Depilacao_Axilas"): 10, ("Proprietaria_2", "Sobrancelha"): 20,
    # Proprietaria 3
    ("Proprietaria_3", "Escova"): 60, ("Proprietaria_3", "Botox"): 240, ("Proprietaria_3", "Progressiva_Pouco_Volume"): 240,
    ("Proprietaria_3", "Progressiva_Volume_Medio"): 270, ("Proprietaria_3", "Progressiva_Muito_Volume"): 300,
    ("Proprietaria_3", "Cauterizacao"): 150, ("Proprietaria_3", "Cutilagem_Esmaltacao_Pes"): 60,
    ("Proprietaria_3", "Hidratacao_Sem_Escova"): 60, ("Proprietaria_3", "Hidratacao_Com_Escova"): 120,
    ("Proprietaria_3", "Retoque_Coloracao"): 90, ("Proprietaria_3", "Relaxamento"): 180,
    # Colaboradora 1
    ("Colaboradora_1", "Maquiagem"): 60, ("Colaboradora_1", "Cutilagem_Esmaltacao_Maos"): 60,
    ("Colaboradora_1", "Cutilagem_Esmaltacao_Pes"): 60, ("Colaboradora_1", "Depilacao_Intima"): 30,
    ("Colaboradora_1", "Depilacao_Axilas"): 15, ("Colaboradora_1", "Depilacao_Buco"): 10, ("Colaboradora_1", "Depilacao_Pernas"): 20,
    ("Colaboradora_1", "Retoque_Coloracao_Sem_Escova"): 65, ("Colaboradora_1", "Hidratacao_Sem_Escova"): 60,
    # Colaboradora 2
    ("Colaboradora_2", "Escova"): 60, ("Colaboradora_2", "Progressiva_Pouco_Volume"): 180,
    ("Colaboradora_2", "Progressiva_Volume_Medio"): 210, ("Colaboradora_2", "Progressiva_Muito_Volume"): 240,
    ("Colaboradora_2", "Botox"): 240, ("Colaboradora_2", "Cauterizacao"): 150, ("Colaboradora_2", "Hidratacao_Com_Escova"): 120,
    ("Colaboradora_2", "Hidratacao_Sem_Escova"): 60, ("Colaboradora_2", "Escova_Com_Chapinha"): 120,
    ("Colaboradora_2", "Aplicacao_Coloracao"): 105, ("Colaboradora_2", "Retoque_Coloracao"): 90
}

# Demandas mínimas (Dmin)
demanda_min = {
    # Prop 1
    ("Proprietaria_1", "Escova"): 6, ("Proprietaria_1", "Corte_Curto"): 13, ("Proprietaria_1", "Corte_Medio_Longo"): 12,
    ("Proprietaria_1", "Aplicacao_Coloracao"): 1, ("Proprietaria_1", "Retoque_Coloracao"): 15, ("Proprietaria_1", "Mechas_Curto"): 3,
    ("Proprietaria_1", "Mechas_Medio_Longo"): 1, ("Proprietaria_1", "Penteado"): 1,
    # Prop 2
    ("Proprietaria_2", "Cutilagem_Esmaltacao_Maos"): 41, ("Proprietaria_2", "Cutilagem_Esmaltacao_Pes"): 22,
    ("Proprietaria_2", "Limpeza_Pele"): 1, ("Proprietaria_2", "Depilacao_Intima"): 1, ("Proprietaria_2", "Depilacao_Rosto"): 1,
    ("Proprietaria_2", "Depilacao_Axilas"): 1, ("Proprietaria_2", "Sobrancelha"): 1,
    # Prop 3
    ("Proprietaria_3", "Escova"): 5, ("Proprietaria_3", "Botox"): 3, ("Proprietaria_3", "Progressiva_Pouco_Volume"): 7,
    ("Proprietaria_3", "Progressiva_Volume_Medio"): 3, ("Proprietaria_3", "Progressiva_Muito_Volume"): 2,
    ("Proprietaria_3", "Cauterizacao"): 3, ("Proprietaria_3", "Cutilagem_Esmaltacao_Pes"): 4,
    ("Proprietaria_3", "Hidratacao_Sem_Escova"): 1, ("Proprietaria_3", "Hidratacao_Com_Escova"): 1,
    ("Proprietaria_3", "Retoque_Coloracao"): 3, ("Proprietaria_3", "Relaxamento"): 1,
    # Colab 1
    ("Colaboradora_1", "Maquiagem"): 1, ("Colaboradora_1", "Cutilagem_Esmaltacao_Maos"): 12,
    ("Colaboradora_1", "Cutilagem_Esmaltacao_Pes"): 4, ("Colaboradora_1", "Depilacao_Intima"): 10,
    ("Colaboradora_1", "Depilacao_Axilas"): 4, ("Colaboradora_1", "Depilacao_Buco"): 1, ("Colaboradora_1", "Depilacao_Pernas"): 1,
    ("Colaboradora_1", "Retoque_Coloracao_Sem_Escova"): 1, ("Colaboradora_1", "Hidratacao_Sem_Escova"): 1,
    # Colab 2
    ("Colaboradora_2", "Escova"): 1, ("Colaboradora_2", "Progressiva_Pouco_Volume"): 1,
    ("Colaboradora_2", "Progressiva_Volume_Medio"): 3, ("Colaboradora_2", "Progressiva_Muito_Volume"): 1,
    ("Colaboradora_2", "Botox"): 1, ("Colaboradora_2", "Cauterizacao"): 1, ("Colaboradora_2", "Hidratacao_Com_Escova"): 1,
    ("Colaboradora_2", "Hidratacao_Sem_Escova"): 1, ("Colaboradora_2", "Escova_Com_Chapinha"): 1,
    ("Colaboradora_2", "Aplicacao_Coloracao"): 1, ("Colaboradora_2", "Retoque_Coloracao"): 3
}

# Demandas máximas (Dmax)
demanda_max = {
    # Prop 1
    ("Proprietaria_1", "Escova"): 19, ("Proprietaria_1", "Corte_Curto"): 37, ("Proprietaria_1", "Corte_Medio_Longo"): 52,
    ("Proprietaria_1", "Aplicacao_Coloracao"): 3, ("Proprietaria_1", "Retoque_Coloracao"): 37, ("Proprietaria_1", "Mechas_Curto"): 8,
    ("Proprietaria_1", "Mechas_Medio_Longo"): 4, ("Proprietaria_1", "Penteado"): 10,
    # Prop 2
    ("Proprietaria_2", "Cutilagem_Esmaltacao_Maos"): 58, ("Proprietaria_2", "Cutilagem_Esmaltacao_Pes"): 34,
    ("Proprietaria_2", "Limpeza_Pele"): 6, ("Proprietaria_2", "Depilacao_Intima"): 3, ("Proprietaria_2", "Depilacao_Rosto"): 2,
    ("Proprietaria_2", "Depilacao_Axilas"): 1, ("Proprietaria_2", "Sobrancelha"): 11,
    # Prop 3
    ("Proprietaria_3", "Escova"): 25, ("Proprietaria_3", "Botox"): 8, ("Proprietaria_3", "Progressiva_Pouco_Volume"): 12,
    ("Proprietaria_3", "Progressiva_Volume_Medio"): 10, ("Proprietaria_3", "Progressiva_Muito_Volume"): 6,
    ("Proprietaria_3", "Cauterizacao"): 7, ("Proprietaria_3", "Cutilagem_Esmaltacao_Pes"): 12,
    ("Proprietaria_3", "Hidratacao_Sem_Escova"): 4, ("Proprietaria_3", "Hidratacao_Com_Escova"): 2,
    ("Proprietaria_3", "Retoque_Coloracao"): 8, ("Proprietaria_3", "Relaxamento"): 1,
    # Colab 1
    ("Colaboradora_1", "Maquiagem"): 15, ("Colaboradora_1", "Cutilagem_Esmaltacao_Maos"): 27,
    ("Colaboradora_1", "Cutilagem_Esmaltacao_Pes"): 13, ("Colaboradora_1", "Depilacao_Intima"): 15,
    ("Colaboradora_1", "Depilacao_Axilas"): 10, ("Colaboradora_1", "Depilacao_Buco"): 4, ("Colaboradora_1", "Depilacao_Pernas"): 5,
    ("Colaboradora_1", "Retoque_Coloracao_Sem_Escova"): 9, ("Colaboradora_1", "Hidratacao_Sem_Escova"): 34,
    # Colab 2
    ("Colaboradora_2", "Escova"): 11, ("Colaboradora_2", "Progressiva_Pouco_Volume"): 5,
    ("Colaboradora_2", "Progressiva_Volume_Medio"): 10, ("Colaboradora_2", "Progressiva_Muito_Volume"): 7,
    ("Colaboradora_2", "Botox"): 1, ("Colaboradora_2", "Cauterizacao"): 2, ("Colaboradora_2", "Hidratacao_Com_Escova"): 2,
    ("Colaboradora_2", "Hidratacao_Sem_Escova"): 1, ("Colaboradora_2", "Escova_Com_Chapinha"): 2,
    ("Colaboradora_2", "Aplicacao_Coloracao"): 1, ("Colaboradora_2", "Retoque_Coloracao"): 5
}

# Limites mensais de materiais (M) limitantes
estoque = {
    "Shampoo_mL": 5000, "Condicionador_g": 3200, "Leavein_mL": 1000, "Mascara_g": 2000,
    "Coloracao_g": 2100, "Emulsao_mL": 7520, "Tonalizante_g": 720, "Po_Descolorante_g": 2000,
    "Fixador_mL": 400, "Cera_Modeladora_Liquida_mL": 250, "Cera_Modeladora_Bastao_g": 75, "Cera_Modeladora_Po_g": 10,
    "Botox_g": 3000, "Selante_g": 4000, "Queratina_g": 1000, "Creme_Pentear_ml": 1000, "Creme_Relaxante_g": 450,
    "Neutralizante_ml": 500, "Kit_Limpeza_Pele_unidades": 40,
}

# Consumo unitário de material por serviço (Q_{i,j})
consumo = {
    "Shampoo_mL": {"Escova": 30, "Corte_Curto": 15, "Corte_Medio_Longo": 30, "Aplicacao_Coloracao": 30, "Retoque_Coloracao": 30, "Mechas_Curto": 20, "Mechas_Medio_Longo": 20, "Penteado": 30, "Botox": 30, "Progressiva_Pouco_Volume": 30, "Progressiva_Volume_Medio": 30, "Progressiva_Muito_Volume": 30, "Cauterizacao": 30, "Hidratacao_Sem_Escova": 30, "Hidratacao_Com_Escova": 30, "Relaxamento": 30, "Retoque_Coloracao_Sem_Escova": 30, "Escova_Com_Chapinha": 30},
    "Condicionador_g": {"Escova": 15, "Corte_Curto": 7.5, "Corte_Medio_Longo": 15, "Aplicacao_Coloracao": 15, "Retoque_Coloracao": 15, "Penteado": 15, "Retoque_Coloracao_Sem_Escova": 15, "Escova_Com_Chapinha": 15},
    "Leavein_mL": {"Escova": 2, "Corte_Medio_Longo": 2, "Aplicacao_Coloracao": 2, "Retoque_Coloracao": 2, "Mechas_Curto": 2, "Mechas_Medio_Longo": 2, "Penteado": 2, "Cauterizacao": 2, "Retoque_Coloracao_Sem_Escova": 2, "Escova_Com_Chapinha": 2},
    "Mascara_g": {"Mechas_Curto": 30, "Mechas_Medio_Longo": 30, "Hidratacao_Com_Escova": 30, "Hidratacao_Sem_Escova": 30, "Cauterizacao": 30, "Relaxamento": 30},
    "Coloracao_g": {"Aplicacao_Coloracao": 60, "Retoque_Coloracao": 30},
    "Emulsao_mL": {"Aplicacao_Coloracao": 83.3, "Retoque_Coloracao": 41.67, "Mechas_Curto": 148.15, "Mechas_Medio_Longo": 389.33},
    "Tonalizante_g": {"Mechas_Curto": 20, "Mechas_Medio_Longo": 30},
    "Po_Descolorante_g": {"Mechas_Curto": 40, "Mechas_Medio_Longo": 120},
    "Fixador_mL": {"Penteado": 20},
    "Cera_Modeladora_Liquida_mL": {"Penteado": 5},
    "Cera_Modeladora_Bastao_g": {"Penteado": 0.75},
    "Cera_Modeladora_Po_g": {"Penteado": 0.05},
    "Botox_g": {"Botox": 40}, 
    "Selante_g": {
        "Progressiva_Pouco_Volume": 45,
        "Progressiva_Volume_Medio": 60,
        "Progressiva_Muito_Volume": 80,
    }, 
    "Queratina_g": {"Cauterizacao": 20},
    "Creme_Pentear_ml": {"Hidratacao_Com_Escova": 30, "Hidratacao_Sem_Escova": 30},
    "Creme_Relaxante_g": {"Relaxamento": 100},
    "Neutralizante_ml": {"Relaxamento": 80},
    "Kit_Limpeza_Pele_unidades": {"Limpeza_Pele": 1},
}




modelo = pulp.LpProblem("Otimizacao_Mix_Servicos_Salao", pulp.LpMaximize)

x = {}
for k in profissionais:
    for i in servicos_habilitados[k]:
        x[(i, k)] = pulp.LpVariable(f"x_{i}_{k}", lowBound=0, cat='Integer')




# Função Objetivo
modelo += pulp.lpSum([lucro[(k, i)] * x[(i, k)] for k in profissionais for i in servicos_habilitados[k]]), "Maximizar_Lucro_Mensal"

# Restrições de Tempo (k, i)
for k in profissionais:
    modelo += pulp.lpSum([tempo_servico[(k, i)] * x[(i, k)] for i in servicos_habilitados[k]]) <= tempo_maximo[k], f"Tempo_Maximo_{k}"

# Restrições de Estoque (com .get(i, 0) para serviços não tabelados no consumo)
for j in estoque.keys():
    modelo += pulp.lpSum([consumo[j].get(i, 0) * x[(i, k)] for k in profissionais for i in servicos_habilitados[k]]) <= estoque[j], f"Estoque_{j}"

# Restrições de Demanda
for k in profissionais:
    for i in servicos_habilitados[k]:
        modelo += x[(i, k)] >= demanda_min[(k, i)], f"Demanda_Min_{i}_{k}"
        modelo += x[(i, k)] <= demanda_max[(k, i)], f"Demanda_Max_{i}_{k}"



modelo.solve()


print("RESULTADOS DA OTIMIZAÇÃO")
print(f"Status da Solução: {pulp.LpStatus[modelo.status]}\n")

print("Quantidade ideal de serviços por mês:")
for k in profissionais:
    print(f"\n>> {k.replace('_', ' ')}:")
    for i in servicos_habilitados[k]:
        qtde = int(x[(i, k)].varValue)
        print(f"  {i}: {qtde} atendimentos")

lucro_maximo = pulp.value(modelo.objective)
print(f"\nLucro Máximo Mensal (Z): R$ {lucro_maximo:.2f}")

print("\nChecagem de Tempo:")
for k in profissionais:
    tempo_gasto = sum([tempo_servico[(k, i)] * x[(i, k)].varValue for i in servicos_habilitados[k]])
    print(f"  {k.replace('_', ' ')}: {int(tempo_gasto)} min ocupados de {tempo_maximo[k]} min disponíveis")


print("\nCONSUMO DOS RECURSOS (TEMPO E ESTOQUE)")
for nome, restricao in modelo.constraints.items():
    if not nome.startswith("Demanda"):
        print(f"- {nome}: folga de {restricao.slack:.2f}")
