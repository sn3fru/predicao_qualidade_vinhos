# Projeto para Estudo e Predição sobre qualidade de Vinhos

**Resumo**
Esse desafio enviado pela consultoria cognitivo.ai faz parte do processo seletivo para consultor em ciência de dados. Neste desafio era solicitado criar uma análise sobre dados fisico-quimicos de vinhos assim como uma nota de qualidade dada por profissionais e fazer um estudo como essas variáveis afetam as notas dos vinhos. Após o estudo foi criado um modelo preditivo que ao inserir as mesmas variáveis é retornado a nota esperada, além disso, foi construído uma API para tornar fácil sua consulta.



### Resolução
1. Faça uma análise exploratória para avaliar a consistência dos dados e identificar
possíveis variáveis que impactam na qualidade do vinho.

- Análise completa disponível no notebook "**main.ipynb**"

Resumo da análise:
Inicialmente foi tratado diversos valores que pareciam estar com a escala errada em diversas variáveis.
Após todos essas sanitizações e a análise das correlações lineares, rodamos um primeiro modelo de regressão linear para usarmos de benchmark e analisarmos os betas e suas confianças, abaixo um resumo do output:

![OLS](https://i.ibb.co/YkkcZBt/ols.png)

Como temos dois tipos de vinhos bem diferentes, tinto e branco, e suas variáveis explicativas interagem de forma bastante diferente, testamos um modelo de decision tree para entender se seria melhor que uma modelo linear que teriamos que passar explicitamente o relacionamento das variáveis para que fosse capturado essas interações. Ao rodar tivemos métricas razoavelmente melhores indicando que ou os dados não tinham um cortamento linear ou a interação das variáveis realmente faz diferença, abaixo a representação da arvore de decisão gerada:

![decision-tree](https://i.ibb.co/vsSdbJQ/decision-tree.png)

Após esse teste, rodamos diversos modelos baseado em árvores, inclusive com métodos de ensamble entre diferentes modelos (utilizando mlens) e o melhor modelo, após parametrizado utilizando grid search, foi um gradiente impulsionado por boosting (xgboost). Como ele tem a enorme desvantagem de ser um algoritmo de "caixa-preta", ou seja, embora produza boas métricas não sabemos bem como ele chegou nesses resultados, dado sua complexidade interna. Para contornar essa deficiência utilizamos uma técnica de Teoria dos Jogos para computar os impactos médios dessas variáveis utilizando o pacote shap, e abaixo temos um resumo das principais variáveis e seus efeitos na qualidade:

![Shap](https://i.ibb.co/brD3W43/2018-12-01-23-14-34.png)

O último passo foi disponibilizar o modelo treinado como um serviço em API disponível no arquivo **webservice.py**.

2. Para a realização deste teste você pode utilizar o software de sua preferência (Python
ou R), só pedimos que compartilhe conosco o código fonte (utilizando um repositório git). Além disso, inclua um arquivo README.md onde você deve cobrir as respostas para os 5 pontos abaixo:

    **a. Como foi a definição da sua estratégia de modelagem?**
    Foi usado diferentes algoritmos, começando com os mais simples como modelos paraetricos até os algoritmos de ensambles entre diferentes parametrizações de arvores aleatórias impulsionadas por boosting e comparando os resultados.


    **b. Como foi definida a função de custo utilizada?**
    1) Foi testado, R2, MAE e RMSE como métricas para minimizar a função de custo. A métrica escolhida foi o RMSE pela facilidade de interpretação já que a escala é a mesma da variável dependente.


    **c. Qual foi o critério utilizado na seleção do modelo final?**
    1) O modelo final foi escolhido dentro todos que geravam as melhores métricas com cross-validation. A melhor métrica obtida foi um RMSE de ~.52

    **d. Qual foi o critério utilizado para validação do modelo? Por que escolheu utilizar**
    este método?
    1) Foi iniciado um split entre treino e validacao 80/20 e depois um cross-validation com cv=10

    **e. Quais evidências você possui de que seu modelo é suficientemente bom?**
    1) Comparando com diferentes benchmarks dos mais simples que tem fortes exigências como correlações lineares até os mais complexos como métodos de boosting, assim podemos usar os simples como comparativo dos mais complicados.
