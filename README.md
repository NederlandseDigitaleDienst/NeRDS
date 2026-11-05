# Nederlandse Richtlijn Digitale Systemen

De [Nederlandse Digitale Dienst](https://github.com/NederlandseDigitaleDienst) ontwikkelt de Nederlandse
Richtlijn Digitale Systemen (NeRDS) op een open manier via Github.
De Nederlandse Richtlijn Digitale Systemen is een set standaarden, richtlijnen en praktische hulpmiddelen (tools) voor het
verantwoord ontwerpen, ontwikkelen en inkopen van digitale systemen binnen de Nederlandse overheid.

In deze repository ontwikkelen wij de Nederlandse Richtlijn Digitale Systemen. De informatie van de Nederlandse
Richtlijn Digitale Systemen wordt uitgewerkt in verschillende Markdown bestanden (een bestandsformaat voor platte
tekstbestanden), welke je terug kan vinden in de map
[docs](docs).
Deze bestanden worden inzichtelijk gemaakt met behulp van [MkDocs](https://www.mkdocs.org/)
en vormgegeven met het [NLDD Designsysteem](https://github.com/NederlandseDigitaleDienst/design-system) in de Rijkshuisstijl.

De Nederlandse Richtlijn Digitale Systemen kun je bekijken op
[https://nerds.digitaledienst.overheid.nl](https://nerds.digitaledienst.overheid.nl/).

## Hoe kun je bijdragen?

Dat kan op verschillende manieren. Zie onze
[Contributing Guidelines](CONTRIBUTING.md) voor meer uitleg over hoe je kan bijdragen aan de Nederlandse Richtlijn
Digitale Systemen.

### Lokaal ontwikkelen

Je hebt alleen [uv](https://docs.astral.sh/uv/) nodig. Een preview van de website start je met:

```bash
uv run mkdocs serve
```

uv installeert bij de eerste keer zelf de juiste Python en de afhankelijkheden uit `pyproject.toml` en `uv.lock`.

De website gebruikt de web components van het NLDD Designsysteem. De versie staat vast in
`nldd-design-system.json`. Bij de eerste build wordt dat pakket eenmalig gedownload naar `.cache/nldd/`.
De build bundelt met esbuild alleen de componenten die de pagina's gebruiken. Daarvoor heb je Node nodig. De versies
van esbuild en het designsysteem staan in `tools/bundle/package.json`; die van het designsysteem moet gelijk zijn aan
die in `nldd-design-system.json`.

Controleer een wijziging aan het thema of aan de inhoud met:

```bash
uv run python scripts/check_site.py
```

Dit bouwt de website en controleert of elk component, attribuut, icoon en elke CSS-variabele bestaat in het
designsysteem, en of er niets is verdwenen uit wat een pagina kan (links, formuliervelden, knoppen).
Heb je bewust iets weggehaald of toegevoegd, leg dat dan vast met `uv run python scripts/check_site.py --update`.

De toegankelijkheid controleer je met:

```bash
just a11y
```

Dit bouwt de website en test elke pagina met pa11y-ci tegen WCAG 2.1 AA, met twee engines (HTML_CodeSniffer en axe).
Dezelfde controle draait op elke pull request. Je hebt er Node en Google Chrome voor nodig.

## Vragen?

Maak een [Issue](https://github.com/NederlandseDigitaleDienst/NeRDS/issues) aan op GitHub. Of stuur een e-mail naar
[bureau.architectuur@minbzk.nl](mailto:bureau.architectuur@minbzk.nl).
