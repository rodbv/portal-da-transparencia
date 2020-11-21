# Checador de diários oficiais do Portal da Transparência

Esse crawler é relacionado ao projeto [Querido Diário](https://github.com/okfn-brasil/querido-diario), [issue 353](https://github.com/okfn-brasil/querido-diario/issues/353), e checa quais das cidades disponíveis na plataforma têm diários oficiais ativos: http://atmtec.org.br/#publicacao

Quando for rodar esse crawler o mais importante é checar a variável `MATCH_CRITERIA` em `city_checker_spider.py`, que é como é determinado se os diários oficiais publicados na cidade são recentes.

No momento em que esse checador foi escrito, estamos em Novembro de 2020, por isso `MATCH_CRITERIA` foi setado para `Novembro/2020` pois isso que se espera encontrar na página, por exemplo na cidade de [Areal/RJ](http://rj.portaldatransparencia.com.br/prefeitura/areal/)

Se você quiser fazer alguma alteração e testar rapidamente, use o arquivo `territories_short.csv`, basta trocar o nome do arquivo no spider.

### Resultados

No diretório `data` são salvos os arquivos `result.csv` com as cidades cujas páginas retornaram diários oficiais recentes, bem como um arquivo html para cada cidade da lista para conferência (em especial dado o problema de concorrência descrito na seção a seguir).

### Nota sobre concorrência:

No arquivo `settings.py` foi colocado `CONCURRENT_REQUESTS = 3` pois o servidor mostrou não lidar bem com muitas requisições concorrentes, algumas páginas vieram com parte do conteúdo de uma cidade (scripts, assets) e conteúdo de outras.
