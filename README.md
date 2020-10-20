# recommender_system
Recomendador de vídeos de ciência de dados<br>
Link da aplicação hospedada no Heroku: https://recommender-videos-ds.herokuapp.com/

Esta aplicação faz um ranqueamento de vídeos do Youtube baseado nas minhas preferências do que estou interessado no momento sobre ciência de dados e machine learning.

## Etapas do processo
1. Coleta de dados
Os dados foram coletados do site do Youtube através de ferraments de web scrapping. As duas bibliotecas python usadas para  essa tarefa foram **requests-html** e **BeautifulSoup**.<br>
Foram extraídos das páginas dos vídeos informações como: o título, quantidade de vizualizações e data de publicação.<br>
A rotulação foi feita manualmente olhando para o título de cada vídeo e decidindo se era algo que eu consideraria interessante assistir.

2. Processamento dos dados
Nessa etapa foi necessário criar os atributos que seriam usados como entrada em um modelo de aprendizado de máquina.<br>
As variáveis criadas foram: a quantidade de visualização de cada vídeo, a média de visualizações por dia e o título do vídeo. Para o título, foi usado o método **tf-idf** para converter as palavras em valores numéricos que o algoritmo pudesse reconhecer.<br>
A manipulação dos dados foi feita com a biblioteca **pandas** do python.

3. Modelagem
Vários algoritmos foram testados frente aos dados. O algoritmo que obteve melhor performance e foi escolhido para ir à produção foi o **RandomForest**.<br>
As métricas de validação analisadas foram **average_precision_score** e **roc_auc_score**, ambas encontradas na biblioteca **sklearn**.

4. Validação
Os dados foram separados entre "passado" e "futuro". Os dados representando o passado foram usados para o treinemanto dos algoritmos e os do futuros foram usados para validar o resultado dos modelos, simulando a situação em produção.

5. Implementação
A implementação foi feita com auxílio da biblioteca **Flask** e a aplicação final foi hospedad no **Heroku**.
