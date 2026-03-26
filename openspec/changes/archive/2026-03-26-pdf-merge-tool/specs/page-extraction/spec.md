## ADDED Requirements

### Requirement: Extração de páginas por número
O sistema DEVE extrair páginas específicas de um PDF informando números individuais. A numeração para o usuário começa em 1 (internamente convertida para índice 0).

#### Scenario: Extrair páginas 1 e 3 de um PDF de 5 páginas
- **WHEN** o usuário configura a extração das páginas "1,3" de um PDF com 5 páginas
- **THEN** o sistema extrai exatamente as páginas 1 e 3 na ordem informada

#### Scenario: Página inexistente
- **WHEN** o usuário solicita a página 10 de um PDF com 5 páginas
- **THEN** o sistema retorna erro 422 com mensagem "Página 10 não existe. O documento possui 5 páginas."

### Requirement: Extração de páginas por intervalo
O sistema DEVE aceitar intervalos no formato "X-Y" (ex: "1-3" = páginas 1, 2, 3).

#### Scenario: Extrair intervalo válido
- **WHEN** o usuário configura a extração das páginas "2-4" de um PDF com 6 páginas
- **THEN** o sistema extrai as páginas 2, 3 e 4 nessa ordem

#### Scenario: Intervalo invertido
- **WHEN** o usuário configura "5-2"
- **THEN** o sistema retorna erro 422 com mensagem "Intervalo inválido: o início deve ser menor ou igual ao fim"

### Requirement: Extração por lista combinada
O sistema DEVE aceitar combinação de números e intervalos separados por vírgula (ex: "1,3-5,7").

#### Scenario: Lista combinada válida
- **WHEN** o usuário configura "1,3-5,8" de um PDF com 10 páginas
- **THEN** o sistema extrai as páginas 1, 3, 4, 5, 8 nessa ordem

#### Scenario: Lista com duplicatas
- **WHEN** o usuário configura "1,1,2-3,2"
- **THEN** o sistema remove duplicatas e extrai as páginas 1, 2, 3 (sem repetição, ordem crescente)

### Requirement: Configuração padrão de páginas
O sistema DEVE usar páginas 1 e 2 como padrão quando nenhuma configuração for especificada pelo usuário.

#### Scenario: Nenhuma configuração de páginas fornecida
- **WHEN** o usuário não especifica quais páginas extrair de um PDF com 5 páginas
- **THEN** o sistema extrai as páginas 1 e 2

#### Scenario: PDF com apenas 1 página sem configuração
- **WHEN** o usuário não especifica páginas para um PDF com 1 página
- **THEN** o sistema extrai apenas a página 1 (ignora a página 2 que não existe)

### Requirement: Configuração individual por arquivo
O sistema DEVE permitir configuração de páginas diferente para cada arquivo no conjunto.

#### Scenario: Configuração individual
- **WHEN** o usuário configura "1-3" para o arquivo A e "1" para o arquivo B
- **THEN** o sistema extrai 3 páginas de A e 1 página de B, respeitando cada configuração
