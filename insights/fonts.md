# The Standard RISC OS Fonts

## Quirks
The regular set of RISC OS Fonts do not contain all the possible glyphs. They also have some inconsistencies:

* *NewHall.Medium* character code 0x81 (with no alphabet specified and also *Latin1* alphabet) displays a breve, but the Italic and Bold versions do not.
* *NewHall.Medium* and *NewHall.Medium.Italic* with the *Latin9* alphabet also display the breve (but not in the Bold fonts).
* In the *Cyrillic* alphabet (in multiple fonts), RISC OS puts a 'Hyphen-Minus' at 0xae, which is not the standard (perhaps this was meant to be at 0xad, the soft-hyphen).
* *Corpus.Medium* with *Greek* alphabet has 0xaf set to what looks like 'Latin Subscript Small Letter O', which is non-standard (ISO/IEC 8859-7, should be a horizontal bar).
* *Sassoon* with the *Welsh* alphabet has 0xac and 0xbc set to 'Ẽ' and 'ẽ', which is non-standard (ISO IR-182, should be 'Ỳ' and 'ỳ'.)
* *Sassoon* with the *Hebrew* alphabet (has 0xaf set to 'EFF' in small caps, which is non-standard (ISO/IEC 8859-8, should be a Macron). Clearly a reference to the [Electronic Font Foundry](https://en.wikipedia.org/wiki/The_Electronic_Font_Foundry).
* *System* font, character code 0x87 shows a subscript 8 and superscript 7, which seems like a placeholder rather than a design choice.
* *Swiss.Monospaced.Bold.italic* is named inconsistently with the word 'italic' not capitalised.

## Fonts

![Corpus.Bold](tiled/Corpus.Bold.png)

![Corpus.Medium](tiled/Corpus.Medium.png)

![Homerton.Bold](tiled/Homerton.Bold.png)

![Homerton.Medium](tiled/Homerton.Medium.png)

![NewHall.Bold](tiled/NewHall.Bold.png)

![NewHall.Medium](tiled/NewHall.Medium.png)

![Sassoon.Primary.Bold](tiled/Sassoon.Primary.Bold.png)

![Sassoon.Primary](tiled/Sassoon.Primary.png)

![Selwyn](tiled/Selwyn.png)

![Sidney](tiled/Sidney.png)

![Swiss.Monospaced.Bold.italic](tiled/Swiss.Monospaced.Bold.italic.png)

![Swiss.Monospaced.Bold](tiled/Swiss.Monospaced.Bold.png)

![Swiss.Monospaced.Italic](tiled/Swiss.Monospaced.Italic.png)

![Swiss.Monospaced](tiled/Swiss.Monospaced.png)

![System.Fixed](tiled/System.Fixed.png)

![System.Medium](tiled/System.Medium.png)

![System](tiled/System.png)

![Trinity.Bold.Italic](tiled/Trinity.Bold.Italic.png)

![Trinity.Bold](tiled/Trinity.Bold.png)

![Trinity.Medium.Italic](tiled/Trinity.Medium.Italic.png)

![Trinity.Medium](tiled/Trinity.Medium.png)

![WimpSymbol](tiled/WimpSymbol.png)
