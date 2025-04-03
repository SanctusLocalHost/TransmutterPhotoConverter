# TRANSMUTER PHOTO CONVERTER

TRANSMUTER é um conversor de imagens em lote com suporte a drag & drop, desenvolvido em Python, com interface escura utilizando CustomTkinter.

## Funcionalidades

- **Importação via Drag & Drop e Diálogo de Arquivos:** Importe imagens arrastando para a área designada ou usando o botão "Importar Imagens".
- **Resolução Personalizada:** Configure a largura e altura desejadas para a conversão.
- **Seleção de Formato:** Escolha entre os formatos de saída:  
  PNG, JPEG, JPG, BMP, GIF, TIFF, WEBP, ICO  
  *(Observação: "JPG" é tratado como "JPEG" internamente.)*
- **Conversão em Lote:** As imagens convertidas são salvas na pasta `imagens_convertidas`.
- **Tratamento de Transparência:** Converte imagens com canal alfa (RGBA ou P) para RGB ao salvar em JPEG.

INTERFACE DO SOFTWARE

![Screenshot do Transmuter](https://github.com/SanctusLocalHost/TransmutterPhotoConverter/blob/main/image.png)

## Como Funciona
Importe as Imagens: Utilize drag & drop ou o botão "Importar Imagens" para carregar os arquivos.

Defina a Resolução: Insira a largura e a altura desejadas.

Selecione o Formato: Escolha o formato de saída.

Converta as Imagens: Clique em "Converter Imagens" para processar e salvar os arquivos convertidos.


## Requisitos

Instale as dependências necessárias via pip:

```bash
pip install customtkinter tkinterdnd2 pillow
