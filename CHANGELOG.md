# Journal des versions

Format : [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/). Les numéros suivent [SemVer](https://semver.org/lang/fr/), et la version de `pyproject.toml` est égale au tag.

## [Non publié]

### Corrigé
- **Détection des modèles 5510 HI / 5520 HI** (#66) : `detect_model` reconnaît la ligne châssis réelle (« HPE 5510 24G 4SFP+ HI 1-slot Switch », « HPE 5520 24G 4SFP+ HI Swch »). Les alias collés (`5510HI`) ne correspondaient qu'aux noms des fichiers d'image, si bien que la détection échouait dès que les images étaient renommées. Trois sorties `display version` réelles servent désormais de fixtures (`tests/fixtures/display_version/`).

### Modifié
- **Licence** (#105) : le `LICENSE` MIT provisoire est remplacé par le texte officiel de la GPLv3, et le projet passe en GPL-3.0-or-later. Ajouts : `license` dans `pyproject.toml`, en-têtes SPDX, `License: GPL-3.0-or-later` et `%license LICENSE` dans le spec RPM, `copyright` DEP-5 installé par le `.deb`, section Licence du README avec les licences des dépendances, `tests/test_licence.py`.

### Ajouté
- Règles de protection versionnées `.github/branch-protection/{main,dev}.json` (relevées sur la protection réelle du 22/10/2026), vérifiées par le workflow `branch-protection.yml` (push sur main/dev, chaque jour) et `scripts/check_branch_protection.py` (socle Mathilde-Team/.github#1, #96).

## [1.0.0] - 2026-10-22

Première version publiée sous forme de release GitHub.

### Ajouté
- **Workflow de release** (#92) : `.github/workflows/release.yml` publie une release GitHub au push d'un tag `vX.Y.Z` sur `main` (tag = version de `pyproject.toml`, notes tirées de la section `## [X.Y.Z]` de ce journal, archive des sources jointe).
