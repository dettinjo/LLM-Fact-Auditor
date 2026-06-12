<!-- portfolio:date=2024-10-14 -->

[Deutsch](README.de.md) · [English](README.md)

# LLM Fact Auditor

Eine fortgeschrittene Post-Processing-Pipeline, die im Rahmen des Kurses "Web Data Processing Systems" an der Vrije Universiteit Amsterdam entwickelt wurde. Das System prüft automatisch die Fakten, verlinkt Entitäten und verifiziert Antworten von Large Language Models (LLMs) anhand strukturierter Wissensbasen.

<p align="center">
  <img src="docs/pytorch.svg" alt="Pytorch" width="170" />
</p>

### Die Herausforderung

LLMs neigen dazu, plausibel klingende, aber sachlich falsche Informationen zu generieren. Dieses Projekt entwickelt eine robuste Pipeline, die LLM-Ausgaben systematisch gegen Wikidata und andere strukturierte Quellen überprüft.

### Kernfunktionen

- **Entitätserkennung** mit spaCy und Stanza zur Identifikation von Personen, Orten und Konzepten
- **Wikidata-Verknüpfung** zur Zuordnung erkannter Entitäten zu verifizierbaren Wissensgraphen-Einträgen
- **Faktenprüfung** durch Abgleich von LLM-Behauptungen mit strukturierten Wissensbasen
- **LLM-Integration** mit Meta Llama für die Antwortgenerierung
- **Docker-Containerisierung** für reproduzierbare Ausführungsumgebungen

### Technischer Aufbau

Die Pipeline verarbeitet Eingabefragen durch mehrere spezialisierte Module: Zunächst generiert das LLM eine Antwort, die anschließend durch Named-Entity-Recognition verarbeitet wird. Erkannte Entitäten werden mit Wikidata verknüpft und gegenüber bekannten Fakten überprüft. Das Ergebnis ist eine strukturierte Ausgabe mit Vertrauensbewertungen für jede Behauptung.
