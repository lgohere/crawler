#Crawler

Descrição Breve: Este projeto implementa um web crawler sofisticado e ético, capaz de extrair conteúdo de websites, processar o texto em chunks gerenciáveis e salvar os resultados em formato JSONL. O crawler inclui recursos avançados como rotação de User-Agents, tratamento de interrupções, e processamento de texto usando NLTK.

Linguagem: Python

Bibliotecas Principais:

- requests: Para fazer requisições HTTP.
- BeautifulSoup: Para parsing de HTML.
- nltk: Para processamento de linguagem natural e tokenização de sentenças.
- json: Para manipulação de dados JSON.
- signal: Para tratamento de sinais de interrupção.

Funcionalidades Principais:

1. Crawling de websites a partir de uma URL inicial.
2. Extração e limpeza de conteúdo HTML.
3. Processamento de texto em chunks de tamanho controlado.
4. Rotação de User-Agents para evitar bloqueios.
5. Tratamento de interrupções para salvar dados parciais.
6. Logging detalhado das operações.
7. Respeito a robots.txt implícito (pelo domínio).

Técnicas Aplicadas:

- Web scraping ético com delays aleatórios entre requisições.
- Processamento de linguagem natural para tokenização de sentenças.
- Manipulação avançada de strings e URLs.
- Tratamento de exceções para robustez.
- Uso de generators para processamento eficiente de grandes volumes de dados.
- Implementação de padrões de design orientado a objetos.

Demonstra habilidades em web scraping, processamento de texto, e desenvolvimento de software robusto em Python. É uma excelente ferramenta de coleta de dados que respeita as boas práticas de crawling web, incluindo considerações éticas e de eficiência.
