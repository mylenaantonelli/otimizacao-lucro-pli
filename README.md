# Otimização do Mix de Serviços em um Salão de Beleza com Programação Linear Inteira (PLI)

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![PuLP](https://img.shields.io/badge/PuLP-1.6.0+-blue?style=flat)](https://coin-or.github.io/pulp/)
[![Solver](https://img.shields.io/badge/Solver-CBC%20Branch--and--Cut-orange?style=flat)](https://github.com/coin-or/Cbc)

Projeto de pesquisa aplicada em Pesquisa Operacional, desenvolvido como Trabalho de Conclusão de Curso (TCC), com foco na utilização da Programação Linear Inteira para maximizar o lucro líquido de um salão de beleza através da otimização do seu mix de serviços, considerando os limites de tempo das profissionais, a disponibilidade de materiais, a demanda pelos serviços e a quantidade inteira de atendimentos.

---

##  Contexto e Problema de Negócio

No segmento de salões de beleza, composto em grande parte por microempreendimentos e profissionais autônomos, o planejamento operacional e financeiro frequentemente é realizado com base no "achismo", trazendo desafios para a sustentabilidade do negócio diante de recursos limitados (tempo de equipe e insumos).

Nesse contexto, o objetivo deste trabalho foi propor um modelo de Programação Linear Inteira (PLI) para otimizar o mix de serviços de um salão de beleza, determinando a melhor distribuição dos serviços a serem realizados mensalmente, buscando aumentar o lucro do estabelecimento e considerando fatores como disponibilidade de horários das profissionais, estoque de produtos e demanda por cada serviço.

---

##  Modelagem Matemática (PLI)

O problema foi formulado como um modelo de **Programação Linear Inteira (PLI)**, formulado com conjuntos, variáveis de decisão inteiras, função objetivo de maximização e restrições operacionais lineares:

```
Maximizar Z = ∑ (k ∈ P) ∑ (i ∈ S_k) L_{i,k} * x_{i,k}

Sujeito a:
(1) Tempo:    ∑ (i ∈ S_k) T_i * x_{i,k} <= T_k,                    ∀ k ∈ P
(2) Estoque:  ∑ (k ∈ P) ∑ (i ∈ S_k) Q_{i,j} * x_{i,k} <= Estoque_j,  ∀ j ∈ M
(3) Demanda:  Dmin_{i,k} <= x_{i,k} <= Dmax_{i,k},                  ∀ k ∈ P, ∀ i ∈ S_k
(4) Domínio:  x_{i,k} ∈ ℤ⁺,                                         ∀ k ∈ P, ∀ i ∈ S_k
```

### Elementos da Formulação:
- **$P$**: Conjunto de profissionais da equipe ($k = 1, \dots, 5$).
- **$S_k$**: Subconjunto de serviços habilitados para a profissional $k$.
- **$M$**: Conjunto de materiais e insumos restritivos ($j = 1, \dots, 19$).
- **$x_{i,k}$**: Variável de decisão inteira representando a quantidade mensal de atendimentos do serviço $i$ realizados pela profissional $k$ (46 variáveis de decisão).
- **$L_{i,k}$**: Lucro líquido unitário do serviço $i$ quando realizado pela profissional $k$ (já deduzidos custos diretos e repasses de comissão).
- **$T_i$ e $T_k$**: Tempo médio de execução do serviço $i$ e carga horária máxima disponível da profissional $k$ (em minutos).
- **$Q_{i,j}$ e $\text{Estoque}_j$**: Coeficiente de consumo unitário e limite de estoque disponível do material $j$.
- **$Dmin_{i,k}$ e $Dmax_{i,k}$**: Piso de demanda mínima (fidelização) e teto de demanda máxima (mercado).

A resolução é realizada com o algoritmo exato **Branch-and-Cut** por meio do solver open-source **CBC (Coin-or branch and cut)** acoplado via biblioteca **PuLP** em Python.

> [NOTA]
> **Privacidade dos Dados Empresariais:** Para resguardar o sigilo comercial e financeiro do estabelecimento, os valores unitários de margem e lucro foram escalonados por um fator proporcional constante ($1.5\times$). Essa transformação preserva rigorosamente todas as decisões ótimas, o consumo de recursos e as folgas operacionais da modelagem matemática.

---

##  Resultados da Otimização e Cenários

A resolução do modelo base estabeleceu uma alocação ótima de 377 atendimentos mensais distribuídos entre a equipe, alcançando um resultado de R$ 30.760,22 de lucro líquido e revelando que o estoque de xampu atuou como a principal restrição limitante da capacidade produtiva capilar. No **Cenário 1**, ao ampliar a disponibilidade de xampu para 10.000 mL, o estabelecimento absorveu a demanda reprimida, saltando para 521 atendimentos (+144 serviços) e elevando o lucro mensal para R$ 38.209,80. No **Cenário 2**, a reestruturação de preços em procedimentos longos e de alto esforço (mechas, penteados e progressivas) gerou R$ 32.771,72 de retorno mantendo exatamente os mesmos 377 atendimentos do mix inicial, sem exigir esforço físico adicional da equipe. No **Cenário 3**, uma ação promocional de 20% para impulsionar a procura em manicure, pedicure, sobrancelha e limpeza de pele aumentou a produção para 405 atendimentos (+28 serviços) e o retorno financeiro para R$ 31.333,22, aproveitando horas ociosas dessas profissionais sem gerar gargalos de estoque.

---

##  Estrutura do Projeto

```bash
otimizacao-lucro-pli/
│
├── modelagem.py                       # Script principal: dados do problema, modelagem PLI e solução base
├── requirements.txt                   # Dependências do projeto e versões exatas
├── README.md                          # Apresentação do projeto, contextualização e instruções
│
└── analise_de_sensibilidade/
    ├── cenario1.py                    # Cenário 1: Expansão do estoque de xampu (+5.000 mL)
    ├── cenario2.py                    # Cenário 2: Reajuste estratégico de preços nos serviços longos
    └── cenario3.py                    # Cenário 3: Promoção e estímulo de demanda em manicure, pedicure e estética
```

---

##  Como Executar o Projeto

Siga os passos abaixo para configurar o ambiente e executar os modelos em sua máquina local.

### 1. Pré-requisitos
- **Python 3.9+** instalado ([download em python.org](https://www.python.org/downloads/)).
- Gerenciador de pacotes **pip** atualizado.

### 2. Clonar o Repositório
```bash
git clone https://github.com/SEU_USUARIO/otimizacao-lucro-pli.git
cd otimizacao-lucro-pli
```

### 3. Criar e Ativar um Ambiente Virtual (Recomendado)

- **Linux / macOS:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

- **Windows:**
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```

### 4. Instalar as Dependências
Instale a biblioteca de modelagem PuLP com o arquivo de requisitos:
```bash
pip install -r requirements.txt
```

### 5. Sobre o Solver CBC
O PuLP já inclui por padrão uma versão binária pré-compilada do solver **CBC (Coin-or branch and cut)**, funcionando nativamente sem necessidade de configurações adicionais na maioria dos sistemas.

Caso seu sistema operacional exija o executável nativo do CBC:
- **Ubuntu/Debian:** `sudo apt-get update && sudo apt-get install coinor-cbc`
- **macOS (via Homebrew):** `brew install cbc`
- **Windows / Outros:** O executável interno do PuLP é acionado automaticamente pelo comando `pulp.PULP_CBC_CMD()`.

### 6. Executar os Scripts de Otimização


> No **Linux / macOS** (especialmente ao rodar diretamente sem ambiente virtual), utilize o comando `python3`. No **Windows** ou com o ambiente virtual (`venv`) ativado, utilize `python`.

- **Modelo Base (Mix Inicial):**
  ```bash
  python3 modelagem.py
  # No Windows ou venv ativo: python modelagem.py
  ```

- **Cenário 1 (Aumento do Estoque de Xampu):**
  ```bash
  python3 analise_de_sensibilidade/cenario1.py
  # No Windows ou venv ativo: python analise_de_sensibilidade/cenario1.py
  ```

- **Cenário 2 (Reajuste de Preços):**
  ```bash
  python3 analise_de_sensibilidade/cenario2.py
  # No Windows ou venv ativo: python analise_de_sensibilidade/cenario2.py
  ```

- **Cenário 3 (Promoção e Estímulo de Demanda):**
  ```bash
  python3 analise_de_sensibilidade/cenario3.py
  # No Windows ou venv ativo: python analise_de_sensibilidade/cenario3.py
  ```

A saída no terminal exibirá:
1. Status da solução (`Optimal`);
2. Quantidade ideal recomendada de cada procedimento por profissional;
3. Lucro líquido mensal total ($Z$);
4. Ocupação da carga horária de cada colaboradora;
5. Folga (*slack*) restante de tempo e estoque de cada insumo.

---


##  Autora

**Mylena Antonelli Ferraz Netto**  
*Graduanda em Ciência da Computação*  

