# scripts/gerar_icone.py
"""Gera assets/icon.png e assets/splash.png (gravata com colarinho).

Rode com: python3 scripts/gerar_icone.py

Todas as coordenadas são frações do tamanho do canvas (0.0 a 1.0), então
o mesmo desenho serve tanto pro ícone (512x512, fundo navy) quanto pro
splash (720x720, fundo transparente).
"""
from PIL import Image, ImageDraw

NAVY_TOP = (3, 34, 63)
NAVY_BOTTOM = (10, 20, 35)
COLARINHO = (245, 243, 238)
GRAVATA = (74, 77, 82)  # cinza chumbo
GRAVATA_FAIXA = (196, 150, 23)  # dourado


def _p(tamanho, *fracoes):
    """Converte uma lista de frações (x0,y0,x1,y1,...) em pontos de pixel."""
    vals = [f * tamanho for f in fracoes]
    return list(zip(vals[0::2], vals[1::2]))


def _desenhar(tamanho, fundo_navy):
    img = Image.new("RGBA", (tamanho, tamanho), (0, 0, 0, 0))

    if fundo_navy:
        raio = int(tamanho * 0.22)
        fundo = Image.new("RGBA", (tamanho, tamanho), (0, 0, 0, 0))
        fdraw = ImageDraw.Draw(fundo)
        for y in range(tamanho):
            t = y / tamanho
            cor = tuple(int(NAVY_TOP[i] + (NAVY_BOTTOM[i] - NAVY_TOP[i]) * t) for i in range(3)) + (255,)
            fdraw.line([(0, y), (tamanho, y)], fill=cor)
        mask = Image.new("L", (tamanho, tamanho), 0)
        ImageDraw.Draw(mask).rounded_rectangle(
            [0, 0, tamanho - 1, tamanho - 1], radius=raio, fill=255
        )
        fundo.putalpha(mask)
        img = fundo

    draw = ImageDraw.Draw(img)

    # Colarinho (chevron branco) — topo da tela, mesmo tamanho/posição do
    # desenho original.
    colarinho = _p(
        tamanho,
        0.175, 0.020,   # topo-esquerda externo
        0.313, 0.020,   # topo-esquerda interno
        0.500, 0.185,   # ponta central (onde encontra a gravata)
        0.688, 0.020,   # topo-direita interno
        0.825, 0.020,   # topo-direita externo
        0.500, 0.270,   # ponta inferior do V
    )
    draw.polygon(colarinho, fill=COLARINHO)

    # Gravata — nó estreito logo abaixo do colarinho, alarga nos ombros e
    # afina até a ponta em V. ~15% maior que o desenho original (ocupa
    # até ~92% da altura do canvas, em vez de ~80%).
    gravata = _p(
        tamanho,
        0.480, 0.230,   # nó topo-esquerda
        0.520, 0.230,   # nó topo-direita
        0.560, 0.330,   # ombro direito
        0.545, 0.470,   # lateral direita descendo
        0.500, 0.920,   # ponta inferior
        0.455, 0.470,   # lateral esquerda descendo
        0.440, 0.330,   # ombro esquerdo
    )
    draw.polygon(gravata, fill=GRAVATA)

    # Faixa dourada central (detalhe decorativo).
    faixa = _p(
        tamanho,
        0.492, 0.280,
        0.508, 0.280,
        0.515, 0.470,
        0.500, 0.870,
        0.485, 0.470,
    )
    draw.polygon(faixa, fill=GRAVATA_FAIXA)

    return img


if __name__ == "__main__":
    icone = _desenhar(512, fundo_navy=True)
    icone.save("assets/icon.png")
    print("assets/icon.png gerado")

    splash = _desenhar(720, fundo_navy=False)
    splash.save("assets/splash.png")
    print("assets/splash.png gerado")
