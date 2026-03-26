## ADDED Requirements

### Requirement: Fluxo de login quando autenticação obrigatória

Quando o backend indicar que a autenticação é obrigatória (por exemplo via endpoint público de configuração), a interface DEVE apresentar uma **tela de login** antes do assistente de merge de PDFs. A tela DEVE coletar credenciais compatíveis com o provedor ativo (para LDAP: identificador de usuário e senha), DEVE exibir mensagens de erro claras em português em caso de falha e DEVE permitir tentar novamente. Após autenticação bem-sucedida, a interface DEVE prosseguir para o fluxo principal existente e DEVE incluir a sessão (cookie ou header, conforme implementação) em todas as chamadas à API da ferramenta.

#### Scenario: Usuário não autenticado vê apenas login

- **WHEN** a autenticação está obrigatória e o usuário ainda não possui sessão válida
- **THEN** a interface exibe a tela de login e não exibe o assistente de PDFs até que o login seja bem-sucedido

#### Scenario: Sessão válida acessa o assistente

- **WHEN** o usuário conclui o login com sucesso
- **THEN** a interface apresenta o assistente de merge como hoje, com chamadas autenticadas à API

#### Scenario: Falha de login

- **WHEN** o servidor rejeita as credenciais
- **THEN** a interface mantém o usuário na tela de login e exibe feedback de erro sem vazar detalhes internos do servidor
