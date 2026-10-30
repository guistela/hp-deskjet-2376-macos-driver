# HP DeskJet 2376 no macOS — driver de impressão local

**Impressão por USB confirmada pelo proprietário em uma HP DeskJet Ink Advantage
2376, MacBook Pro Intel e macOS 26.6.2, em 30/10/2026.**

Driver comunitário, sem vínculo ou suporte oficial da HP. O executável foi
compilado localmente a partir de fontes HPLIP assinados pela HP. Não usamos o
executável pré-compilado do projeto que inspirou esta solução.

**Este download é somente para Mac Intel (x86_64), macOS 26.** Não testado em
Apple Silicon, outras versões de macOS ou outros modelos de impressora.
O pacote não instala scanner nem atualiza firmware.

English instructions: [README.en.md](README.en.md).

## Por que foi necessário

A impressora era reconhecida por USB como `HP DeskJet 2300 series`, mas estava
configurada com `Generic PCL Laser Printer` e nunca havia imprimido neste Mac.
Ao tentar trocar o driver, o HP Easy Start recebeu `NOT SUPPORTED` do catálogo
HP para esse modelo/macOS e terminou com `Found 0 available PPDs`.
Isso descreve o diagnóstico deste caso; não significa que todos os produtos HP
ou todos os métodos oficiais de instalação falhem.

## Instalar

Mantenha a impressora ligada, conectada por USB e com papel. Baixe este
repositório pelo botão **Code → Download ZIP**, extraia e abra o Terminal na pasta.
Alternativamente:

```bash
git clone https://github.com/guistela/hp-deskjet-2376-macos-driver.git
cd hp-deskjet-2376-macos-driver
```

Confira os arquivos antes de instalar:

```bash
(cd dist && shasum -a 256 -c install.sha256)
cat scripts/install.sh
bash scripts/install.sh
```

Execute em um **Terminal interativo**: o macOS pedirá a senha de administrador.
Não execute com `curl | sh`. A instalação envia **uma página de teste** com quatro
retângulos coloridos. Selecione **HP DeskJet 2376 (driver local)** ao imprimir.
Confirme que a página saiu: uma fila vazia, sozinha, não comprova impressão.

### O que o instalador altera

- Instala `hpcups` e o PPD em `/Library/Printers/hplip-local/`, pertencentes ao root.
- Cria/atualiza somente a fila `HP_DeskJet_2376_Local`, com papel A4 e sem compartilhamento.
- Preserva outras filas, a impressora padrão e as configurações de segurança.
- Verifica SHA-256 e a assinatura ad hoc antes de instalar.
- Não remove quarentena, não instala serviços em segundo plano e não inclui o scanner.
- Não baixa outros componentes durante a instalação.

O script usa a URI USB detectada naquele Mac; nenhum número de série está fixado.
Se houver mais de uma DeskJet 2300 conectada, deixe somente a desejada conectada.

## Transparência e segurança

Veja [docs/SECURITY-REVIEW.md](docs/SECURITY-REVIEW.md) para escopo e limitações.
**Não é um pacote certificado como livre de malware.** A assinatura ad hoc do
executável não identifica desenvolvedor certificado e não equivale a notarização
da Apple. Os checksums detectam alteração em relação ao manifesto distribuído;
não autenticam o mantenedor se o repositório inteiro for comprometido.

A assinatura OpenPGP autentica o arquivo de fontes HPLIP, não a adaptação macOS,
o compilador, o libjpeg local ou este instalador. O fonte exato, a assinatura e a
chave pública estão em `sources/`. O scanner do projeto inspirador foi excluído
após uma revisão que encontrou interpolação insegura de nomes de arquivo em shell.
Isso é uma falha de código, não evidência de intenção maliciosa do autor.

## Compilar você mesmo

Não usa os executáveis do projeto inspirador. Requer Mac Intel, Xcode Command
Line Tools, Python 3, GnuPG e libjpeg-turbo Intel. O build usa os cabeçalhos CUPS
do SDK do macOS e a biblioteca JPEG estática já instalada pelo Homebrew.

```bash
brew install gnupg jpeg-turbo
python3 scripts/build.py
bash scripts/test.sh
```

O build verifica a assinatura HP em um chaveiro temporário isolado, compila os
50 arquivos C/C++ do filtro e gera um PPD a partir do arquivo HPLIP. A única
adaptação adicionada ao fonte é um cabeçalho `malloc.h` que inclui `stdlib.h`.
As flags incluem `APDK_LITTLE_ENDIAN` e `DISABLE_IMAGEPROCESSOR`; o build não usa
plugins proprietários. Veja `scripts/build.py` e `docs/BUILD-ENVIRONMENT.txt`.

Não prometemos reprodução byte a byte: SDK, compilador e versão do libjpeg podem
alterar o binário. Os fontes HPLIP estão fixados em 3.25.2 para reproduzir o caso
testado; isso não afirma que seja a versão mais recente ou sem vulnerabilidades.

## Remover

```bash
bash scripts/uninstall.sh
```

Remove somente a fila e a pasta de driver criadas por este pacote. Não cancela
trabalhos de outras impressoras nem redefine o sistema de impressão inteiro.

## Problemas e relatos

```bash
lpstat -p HP_DeskJet_2376_Local -v HP_DeskJet_2376_Local
lpstat -W not-completed -o HP_DeskJet_2376_Local
```

Se aparecer `sudo: a terminal is required`, execute no Terminal do macOS.
Os avisos do PPD sobre nomes de papel e a descontinuação futura dos drivers
clássicos CUPS apareceram no teste bem-sucedido e não impediram a impressão.
Falhas de instalação ou de filtro precisam ser investigadas separadamente.

Ao abrir uma issue, informe modelo, arquitetura, versão do macOS, mensagem de
erro e se a folha realmente saiu. Remova número de série, nome de usuário e
dados dos documentos. Até esta publicação, a confirmação física é de **um caso**.
Não há alegação de validação independente ampla.

## Créditos e licenças

- [HP HPLIP](https://developers.hp.com/hp-linux-imaging-and-printing): filtro hpcups e PPD.
- [squatchus/hp-deskjet-2320-macos-driver](https://github.com/squatchus/hp-deskjet-2320-macos-driver): investigação e receita de adaptação macOS que orientaram a solução.
- [libjpeg-turbo](https://libjpeg-turbo.org/): biblioteca JPEG linkada estaticamente.
- Preparação, revisão e teste assistidos por OpenAI Codex; impressão física
  confirmada pelo proprietário. A assistência de IA não equivale a certificação.

Scripts e documentação próprios: MIT, veja `LICENSE`. Componentes de terceiros
mantêm suas licenças e copyrights: veja `NOTICE.md`, `licenses/` e o arquivo
completo de fontes em `sources/`. Produto fornecido sem garantia.
