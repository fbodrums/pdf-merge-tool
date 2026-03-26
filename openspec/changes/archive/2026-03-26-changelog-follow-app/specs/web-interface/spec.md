# web-interface (delta)

## ADDED Requirements

### Requirement: Ponto de entrada ao changelog no cabeçalho

A interface DEVE oferecer, na região do cabeçalho do shell, um controle dedicado (botão ou link com aparência de ação secundária) para abrir o changelog do produto, posicionado de forma consistente com o layout de largura máxima existente e visível em desktop e tablet. O controle DEVE usar componentes de `components/ui` (por exemplo `Button` com variante outline ou ghost) e possuir rótulo acessível (texto ou `aria-label`).

#### Scenario: Cabeçalho com ação secundária

- **WHEN** o usuário visualiza a tela principal da ferramenta
- **THEN** o cabeçalho exibe o título e a descrição existentes e, na mesma faixa, o controle para abrir o changelog sem obscurecer o fluxo principal de merge de PDFs

#### Scenario: Uso em viewport estreita

- **WHEN** o usuário acessa em largura reduzida (tablet ou janela estreita)
- **THEN** o controle permanece utilizável (sem sobreposição ilegível com o título; empilhamento ou quebra de linha aceitável conforme o design responsivo atual)
