def carregar_imagem(Pastor):
    with open(Pastor, 'rb') as f:
        assert f.readline().strip() == b'P6' #Verificando se a imagem é no formato P6 (PPM)
        
        def proxima_linha():
            linha = f.readline()
            while linha.startswith(b'#') or linha.strip() == b'':
                linha = f.readline()
            return linha
                
        linha = proxima_linha()
        la, al = map(int, linha.strip().split()) #Ler a Lagura(la) e a Altura(al)

        linha = proxima_linha()
        maximo = int(linha.strip()) #Lendo o total de canais de cores (maximo=255)

        #Lendo os dados:
        dados = f.read(la * al * 3)

        pixels = [list(dados[i:i+3]) for i in range(0, len(dados),3)] # cada pixel tem R,G,B
        imagem = [pixels[i*la:(i+1)*la] for i in range(al)]
    return imagem, la, al, maximo


entrada = 'Pastor.ppm'
imagem, la, al, maximo = carregar_imagem(entrada)



def salvar_imagem(nome_arquivo, imagem, largura, altura, maximo=255):
    with open(nome_arquivo, 'wb') as f:
        f.write(b'P6\n')
        f.write(f'{largura} {altura}\n'.encode())
        f.write(f'{maximo}\n'.encode())

        for linha in imagem:
            for pixel in linha:
                f.write(bytes(pixel))


def mudar_para_cinza(imagem, la, al):
    nova_imagem = []
    for linha in imagem:
        nova_linha = []
        for pixel in linha:
            r, g, b = pixel
            # Calcula o valor em cinza
            cinza = int(0.299 * r + 0.587 * g + 0.114 * b)
            nova_linha.append([cinza, cinza, cinza])
        nova_imagem.append(nova_linha)
    return nova_imagem


def mudar_para_binario(imagem_cinza, la, al, limiar=128):
    imagem_binaria = []
    for linha in imagem_cinza:
        nova_linha = []
        for pixel in linha:
            c = pixel[0]
            if c >= limiar:
                nova_linha.append([255, 255, 255])  # Branco
            else:
                nova_linha.append([0, 0, 0])        # Preto
        imagem_binaria.append(nova_linha)
    return imagem_binaria


entrada = 'Pastor.ppm'
imagem, la, al, maximo = carregar_imagem(entrada)

# Converte para cinza
imagem_cinza = mudar_para_cinza(imagem, la, al)
salvar_imagem('cinza.ppm', imagem_cinza, la, al, maximo)

# Converte para binário
imagem_binaria = mudar_para_binario(imagem_cinza, la, al)
salvar_imagem('binaria.ppm', imagem_binaria, la, al, maximo)
