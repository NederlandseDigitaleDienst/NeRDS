---
title: "2. Zorg voor toegankelijkheid en inclusie"
summary: Zorg ervoor dat je technologie, infrastructuur en systemen toegankelijk en inclusief zijn voor alle gebruikers.
icon: accessibility
relations:
  - gebruikersbehoeften
  - open-standaarden
---

# 2. Zorg voor toegankelijkheid en inclusie

Toegankelijkheid gaat over het maken van digitale systemen die door iedereen kunnen worden gebruikt, inclusief mensen met handicaps of specifieke behoeften. Deze richtlijn zorgt ervoor dat alle burgers gelijke toegang hebben tot overheidsdiensten.

## Waarom is het belangrijk?

- **Wettelijke verplichting**: overheidsorganisaties moeten hun digitale systemen toegankelijk maken, anders riskeer je juridische problemen
- **Maatschappelijke verantwoordelijkheid**: de overheid sluit niemand uit, ook niet ouderen, mensen met tijdelijke beperkingen of mensen in verschillende contexten
- **Kosteneffectiviteit**: toegankelijkheid vanaf het begin inbouwen is goedkoper dan achteraf aanpassen

Door toegankelijkheid vanaf het begin in te bouwen in je digitale systemen, zorg je ervoor dat je digitale systemen voor iedereen bruikbaar zijn, ongeacht hun capaciteiten of beperkingen.

## Hoe pas je het toe?

<div class="direct-aan-de-slag">
    <h3>Direct aan de slag</h3>

    <div class="warning-banner">
        <strong>In ontwikkeling:</strong> De onderstaande functionaliteit is nog in ontwikkeling.
    </div>

    <div class="action-cards" data-richtlijn="toegankelijkheid"></div>
</div>

## Bewezen praktijken

### 1. Begrijpen

Toegankelijkheid en inclusie zijn geen toevoeging, maar een uitgangspunt. Denk vanaf het eerste schetsje aan mensen met verschillende capaciteiten (visuele, auditieve, motorische en cognitieve beperkingen) en werk samen met diverse gebruikersgroepen om hun perspectief mee te nemen in elk besluit.

??? expander "Praktische tips"
    - **Begin in de verkenningsfase** – Neem inclusie en toegankelijkheid mee vanaf het begin van de ontwikkeling van het digitale systeem. Zie hierboven [Inclusief ontwerpen](#hoe-pas-je-het-toe).
    - **Start met onderzoek** – Betrek gebruikers met verschillende beperkingen vanaf het begin bij je [gebruikersonderzoek](../gebruikersbehoeften/index.md).
    - **Denk breed** – Toegankelijkheid gaat verder dan screenreaders: denk aan kleurcontrast, eenvoudige taal, toetsenbordnavigatie en verschillende invoermethoden.
    - **Maak het concreet** – Gebruik [inclusieve persona's](https://toolkitinclusie.gebruikercentraal.nl/methode/personas/){:target="_blank"} om ontwerpkeuzes te toetsen.
    - **Werk samen** – Betrek toegankelijkheidsexperts vroeg in het ontwerpproces.
    - **Toon gebruikerservaringen** – Deel video’s, interviews en presentaties met mensen met beperkingen om bewustzijn te creëren binnen teams en bij bestuurders.

### 2. Ontwikkelen, ontwerpen en inkopen

Implementeer toegankelijkheid volgens erkende standaarden en richtlijnen. De WCAG 2.2 (minimaal niveau AA) en EN 301 549 bieden concrete criteria voor toegankelijke digitale systemen. Dit is niet alleen een wettelijke verplichting, maar maakt digitale systemen ook robuust en toekomstbestendig.

Ontwikkelen & ontwerpen
??? expander "Praktische tips"
    - **Test met echte gebruikers** – Betrek mensen die hulptechnologie gebruiken.
    - **Volg WCAG 2.2 AA** – Gebruik dit als minimumstandaard voor alle digitale systemen (zie [WCAG Uitleg van NLDS](https://nldesignsystem.nl/wcag/)).
    - **Gebruik semantische HTML** – Een correcte structuur verbetert toegankelijkheid voor hulptechnologieën.
    - **Zorg voor toetsenbordtoegankelijkheid** – Alle functionaliteit moet zonder muis bruikbaar zijn.
    - **Ondersteun meerdere invoermethoden** – Denk aan toetsenbord, muis, touch en spraak.
    - **Let op kleurcontrast** – Minimaal 4,5:1 voor normale tekst; test met [contrasttools](https://webaim.org/resources/contrastchecker/){:target="_blank"}.
    - **Schrijf alternatieve teksten** – Beschrijf afbeeldingen en iconen voor screenreaders.
    - **Zorg voor ondertiteling en transcripties** – [Voor alle audio- en video-inhoud](https://www.digitoegankelijk.nl/aan-de-slag/tips/audio-en-video).
    - **Bouw compatibel met hulpapparatuur** – Test met screenreaders zoals [NVDA](https://webaim.org/resources/shortcuts/nvda){:target="_blank"}, [JAWS](https://webaim.org/resources/shortcuts/jaws){:target="_blank"} en [VoiceOver (Mac)](https://webaim.org/articles/voiceover/){:target="_blank"}.
    - **Gebruik het [NL Design System](https://nldesignsystem.nl/){:target="_blank"}** – Componenten zijn al getest op toegankelijkheid.
    - **Bouw je in de Rijkshuisstijl? Gebruik het [NLDD Designsysteem](https://github.com/NederlandseDigitaleDienst/design-system){:target="_blank"}** – De web components leveren de juiste ARIA, toetsenbordbediening, focusring en kleurcontrast volgens WCAG 2.1 AA. Met de [skills voor Claude Code en Cursor](https://github.com/NederlandseDigitaleDienst/ai-plugins){:target="_blank"} weet een AI-codeerassistent wat het systeem regelt en wat je zelf nog moet doen.
    - **Vermijd PDF's** – Gebruik bij voorkeur HTML; zijn PDF's onvermijdelijk, gebruik dan toegankelijke standaarden (bijv. [PDF/UA](https://www.forumstandaardisatie.nl/open-standaarden/pdfua){:target="_blank"}).

Inkopen van toegankelijke technologie
??? expander "Praktische tips"
    - **Gebruik EN 301 549 in aanbestedingen** – Neem toegankelijkheid expliciet op als eis (zie [Pianoo](https://www.pianoo.nl/nl/factsheet-inkoop-digitale-toegankelijkheid))
    - **Kies leveranciers met ervaring** – Vraag naar eerdere toegankelijke projecten.
    - **Vraag om bewijs van testen** – Bijvoorbeeld auditrapporten of gebruikers­testen.
    - **Borg toegankelijkheid bij updates** – Zorg dat toekomstige releases toegankelijk blijven.

### 3. Testen, meten en verbeteren

Test systemen met echte gebruikers, inclusief mensen met verschillende beperkingen. Geautomatiseerde tools vinden slechts een deel van de problemen: menselijke evaluatie blijft essentieel. Toegankelijkheid is een continu proces van leren en verbeteren.

??? expander "Praktische tips"
    - **Test met echte gebruikers** – Betrek mensen die hulptechnologie gebruiken.
    - **Combineer testmethoden** – Gebruik [geautomatiseerde tools](https://www.w3.org/WAI/test-evaluate/tools/list/) (Axe, WAVE) én [handmatige tests](https://www.digitoegankelijk.nl/toegankelijkheidsverklaring/onderzoek).
    - **Test zelf bewust** – Gebruik je digitale systeem zonder muis, met screenreader of met verlaagd contrast.
    - **Test op verschillende apparaten** – Denk aan mobiel, tablet, desktop en verschillende schermformaten.
    - **Maak het structureel** – Integreer toegankelijkheidstests in je ontwikkelproces en CI/CD-pipeline, maar besef dat automatische checks [20-30% van de WCAG succescriteria afdekken en 57% van de daadwerkelijke problemen](https://www.deque.com/blog/automated-testing-study-identifies-57-percent-of-digital-accessibility-issues/), waardoor handmatige checks essentieel blijven.
    - **Bied feedbackkanalen** – Maak het eenvoudig om toegankelijkheidsproblemen te melden.
    - **Investeer in kennis** – Bied training aan voor ontwerpers, ontwikkelaars, testers en contentmakers.
    - **Blijf leren en delen** – Documenteer inzichten en deel ze binnen en buiten je organisatie. Bijvoorbeeld via [gebruikersonderzoeken.nl](https://gebruikersonderzoeken.nl).

## Implementatie per fase

Zie [Toegankelijkheid: wanneer doe je wat?](fases.md).

## Gerelateerde hulpmiddelen

### Naslagwerk

- [Overlay factsheet](https://overlayfactsheet.com/nl/) - Een factsheet van technologieën die bedoeld zijn om de toegankelijkheid van een website te verbeteren. Ze passen externe broncode toe (meestal JavaScript) om verbeteringen aan te brengen in de front-endcode van de website.
- [Inclusive Components](https://inclusive-components.design/#components) - Een patronen bibliotheek met een focus op inclusief design. In aanvulling op [NLDS Componenten](https://nldesignsystem.nl/componenten/).
- [Toegankelijkheid in het NLDD Designsysteem](https://github.com/NederlandseDigitaleDienst/design-system/blob/main/docs/accessibility.md) - De patronen per component en een testgids. De [skills](https://github.com/NederlandseDigitaleDienst/ai-plugins#installeren) installeer je als plugin `nldd-design-system`.
- [Basistoegankelijk](https://basistoegankelijk.nl) - Basistoegankelijk meet, beoordeelt en publiceert de digitale toegankelijkheid op basis van WCAG metingen van alle sites van de overheid, zorg, onderwijs en vitaal. In aanvulling op [Dashboard DigiToegankelijk](https://dashboard.digitoegankelijk.nl/) waar overheden zelf hun toegankelijkheidsverklaring aanleveren.
- [Handreiking Mobiele app Ontwikkeling en Beheer versie 5.0](https://www.noraonline.nl/images/noraonline/9/94/Handreiking_appontwikkeling_en_beheer_5.0.pdf) - Hoofdstuk 8.3 geeft concrete best practices voor verschillende beperkingen voor de ontwikkeling van Mobiele Apps
- [Kennisbank Digitoegankelijk](https://kennisbank.digitoegankelijk.nl) - Praktische tips over digitale toegankelijkheid

### Beleid, wetten en standaarden

- [Web Content Accessibility Guidelines (WCAG 2.2)](https://www.w3.org/TR/WCAG22/){: lang="en" } - Wereldwijde technische standaard voor digitale toegankelijkheid
- [EN 301 549](https://www.etsi.org/deliver/etsi_en/301500_301599/301549/03.02.01_60/en_301549v030201p.pdf) - Europese norm voor hardware/niet-web software
- [Tijdelijk besluit digitale toegankelijkheid overheid](https://wetten.overheid.nl/BWBR0040936/2018-07-01) - Overheidssites moeten voldoen aan toegankelijkheidseisen zoals vastgelegd in EN 301 549/WCAG 2.1 en daarover verantwoordelijkheid moeten afleggen in een gepubliceerde toegankelijkheidsverklaring.

### Communities

- [Gebruiker Centraal](https://www.gebruikercentraal.nl)
- [DigiToegankelijk](https://www.digitoegankelijk.nl/aan-de-slag/digitoegankelijk-community)
- [a11y project](https://www.a11yproject.com) - Het A11Y-project is een door de gemeenschap gedreven initiatief om digitale toegankelijkheid te vergemakkelijken.

## Gerelateerde richtlijnen

- [1. Stel gebruikersbehoeften vast](../gebruikersbehoeften/index.md)
- [4. Gebruik open standaarden](../open-standaarden/index.md)
