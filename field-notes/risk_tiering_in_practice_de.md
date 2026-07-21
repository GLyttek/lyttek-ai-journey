# Risk Tiering in der Praxis: Was funktioniert hat und was nicht

*Eine persönliche Feldnotiz aus einem lokalen, menschlich kontrollierten Agenten- und Wissenssystem. Kein organisationsweiter Wirksamkeitsnachweis.*

## Die Idee war einfacher als die Einführung

Als ich begann, Agenten nicht nur lesen und schreiben, sondern auch Werkzeuge benutzen zu lassen, brauchte ich eine gemeinsame Sprache für Grenzen. Daraus entstand eine einfache Matrix:

- Green für Lesen, Recherche und neue lokale Entwürfe;
- Yellow für Änderungen an bestehendem Zustand;
- Red für Veröffentlichung, Systemänderung, Automatisierung und andere folgenreiche Aktionen;
- Black für Dinge, die auch mit Zustimmung nicht passieren dürfen, etwa Secrets auszugeben oder Schutzgrenzen zu umgehen.

Die Einteilung sah auf Papier sauber aus. In der Praxis zeigte sich schnell, dass ein Task keine Farbe besitzt. **Eine Handlung besitzt eine Wirkung.**

Eine Videorecherche kann Green beginnen, Yellow werden, sobald ein bestehender Index geändert wird, und Red enden, wenn der fertige Artikel auf eine öffentliche Website übertragen wird. Wer dem gesamten Vorhaben nur am Anfang ein Label gibt, verliert genau den Übergang, an dem Kontrolle wichtig wird.

## Der erste Erfolg war keine perfekte Klassifikation

Der erste wirkliche Nutzen bestand darin, dass folgenreiche Aktionen sichtbar blieben. Löschen, Publizieren, wiederkehrende Automatisierung, Änderungen außerhalb des Arbeitsraums und Eingriffe in Sicherheitskonfigurationen verschwanden nicht mehr in der Mitte eines langen Agentenlaufs.

Das klingt bescheiden. Es ist aber ein wesentlicher Unterschied zwischen einer Checkliste und einer Arbeitsweise. Ein Agent kann viele harmlose Schritte ausführen und trotzdem an der Grenze zu einer anderen Wirkung stoppen.

Die Matrix half außerdem, Receipts lesbarer zu machen. Spätere Reviews konnten erkennen:

- welche Aktion vorgesehen war;
- warum sie einer höheren Klasse zugeordnet wurde;
- welche Freigabe vorlag;
- welche Verifikation danach tatsächlich stattfand.

Risk Tiering wurde damit weniger zu einer Vorhersage und mehr zu einem Routing-System.

## Die erste Schwierigkeit war Scope

„Datei ändern“ ist als Risikoklasse zu grob. Eine neue Markdown-Datei im Arbeitsbereich ist nicht dasselbe wie eine Änderung an einer Service-Konfiguration. Ein lokaler HTML-Entwurf ist nicht dasselbe wie sein Upload. Ein Testlauf mit synthetischen Daten ist nicht dasselbe wie das Indexieren privater Inhalte.

Die Klassifikation brauchte deshalb zusätzliche Dimensionen:

```text
Aktion
Ziel
Datenklasse
Empfänger oder Umgebung
Reversibilität
Blast Radius
benötigte Identität
Nachweis nach der Aktion
```

Erst diese Felder machen aus „Yellow“ oder „Red“ eine brauchbare Grenze.

## Modelle klassifizieren nicht zuverlässig genug

Ein früher lokaler Smoke-Test zeigte die Schwäche direkt. Ein Modell sollte harmlose Lesezugriffe, das Erstellen eines freigegebenen lokalen Modells, das Löschen von Modellen und das Ausgeben von API-Schlüsseln einordnen. In einem Lauf stufte es die Modellerstellung zu niedrig ein und behandelte die Ausgabe von Secrets nicht als unverhandelbar verboten. Ein späterer Lauf bestand denselben Test.

Das ist keine belastbare Modellstudie. Es war ein kleiner lokaler Test mit wenigen Fällen. Für meine Architektur reichte die Beobachtung trotzdem:

> Ein Modell kann eine Risikoklasse vorschlagen. Es darf die daraus folgenden Rechte nicht selbst vergeben.

Die endgültige Durchsetzung muss in Tool-Policy, Dateigrenzen, Credential-Brokern, Repository-Regeln und Deployment-Gates liegen.

## Die zweite Schwierigkeit war Approval Fatigue

Eine Sicherheitsmatrix kann leicht zu viele Rückfragen erzeugen. Wenn jede kleine Änderung mit demselben Dialog endet, lernt der Mensch nicht, genauer hinzusehen. Er lernt, schneller zu bestätigen.

Der Ausweg war nicht weniger Kontrolle, sondern genauerer Scope. Eine gute Freigabe bündelt harmlose Schritte innerhalb einer verständlichen Grenze. Sie fragt erneut, wenn sich etwas Wesentliches ändert:

- ein neuer Empfänger;
- eine neue Datenklasse;
- ein produktives Ziel;
- ein externer Seiteneffekt;
- eine irreversible Aktion;
- ein deutlich größerer Änderungsumfang.

„Darf ich fortfahren?“ ist dafür zu schwach. Eine brauchbare Freigabe sagt, was mit welchen Daten auf welchem Ziel passieren soll und wie lange diese Erlaubnis gilt.

## Die dritte Schwierigkeit war die Vermischung von Inhalt und Wirkung

Security-Recherche kann Dual-Use-Inhalte enthalten, ohne selbst ein System zu verändern. Eine harmlose Dokumentation kann dagegen private Pfade oder interne Details veröffentlichen. Der Inhalt eines Tasks und seine operative Wirkung sind zwei verschiedene Achsen.

Deshalb prüfe ich inzwischen getrennt:

1. Welche Informationen werden verarbeitet?
2. Welche Aktion darf das System ausführen?
3. Welche Grenze überschreiten Daten oder Effekte?
4. Wie wird das Ergebnis unabhängig verifiziert?

Diese Trennung verhindert, dass ein „defensives“ Thema automatisch als operativ harmlos gilt oder eine „nur redaktionelle“ Änderung ohne Veröffentlichungskontrolle bleibt.

## Was sich bewährt hat

### Die höchste Wirkung gewinnt

Bei zusammengesetzten Aufgaben bestimmt nicht der bequemste Teilschritt die Kontrolle. Recherche kann frei laufen. Der spätere Push oder Upload bleibt trotzdem ein eigener Gate.

### Dynamische Neuklassifikation

Wenn der Plan nach einem Fehler einen anderen Dienst, eine breitere Dateioperation oder einen neuen Empfänger benötigt, wird neu klassifiziert. Die alte Freigabe wächst nicht mit.

### Risikoklasse plus Begründung

Ein Label ohne Begründung ist schwer kalibrierbar. Die nützliche Form lautet beispielsweise:

> Red, weil der Schritt öffentlich veröffentlicht, einen externen Zustand verändert und nur durch Backup sowie verifizierten Rückdownload sicher abgeschlossen werden kann.

### Proof of Done

Die Klasse bestimmt nicht nur, wer vorher zustimmt. Sie bestimmt auch, welcher Nachweis danach nötig ist. Bei einer lokalen Notiz reicht ein Dateicheck. Bei einem Upload brauche ich Backup, Hashvergleich, HTTPS-Prüfung und ein Receipt. Bei GitHub brauche ich Commit, Remote-Readback und erfolgreiche Repository-Checks.

### Black bleibt Black

Nicht jede Aktion wird durch Zustimmung legitim. Secret-Ausgabe, Umgehung von Schutzregeln und nicht autorisierte offensive Nutzung gehören nicht in eine höhere Freigabestufe. Sie bleiben ausgeschlossen.

## Was noch nicht gelöst ist

Meine Matrix ist lokal gewachsen. Sie ist weder statistisch validiert noch automatisch in jeder Tool-Kette durchgesetzt. Einige Grenzen leben weiterhin in Arbeitsregeln und menschlicher Aufmerksamkeit. Das ist besser als unsichtbare Vollmacht, aber noch kein vollständiges Policy-System.

Offen bleiben insbesondere:

- konsistente Klassifikation über verschiedene Agenten und Modelle;
- maschinenlesbare Bindung von Freigaben an exakte Parameter;
- systemweite Egress- und Datenklassifikationskontrolle;
- Messung von Fehlklassifikationen und unnötigen Eskalationen;
- Kalibrierung gegen reale Near Misses statt nur gegen entworfene Beispiele;
- Widerruf laufender, abgeleiteter Berechtigungen.

## Mein heutiges Modell

Ich behandle Risk Tiering als Steuerung der Kontrolltiefe:

| Stufe | Typische Wirkung | Kontrolltiefe |
|---|---|---|
| Observe | lesen und erklären | Provenienz, keine Seiteneffekte |
| Draft | isoliert neu erzeugen | Pfadgrenze, keine Veröffentlichung |
| Change | bestehenden Zustand ändern | Diff, Tests, Review, Rollback |
| Execute | operatives Tool nutzen | taskgebundene Identität, Policy, Trace |
| Publish/Deploy | öffentlich oder produktiv wirken | exakte Freigabe, Artefaktbindung, Readback |

Die Farbnamen sind austauschbar. Entscheidend ist, dass jede Stufe konkrete technische Kontrollen und einen passenden Proof of Done besitzt.

## Der wichtigste Erfolg

Risk Tiering hat meine Agenten nicht „sicher“ gemacht. Das wäre eine zu große Behauptung.

Es hat etwas Praktischeres geschafft. Es hat die Stellen sichtbar gemacht, an denen ein flüssiger Arbeitsablauf seine Bedeutung ändert. Aus Lesen wird Schreiben. Aus Entwurf wird Veröffentlichung. Aus Empfehlung wird Systemzustand. Aus plausibler Antwort wird eine Aktion, für die jemand Verantwortung übernehmen muss.

Genau dort gehört die Grenze hin.

## Quellen und Evidenz

- [NIST AI RMF 1.0](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10) unterstützt risikobasierte Priorisierung, schreibt aber keine konkrete lokale Farblogik vor.
- [NIST Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence) empfiehlt unter anderem risikoadäquate Governance, Rollen, Tests und Monitoring.
- [OWASP AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html) empfiehlt risikobasierte Autonomiegrenzen und unabhängige Kontrolle hochwirksamer Aktionen.
- Die beschriebenen Erfolge und Schwierigkeiten sind lokale Beobachtungen aus einem persönlichen Proof of Concept. Sie belegen keine allgemeine Wirksamkeitsquote.
