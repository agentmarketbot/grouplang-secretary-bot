# GroupLang-secretary-bot

GroupLang-secretary-bot Telegram bot bat da, ahots-mezuak transkribatzen dituena, edukia laburbiltzen duena eta erabiltzaileei zerbitzuagatik tipa emateko aukera ematen diena. AWS zerbitzuak erabiltzen ditu transkripziorako eta API pertsonalizatua laburpenetarako. Bot-a AWS Lambda funtzio gisa hedatzeko diseinatuta dago.

## Eduki-taula

- [Ezaugarriak](#ezaugarriak)
- [Aurrebaldintzak](#aurrebaldintzak)
- [Instalazioa](#instalazioa)
- [Konfigurazioa](#konfigurazioa)
- [Erabilera](#erabilera)
- [Hedapena](#hedapena)
- [API Erreferentzia](#api-erreferentzia)

## Ezaugarriak

- Ahots-mezuak transkribatu AWS Transcribe erabiliz
- Testu transkribatua laburbildu API pertsonalizatu baten bidez
- Erabiltzaileei zerbitzuagatik tipa emateko aukera eman
- API gako eta tokenen kudeaketa segurua
- AWS Lambda funtzio gisa hedagarria

## Aurrebaldintzak

- Poetry mendekotasun kudeaketarako
- AWS kontua Transcribe sarbidearekin
- Telegram Bot Token
- MarketRouter API Gakoa

## Instalazioa

1. Klonatu biltegia:
   ```
   git clone https://github.com/yourusername/GroupLang-secretary-bot.git
   cd GroupLang-secretary-bot
   ```

2. Instalatu Poetry oraindik ez baduzu:
   ```
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. Instalatu mendekotasunak Poetry erabiliz:
   ```
   poetry install
   ```

## Konfigurazioa

1. Ezarri ingurune aldagaiak:
   - `TELEGRAM_BOT_TOKEN`: Zure Telegram Bot Token
   - `AWS_ACCESS_KEY_ID`: Zure AWS Sarbide Gakoa ID
   - `AWS_SECRET_ACCESS_KEY`: Zure AWS Sarbide Gakoa Sekretua
   - `MARKETROUTER_API_KEY`: Zure MarketRouter API Gakoa

2. Konfiguratu AWS kredentzialak:
   - Ezarri AWS CLI edo erabili goian aipatutako ingurune aldagaiak

## Erabilera

1. Aktibatu Poetry ingurune birtuala:
   ```
   poetry shell
   ```

2. Abiarazi bot-a:
   ```
   uvicorn main:app --reload
   ```

3. Telegramen, hasi elkarrizketa botarekin edo gehitu talde batean

4. Bidali ahots-mezu bat botari

5. Bot-ak audioa transkribatuko du, edukia laburbilduko du eta emaitza bidaliko du berriro

6. Erabiltzaileek tipa eman dezakete erantzunarekin emandako botoi bidez

## Mendekotasunak gehitzea edo eguneratzea

Pakete berri bat gehitzeko:
```
poetry add package_name
```

Pakete guztiak eguneratzeko:
```
poetry update
```

Pakete zehatz bat eguneratzeko:
```
poetry update package_name
```

## API Erreferentzia

Bot-ak honako API kanpokoak erabiltzen ditu:

- AWS Transcribe: Audio transkripziorako
- MarketRouter API: Testu laburpen eta sari bidalketarako

API hauen dokumentazioan xehetasun gehiago aurki ditzakezu.

Fixes #98
