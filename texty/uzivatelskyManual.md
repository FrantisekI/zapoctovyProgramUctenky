# Uživatelský manuál

## K čemu je to dobré:
- Tento program slouží k ukládání zakoupených produktů 
- Vstupem pro program je obrázek účtenky, který program zpracuje, pak se zeptá, jestli je vše v pořádku - budete mít možnost výsledky upravit a uloží do databáze
- Program vám umožní následně zobrazit, co jste zakoupili a kolik jste za to zaplatili a podobné informace


## Co budete potřebovat:
- Určitě funguje na Python 3.11 a vyšší a pip verze 25.0
- MySQL databáze
- připravit si environment variables - buď do .env umístěného do root složky tohoto repozitáře souboru nebo jako systémové proměnné
    - GROQ_API_KEY (z https://console.groq.com/keys)
    - OCR_API_KEY (z https://ocr.space/OCRAPI/confirmation)
    - DB_HOST = "127.0.0.1" / nebo pokud máte nějakou vzdálenou, tak její IP
    - DB_USER = "root" / nebo nějaký jiný uživatel
    - DB_DATABASE (jméno vaší databáze)
    - DB_PASSWORD (heslo pro vaši databázi)
- vytvořit virtuální prostředí a nainstalovat requirements:
    - `python -m venv venv` (nebo místo 2. venv nějaký jiný název)
    - `venv\Scripts\activate` (tady ten samý)
    - `pip install -r requirements.txt`
- přístup k internetu

## Jak ukládat účtenky:
- aktivovat virtuální prostředí - `source venv\Scripts\activate`
- spustit program:
    - `python __main__.py`
- postupujte podle pokynů programu
- uložte si obrázek účtenky do počítače na kterém je program a do konzole zadejte cestu k němu
- program po chvíli vrátí jako tabulku všechny položky z účtenky
- pokud budete chtít nějakou informaci změnit, zadejte číslo nebo písmeno které se nachází v prvním sloupci, vyberte co chcete zmenit a zadejte novou hodnotu
- až budete spokojeni napište do konzole `done` a program vše uloží do databáze

## Jak zobrazit uložené účtenky:
- pokud na úvodu zvolíte možnost `1`, tak si budete moci vybrat jakou informaci o vašich nákupu chcete zobrazit
- až budete hotovi opět napište `done` a opět se vrátíte na úvodní obrazovku


