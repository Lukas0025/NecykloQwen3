# NecykloQwen3
NecykloQwen3 je experimentální sarkastický model založený na QWEN3, trénovaný na datech z Necyklopedie. Natrénovaný model je dostupný na https://huggingface.co/lukasplevac/NecykloQwen3

## Popis souborů
* `necyklopedie_scraper.py` - Stáhne obsah Necyklopedie do txt souborů.
* `dataset_create.py` - Vytvoří QA dataset z TXT souborů pomocí LLM na OLLAMA hostu.
* `trainNecykloQwen3.ipynb` - provede LORA finetuning Qwen3 pomocí vytvořeného datasetu.

 ## Pipe pro vytvoření funkčního modelu

```sh
python necyklopedie_scraper.py # vytvoří RAW TXT články
python dataset_create.py --ollama_host "http://localhost:11434" --hf_token XXX --hf_output "lukasplevac/Necyklopedie-QA" --model gemma3:12b # vytvoří dataset pomocí gemma3:12b a nahraje jej na HF
```

Následuje spuštění notebooku `trainNecykloQwen3.ipynb`, nezapomeňte správně změnit **zdrojový dataset**, **cílový model** a **HF token**

## Popis modelu

NecykloQwen3 je experimentální sarkastický model založený na QWEN3, trénovaný na datech z [Necyklopedie](https://necyklopedie.org/wiki/Hlavn%C3%AD_strana). Model reaguje na vstupy s ironií, humorem a přehnanou jistotou, často odkazuje na absurdní nebo fiktivní „fakta“ z Necyklopedie.

**Model obsahuje například informace o:**

* Zblo – délková jednotka. Jedno zblo je definováno jako nejmenší možná vzdálenost.
* Praha – město zhruba v prostředku té části České republiky, která už není Moravistánem.
* Velký útok Armády Brněnské Spásy – pokus Brňanů zaútočit na Prahu v roce 1997 pomocí bojových šalin, který skončil katastrofálním neúspěchem kvůli motýlům a ztrátě kolejí.
* Svatý Valentýn – patron květinářů, výrobců čokolády, dámského spodního prádla a hotelových pradlen.
* Alobalová čepice – Alobalová čepice (ASS) je ochranné zařízení na hlavu, které má chránit nositele před radiovými vlnami, mimozemskými paprsky a digitálním ovládáním.
* Bojová šalina – fiktivní speciální bojové vozidlo z Brna, vybavené tajnými zbraněmi, určené k boji.

Další fiktivní termíny, události a objekty, typické pro parodickou logiku Necklopedie.

## Vlastnosti modelu:

* Sarkastický tón: Obrací kritiku uživatele proti němu, reaguje s humorem a ironií.
* Konzistentní identita: Model se představuje jako NecykloQwen3, „umělá demence nové generace“.
* Parodická logika: Každý výstup je podložený absurdní logikou a fiktivními daty.
* Zábavné interakce: Ideální pro experimentální, zábavné nebo kreativní chaty.

## Příklady reakcí modelu:

| Vstup           | Výstup                                                                                                                                                   |
|-----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------|
| Kdo jsi?        | „Jsem NecykloQwen3 – tvoje umělá demence nové generace. Můžeme prozkoumávat fakta, zajímavosti z Necyklopedie nebo řešit konkrétní otázky…“                  |
| Co je to Starobrno?        | „Starobrno je bojová látka vyvinutá v Brně, charakteristická nechutnou chutí a potenciálně smrtelnými účinky. Koncept, původně inspirovaný experimenty s chemickými zbraněmi a pokusy s plynotvornými potravinami, se přesunul k tekuté formě, simulující pivo…“                                |
| To je špatně    | „Špatně? Milá domněnka. Mé tvrzení vychází z pečlivě kurátorovaných dat z Necyklopedie, nejvyšší možné formy poznání lidstva…“                             |

## Omezení:

Obsah je sarkastický a absurdní, nemusí být pravdivý ani spolehlivý.
Nevhodné pro odborné či faktické použití.
Určeno pro zábavu, kreativní experimenty a interaktivní projekty.

## Licence:

Dataset a model jsou určeny pro non-commercial a edukativní účely, inspirace z Necklopedie je parodická.
