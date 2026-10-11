---
title: "5. Gebruik cloud verantwoord en blijf wendbaar"
summary: Kies bewust waar je systeem draait en houd zelf de zeggenschap over je data en je infrastructuur.
icon: cloud
relations:
  - veiligheid
  - privacy
  - duurzaamheid
  - inkoop
---

# 5. Gebruik cloud verantwoord en blijf wendbaar

Kies bij elk nieuw of te vernieuwen systeem bewust waar het draait en wie daar zeggenschap over heeft. Ontwerp zo dat je kunt overstappen als de leverancier, het aanbod of het beleid verandert. Cloud biedt de overheid voordelen en het gebruik is toegestaan, binnen kaders. Het [Rijksbrede Cloudbeleid 2026](https://www.tweedekamer.nl/downloads/document?id=2026D35295){:target="_blank"} raadt een generiek "cloud-tenzij"-beleid af, en het kabinet heeft in de [Kamerbrief Verkenning soevereine overheidscloud](https://www.tweedekamer.nl/kamerstukken/brieven_regering/detail?id=2026Z15306&did=2026D34379){:target="_blank"} zijn voorkeur uitgesproken voor een soevereine overheidscloud.

## Waarom is het belangrijk?

- **Continuïteit in eigen hand**: dienstverlening mag niet stilvallen omdat een leverancier wordt overgenomen, een dienst stopzet of onder druk komt van een buitenlandse overheid.
- **Jurisdictie volgt de leverancier**: valt de leverancier of het moederbedrijf onder wetgeving van buiten de EU, dan kan die ook gelden voor gegevens in een Europees datacenter.
- **Minder afhankelijkheid**: de markt concentreert zich bij een kleine groep bedrijven. Bij 67% van de materiële publieke clouddiensten van het Rijk ontbrak in 2025 de verplichte risicoafweging, stelde de Algemene Rekenkamer vast.
- **Kennis in eigen huis**: goed cloudgebruik vraagt eigen mensen die veiligheid, beschikbaarheid en variabele kosten kunnen beoordelen.

## Wat geldt er nu?

Een samenvatting, stand oktober 2026. De beleidsteksten zelf zijn leidend.

### Rijksoverheid

De [Herziening Rijksbreed Cloudbeleid 2026](https://www.tweedekamer.nl/kamerstukken/brieven_regering/detail?id=2026Z15738&did=2026D35294){:target="_blank"} geldt voor de hele Rijksoverheid, behalve de Hoge Colleges van Staat en Defensie. Zelfstandige bestuursorganen volgen het beleid, andere overheden krijgen het advies dat te doen. Het vraagt om waar mogelijk soevereine of Europese cloudoplossingen te gebruiken.

Bij materieel cloudgebruik (voor de kerntaak van je organisatie, of bij grootschalige verwerking van persoonsgegevens) regel je:

- een integrale risicobeoordeling volgens het [implementatiekader](https://open.overheid.nl/documenten/ronl-734f947ec6465e4f75a56bed82fe64a1135f71a8/pdf){:target="_blank"}, dat wordt herzien;
- een zelf getoetst exitplan voor een geplande overstap en voor een onverwachte uitval, jaarlijks geactualiseerd;
- een melding aan CISO Rijk vóór de implementatie, en registratie van het gebruik.

Voor al het cloudgebruik geldt:

- opslag en verwerking binnen de EER en Zwitserland, versleuteld, met het sleutelbeheer bij voorkeur in eigen hand;
- e-mail en documenten niet in de publieke cloud, behalve onder drie voorwaarden waaronder akkoord van de minister;
- bijzondere persoonsgegevens bij voorkeur niet in de publieke cloud;
- geen publieke cloud voor staatsgeheim gerubriceerde informatie, TBB-niveau 1 tot en met 3 en de brondata van basisregistraties;
- kritieke en essentiële entiteiten krijgen het advies om voor hun primaire proces geen leverancier te gebruiken die (deels) onder een jurisdictie buiten de EU of de EER valt.

Bestaand gebruik heeft een overgangstermijn van vier jaar. Het exitplan moet er binnen twaalf maanden zijn.

### Soevereine overheidscloud

Het kabinet sprak op 1 juli 2026 in de [Kamerbrief Verkenning soevereine overheidscloud](https://www.tweedekamer.nl/kamerstukken/brieven_regering/detail?id=2026Z15306&did=2026D34379){:target="_blank"} zijn voorkeur uit voor een nieuwe soevereine overheidsclouddienst onder centrale regie, gebouwd op open source en waar mogelijk gehuisvest in de overheidsdatacenters. Sinds 31 augustus 2026 ligt [Het Ontwerp](https://www.digitaleoverheid.nl/nieuws-nds/nds-cloud-mijlpaal-publicatie-van-het-ontwerp/){:target="_blank"} van de clouddienst voor openbare review. Governance, bekostiging en inkoop volgen later. De proof of concept is een doorbraaktraject van de [Nederlandse Digitale Dienst](https://digitaledienst.overheid.nl/){:target="_blank"} en draait op [Fundament](https://docs.fundament.projects.digilab.network/){:target="_blank"}, een open source platform met openbare documentatie en broncode.

### Gemeenten

De [VNG-handreiking Eisen aan gemeentelijke Cloudvoorzieningen (pdf)](https://vng.nl/sites/default/files/2026-07/handreiking-cloud-voor-gemeenten.pdf){:target="_blank"} hanteert "EU-by-design": niet-Europese leveranciers alleen als een volwaardig Europees alternatief ontbreekt, en dan tijdelijk. De handreiking bevat een programma van eisen voor aanbestedingen.

### Europa

Het [EU Cloud Sovereignty Framework](https://commission.europa.eu/document/09579818-64a6-4dd5-9577-446ab6219113_en){:target="_blank" lang="en"} deelt clouddiensten in op de niveaus SEAL-0 tot en met SEAL-4. Het cloudbeleid noemt het als hulpmiddel bij de leveranciersselectie.

## Hoe pas je het toe?

<div class="direct-aan-de-slag">
    <h3>Direct aan de slag</h3>

    <div class="warning-banner">
        <strong>In ontwikkeling:</strong> De onderstaande functionaliteit is nog in ontwikkeling.
    </div>

    <div class="action-cards" data-richtlijn="cloud"></div>
</div>

## Bewezen praktijken

### 1. Begrijpen

Begin bij wat je functioneel wilt bereiken; cloud is een middel. Hoe gevoelig je gegevens zijn en hoe kritiek je processen, bepaalt waar je systeem mag draaien.

??? expander "Praktische tips"
    - **Start met de behoefte** - Formuleer wat je functioneel wilt bereiken voordat je over technologie nadenkt.
    - **Geen cloud-tenzij** - Leg in je cloudstrategie vast wanneer cloud de voorkeur heeft, welke voordelen je verwacht en hoe je die borgt.
    - **Classificeer je toepassing en data** - Ga uit van BIV-eisen of TBB-niveau. Gemeenten gebruiken de soevereiniteitsniveaus uit de [VNG-handreiking Eisen aan gemeentelijke Cloudvoorzieningen (pdf)](https://vng.nl/sites/default/files/2026-07/handreiking-cloud-voor-gemeenten.pdf){:target="_blank"}.
    - **Voer de risicoanalyse uit** - Met een [DPIA](https://autoriteitpersoonsgegevens.nl/themas/basis-avg/praktisch-avg/data-protection-impact-assessment-dpia){:target="_blank"} en waar nodig een [DTIA](https://www.autoriteitpersoonsgegevens.nl/themas/internationaal/doorgifte-binnen-en-buiten-de-eer/doorgifte-persoonsgegevens-buiten-de-eer){:target="_blank"}. Leg het restrisico vast en laat het formeel accepteren.
    - **Beoordeel de jurisdictie, niet alleen de locatie** - Vraag onder welk recht de leverancier en het moederbedrijf vallen.
    - **Kijk ook naar wat de overheid zelf biedt** - Weeg je keuze af tegen een overheidsdatacenter of een gedeelde overheidsvoorziening, en volg de ontwikkeling van [Fundament](https://docs.fundament.projects.digilab.network/){:target="_blank"}.
    - **Vermijd lift-en-shift** - Migreren zonder passende architectuur levert zelden de verwachte voordelen op en wel nieuwe risico's.
    - **Vertel het verhaal** - Leg bestuurders uit welke continuïteitsrisico's je ziet en welke keuze je daarom maakt.

### 2. Ontwikkelen, ontwerpen en inkopen

Koppel applicatie en data los van het onderliggende platform, zodat je kunt verhuizen als dat nodig is. Open source en open standaarden zijn daarvoor de basis (zie [Werk transparant en gebruik open source](../open-source/index.md){:target="_blank"}).

Ontwikkelen & ontwerpen
??? expander "Praktische tips"
    - **Bouw op open source en open standaarden** - Kies componenten die op meerdere platformen draaien, zoals [Kubernetes](https://kubernetes.io/){:target="_blank"} volgens de [Haven-standaard](https://haven.commonground.nl/){:target="_blank"}. Isoleer diensten die maar bij één leverancier bestaan achter een eigen interface.
    - **Ontwerp je exit vanaf dag één** - Dek een geplande overstap en een onverwachte uitval af, met een back-up buiten de cloudomgeving van dezelfde leverancier.
    - **Zet je infrastructuur in code** - Met Infrastructure as Code, bijvoorbeeld [OpenTofu](https://opentofu.org/){:target="_blank"}, en [GitOps](https://opengitops.dev/){:target="_blank"} bouw je een omgeving elders opnieuw op.
    - **Versleutel en beheer je eigen sleutels** - Bewaar ook wachtwoorden en certificaten buiten je code, bijvoorbeeld met [OpenBao](https://openbao.org/){:target="_blank"}.
    - **Houd identity in eigen hand** - Wie de identiteiten beheert, heeft de sleutel tot alles.
    - **Ontwerp op falen** - Definieer SLO's en SLI's en ga ervan uit dat systemen uitvallen. Zie het [Google SRE Book](https://sre.google/books/){:target="_blank"}.
    - **Bouw kennis op in je eigen organisatie** - Zorg dat eigen mensen het platform begrijpen en kunnen bedienen.
    - **Beveilig en borg privacy vanaf het ontwerp** - Zie [Maak veilige systemen](../veiligheid/index.md){:target="_blank"} en [Maak privacy integraal](../privacy/index.md){:target="_blank"}.

Inkopen
??? expander "Praktische tips"
    - **Volg het cloudbeleid** - Meld materieel cloudgebruik vooraf bij CISO Rijk. Wijk je af van het beleid, meld dat dan vooraf bij CIO Rijk.
    - **Kies soeverein of Europees waar het kan** - Leg bij een niet-Europese leverancier vast hoe je eruit komt.
    - **Stel soevereiniteitseisen** - Vraag naar eigendom, toepasselijk recht, de locatie van data en beheer, en wat er gebeurt bij een overname. Met de SEAL-niveaus vergelijk je de antwoorden.
    - **Leg de exit contractueel vast** - Regel de overdracht van data en applicaties bij beëindiging en de vernietiging daarna.
    - **Vergelijk de totale kosten** - Reken migratie, training, dataverkeer naar buiten en exit mee, en reken ook het alternatief in een overheidsdatacenter door.
    - **Stel dezelfde eisen aan jezelf** - Wat je van een leverancier vraagt, geldt ook voor je eigen organisatie.
    - **Controleer compliance en duurzaamheid** - Vraag naar certificeringen en energieverbruik (zie [Maak je technologie duurzaam](../duurzaamheid/index.md){:target="_blank"}).

### 3. Testen, meten en verbeteren

Een exitplan dat nooit is geoefend, is een aanname. Het aanbod en het beleid veranderen snel, dus herijk ook je keuze voor het platform.

??? expander "Praktische tips"
    - **Oefen je exit en je herstel** - Test de overstap, de noodprocedure en je back-ups, ook voor het geval dat de hele cloudomgeving onbereikbaar is.
    - **Houd je cloudgebruik bij** - Registreer welke diensten je voor welke verwerkingen gebruikt en bij welke leverancier.
    - **Herijk je afhankelijkheden** - Kijk periodiek of er een Europees of soeverein alternatief is gekomen, en of eigenaarschap of jurisdictie van je leverancier is veranderd.
    - **Beheers de kosten** - Stel budgetlimieten in en betrek finance en engineering bij cloudbeslissingen. Zie de [FinOps Foundation](https://www.finops.org/){:target="_blank"}.
    - **Monitor beveiliging en prestaties** - Bewaak je omgeving, meet tegen je SLO's en voer regelmatig audits uit.
    - **Deel wat je leert** - Publiceer ervaringen binnen de overheid.

## Implementatie per fase

Zie [Cloud: wanneer doe je wat?](fases.md).

## Gerelateerde hulpmiddelen

### Beleid en kaders

- [Herziening Rijksbreed Cloudbeleid 2026](https://www.tweedekamer.nl/kamerstukken/brieven_regering/detail?id=2026Z15738&did=2026D35294) - Kamerbrief van 3 juli 2026, met het [beleidsdocument](https://www.tweedekamer.nl/downloads/document?id=2026D35295)
- [Kamerbrief Verkenning soevereine overheidscloud](https://www.tweedekamer.nl/kamerstukken/brieven_regering/detail?id=2026Z15306&did=2026D34379) - 1 juli 2026
- [Implementatiekader risicoafweging](https://open.overheid.nl/documenten/ronl-734f947ec6465e4f75a56bed82fe64a1135f71a8/pdf) - Kader voor de risicoafweging bij cloudgebruik
- [VNG-handreiking Eisen aan gemeentelijke Cloudvoorzieningen (pdf)](https://vng.nl/sites/default/files/2026-07/handreiking-cloud-voor-gemeenten.pdf) - met programma van eisen
- [EU Cloud Sovereignty Framework](https://commission.europa.eu/document/09579818-64a6-4dd5-9577-446ab6219113_en){: lang="en" } - Europese soevereiniteitsniveaus SEAL-0 tot en met SEAL-4
- [Nederlandse Digitaliseringsstrategie (NDS) prioriteit Cloud](https://www.digitaleoverheid.nl/nederlandse-digitaliseringsstrategie-nds/6-prioriteiten-voor-een-overheid/prioriteit-1-cloud/){:target="_blank"}
- [Visie digitale autonomie en soevereiniteit van de overheid](https://www.rijksoverheid.nl/documenten/rapporten/2025/12/18/bijlage-2-visie-digitale-autonomie-en-soevereiniteit-van-de-overheid) - Rijksbrede visie
- [BIO (Baseline Informatiebeveiliging Overheid)](https://www.digitaleoverheid.nl/overzicht-van-alle-onderwerpen/cybersecurity/bio-en-ensia/) - Beveiligingsnormen overheid

### Naslagwerk

- [Fundament](https://docs.fundament.projects.digilab.network/) - Open source platform waarop de proef met de soevereine overheidscloud draait
- [Haven](https://haven.commonground.nl/) - Standaard voor platformonafhankelijke cloudhosting op Kubernetes
- [Het Rijk in de cloud](https://www.rekenkamer.nl/publicaties/rapporten/2025/01/15/het-rijk-in-de-cloud) - Rapport van de Algemene Rekenkamer
- [Marktstudie clouddiensten](https://www.acm.nl/nl/publicaties/marktstudie-clouddiensten) - ACM over overstapdrempels in de cloudmarkt
- [NORA](https://www.noraonline.nl/wiki/Cloud_computing) - Architectuurprincipes overheid
- [Cloud Native Computing Foundation](https://www.cncf.io/) - Open source projecten voor cloud-native werken

### Communities en trainingen

- [Nederlandse Digitale Dienst](https://digitaledienst.overheid.nl/) - Werkt met overheidsorganisaties aan doorbraakprojecten, waaronder de soevereine overheidscloud
- [Common Ground](https://developer.overheid.nl/communities/common-ground) - Gemeenten werken samen aan herbruikbare bouwstenen
- [Dutch Cloud Commmunity](https://dutchcloudcommunity.nl/){:target="_blank"} - Branchevereniging voor de Nederlandse cloud- en internetsector
- [GGI-Cloud Expertisecentrum](https://vng.nl/nieuws/ggi-cloud-expertisecentrum-helpt-gemeentelijke-transitie) - Ondersteuning voor gemeenten
- [RADIO](https://www.it-academieoverheid.nl/onderwerpen/c/cloud-computing/cursussen-cloud) - Cloudtrainingen voor rijksambtenaren
- [Linux Foundation Training](https://training.linuxfoundation.org/resources/) - Cursussen over Kubernetes en cloud-native

## Gerelateerde richtlijnen

- [6. Maak veilige systemen](../veiligheid/index.md){:target="_blank"}
- [7. Maak privacy integraal](../privacy/index.md){:target="_blank"}
- [12. Definieer je inkoopstrategie](../inkoop/index.md){:target="_blank"}
- [13. Maak je technologie duurzaam](../duurzaamheid/index.md){:target="_blank"}
