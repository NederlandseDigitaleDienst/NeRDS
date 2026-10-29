<!-- Gegenereerd uit docs/richtlijnen/open-source/index.md. Wijzig dat bestand en draai: just plugin -->

# 3. Werk transparant en gebruik open source

Open source is een manier van werken waarbij de makers de broncode, documentatie en ontwerp openbaar beschikbaar stellen onder een opensourcelicentie. Hierdoor kan iedereen de software bekijken, kopiëren, aanpassen of delen. Mensen kunnen voorstellen doen voor verbeteringen of toevoegingen. Het delen van code en het gebruik van open source software kan leiden tot betere, veiligere en meer kosteneffectieve oplossingen.

## Waarom is het belangrijk?

- **Transparantie en veiligheid**: iedereen kan zien hoe de software werkt, waardoor problemen sneller worden ontdekt en vertrouwen ontstaat
- **Samenwerking en innovatie**: organisaties kunnen kennis delen, van elkaar leren en voortbouwen op bestaande oplossingen
- **Kosteneffectiviteit**: vermijd licentiekosten, vendor lock-in en bespaar tijd door hergebruik van bestaande oplossingen

Door open en transparant te werken en open source software te omarmen, draag je bij aan een meer transparante, flexibele en verantwoordelijke digitale overheid.

## Hoe pas je het toe?

**Direct aan de slag**

- [Ambitieladder opensourcewerken](https://minvws.opensourcewerken.nl/open-source-ambitieladder-voor-opensourcewerken-in-projecten/): Helpt projectteams concrete afspraken te maken over opensourcewerken
- [Open Stad](https://openstad.org/): Open source platform voor participatie en samenwerking
- [Opensourcewerken.nl](https://opensourcewerken.nl): Kennis en community voor open source werken bij de overheid
- [Community Opensourcewerken](https://developer.overheid.nl/communities/open-source-werken): Community of practice omtrent open source werken (status: ontwikkeling)
- [Standaard voor publieke code](https://www.standaardvoorpubliekecode.nl/): Richtlijnen voor het ontwikkelen en beheren van software en beleid
- [Handreiking publieke waarde bij ICT-aanbesteding](https://www.pianoo.nl/nl/handreiking-publieke-waarden-en-rechten-bij-aanbesteden-van-ict): Stappenplan voor het maken van bewuste keuzes rondom publieke waarde en rechten
- [Licentieadvies](https://opensourcewerken.nl/page/view/677bb847-79b5-42b2-8a63-e7bb2e074530/softwarelicenties): Copyleft: CC BY-SA, GPLv3, AGPLv3 of EUPL-1.2. Permissive: Apache 2.0, MIT, BSD-0-clause

## Bewezen praktijken

### 1. Begrijpen

Start met verkennen van bestaande open source oplossingen voordat je zelf iets bouwt. Evalueer of open source past bij je project en begrijp het [open-tenzij beleid](https://www.digitaleoverheid.nl/overzicht-van-alle-onderwerpen/open-source/beleid/): je code moet open zijn, tenzij er zwaarwegende redenen zijn om dit niet te doen (zoals staatsgeheimen of fraudepreventie). Dit principe van transparantie versterkt het vertrouwen in de overheid.

**Praktische tips**

- **Onderzoek eerst of hergebruik mogelijk is** - Zoek naar bestaande open source oplossingen die je probleem al oplossen. Verken repositories op [developer.overheid.nl](https://oss.developer.overheid.nl/).
- **Begrijp welke afspraken er in het team gemaakt moeten worden** - Verken de [Open source ambitieladder](https://minvws.opensourcewerken.nl/open-source-ambitieladder-voor-opensourcewerken-in-projecten/).
- **Evalueer total cost of ownership** - Kijk naar alle kosten: implementatie, migratie, training en onderhoud.
- **Test met prototypes** - Bouw kleine prototypes om technische aannames te valideren.
- **Betrek de community** - Leg contact met [open source gemeenschappen](#gerelateerde-hulpmiddelen) voor advies.

### 2. Ontwikkelen, ontwerpen en inkopen

Werk open vanaf dag 1: begin met een publieke repository vanaf het start van je project. Dit voorkomt kostbare retrofitting en bevordert incrementele security improvements. Kies een geschikte open source licentie (bij voorkeur EUPL-1.2 voor overheidscode).

**Praktische tips voor ontwikkelen en ontwerpen**

- **Start met een publieke repository** - Begin vanaf dag 1 met een publieke GitHub of GitLab repository.
- **Kies EUPL-1.2 licentie** - De aanbevolen licentie voor Nederlandse overheidscode. Zie [licentieadvies](https://opensourcewerken.nl/page/view/677bb847-79b5-42b2-8a63-e7bb2e074530/softwarelicenties) voor meer informatie.
- **Gebruik secrets management** - Sla wachtwoorden, API-keys en credentials op in een apart systeem en nooit in de code zelf (bijv. HashiCorp Vault, Azure Key Vault).
- **Schrijf een goede README** - Leg uit wat de code doet, hoe je het installeert en hoe je kunt bijdragen. Zie voorbeelden bij [MinBZK](https://github.com/MinBZK) en [Gemeente Amsterdam](https://github.com/amsterdam) repositories.
- **Maak een CONTRIBUTING.md** - Geef duidelijke richtlijnen voor externe bijdragen. Zie [Developer.overheid.nl](https://developer.overheid.nl/kennisbank/open-source/standaarden/contributing-md#wat-neem-je-erin-op) voor hoe je dat kan doen.
- **Creëer een veilige en inclusieve omgeving voor contributors** - Definieer een [Code of Conduct](https://developer.overheid.nl/kennisbank/open-source/standaarden/code-of-conduct-md).
- **Gebruik [open standaarden](https://www.forumstandaardisatie.nl/open-standaarden)** - Zorg dat je architectuur interoperabel is (zie Gebruik open standaarden (skill `/nerds-standaarden`)).
- **Documenteer ontwerpbeslissingen** - Leg vast waarom je bepaalde technologiekeuzes maakt. Gebruik hiervoor bijvoorbeeld een [Architectural Decision Record van Gov UK](https://www.gov.uk/government/publications/architectural-decision-record-framework/architectural-decision-record-framework).

**Praktische tips voor inkopen**

- **Neem Standaarden op in de inkoopvoorwaarde** - Zie de [Instructie Rijksdienst bij aanschaf ICT-diensten of ICT-producten](https://wetten.overheid.nl/BWBR0024717/2008-11-23) en [Opensource Gereedschapskist voor het aanbesteden van standaardsoftware VWS](https://minvws.opensourcewerken.nl/open-source-gereedschapskist-voor-het-aanbesteden-van-standaardsoftware/).
- **Controleer de maturiteit** - Is het project actief onderhouden en stabiel?
- **Evalueer de community** - Is er een actieve gemeenschap of commerciële ondersteuning?
- **Check de veiligheid** - Bekijk de security geschiedenis en updatefrequentie.
- **Beoordeel vendor lock-in risico's** - Vermijd afhankelijkheid van één leverancier en zorg voor een exit-strategie.
- **Begrijp de licentie** - Zorg dat je de verplichtingen kent. Zie [licentieadvies](https://opensourcewerken.nl/page/view/677bb847-79b5-42b2-8a63-e7bb2e074530/softwarelicenties).
- **Vraag naar gebruikerservaringen** - Gebruiken andere overheidsorganisaties dit al? Vraag het op [Developer Overheid](https://developer.overheid.nl/).

### 3. Testen, meten en verbeteren

Onderhoud je open source project actief: Reageer snel op security issues, monitor dependencies op kwetsbaarheden en wees transparant over je onderhoudsniveau. Open source publiceren is een langetermijncommitment, alloceer voldoende resources voor community management.

**Praktische tips**

- **Review code op secrets** - Scan regelmatig op hard-coded wachtwoorden en credentials.
- **Monitor security advisories** - Volg CVE's (Common Vulnerabilities and Exposures) en security updates voor je dependencies. Zoals [dependabot](https://github.com/dependabot).
- **Reageer snel op security issues** - Patch kritieke kwetsbaarheden binnen 24-48 uur.
- **Test installeerbaarheid** - Doe regelmatig een fresh clone test met een nieuwe gebruiker.
- **Communiceer onderhoudsniveau** - Wees duidelijk over of het digitale systeem "actively maintained", "maintenance mode" of "archived" is.
- **Gebruik Semantic Versioning** - Versies in [major.minor.patch](https://semver.org/) formaat voor duidelijkheid.
- **Draag bij aan upstream** - Geef terug aan projecten waar je van afhankelijk bent.
- **Deel je bevindingen** - Publiceer blogposts en presentaties over je ervaringen. Deel kennis via de [opensourcewerken community](https://developer.overheid.nl/communities/open-source-werken).

## Implementatie per fase

Zie [Open source: wanneer doe je wat?](fases.md).

## Gerelateerde hulpmiddelen

### Naslagwerk

- [Git commit guidelines](https://ec.europa.eu/component-library/v1.14.2/ec/docs/conventions/git/) - Europese richtlijnen voor het maken van commit messages.
- [Developer Amsterdam](http://developers.amsterdam) -
- [Service Manual 'Making source code open and reusable'](https://www.gov.uk/service-manual/technology/making-source-code-open-and-reusable) - Vanuit GOV UK.

### Beleid, wetten en standaarden

- [Beleid Opensourcewerken - Digitale Overheid](https://www.digitaleoverheid.nl/overzicht-van-alle-onderwerpen/open-source/beleid/) - Het officiële open-tenzij beleid van de Nederlandse overheid
- [Instructie Rijksdienst bij aanschaf ICT-diensten of ICT-producten](https://wetten.overheid.nl/BWBR0024717/2008-11-23) - Officiële instructie die open standaarden voorschrijft bij ICT-aanschaf
- [EUPL-1.2 Licentie](https://interoperable-europe.ec.europa.eu/collection/eupl/eupl-text-eupl-12) - European Union Public Licence, aanbevolen voor overheidscode
- [Softwarelicenties - Opensourcewerken](https://opensourcewerken.nl/page/view/677bb847-79b5-42b2-8a63-e7bb2e074530/softwarelicenties) - Overzicht van open source licenties en overwegingen

### Communities

- [Opensourcewerken community](https://developer.overheid.nl/communities/open-source-werken) - Community van het Ministerie van Binnenlandse Zaken voor praktische kennis, een forum om ervaringen te delen en informatie over relevante regelgeving
- [Code for NL](https://developer.overheid.nl/communities/code-for-nl) - Code for NL is een netwerk van developers, designers en andere experts die samenwerken aan digitale toepassingen voor een open, eerlijke en inclusieve samenleving.
- [Common Ground](https://developer.overheid.nl/communities/common-ground) - Gemeenten werken samen met een community van betrokkenen partijen aan bouwstenen, zoals softwaretoepassingen, technische componenten of standaarden voor gegevensuitwisseling.

### Boeken

- **Platformland** - Richard Pope - *An anatomy of next-generation public services*
- **[Producing Opensource Software](https://producingoss.com/)** - Karl Fogel - *About the human side of open source development.*

## Gerelateerde richtlijnen

- 4. Gebruik open standaarden (skill `/nerds-standaarden`)
- 6. Maak veilige systemen (skill `/nerds-veiligheid`)
- 8. Deel, hergebruik en werk samen (skill `/nerds-samenwerking`)
