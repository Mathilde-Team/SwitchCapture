# Journal des versions

Format : [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/). Les numéros suivent [SemVer](https://semver.org/lang/fr/), et la version de `pyproject.toml` est égale au tag.

## [Non publié]

- CI et publication : repli GitHub autorisé, publication manuelle sur un tag
  déjà livré dans main, vérification d’ascendance et archives du tag exact.


### Modifié
- **Licence** (#105) : le `LICENSE` MIT provisoire est remplacé par le texte officiel de la GPLv3, et le projet passe en GPL-3.0-or-later. Ajouts : `license` dans `pyproject.toml`, en-têtes SPDX, `License: GPL-3.0-or-later` et `%license LICENSE` dans le spec RPM, `copyright` DEP-5 installé par le `.deb`, section Licence du README avec les licences des dépendances, `tests/test_licence.py`.

### Ajouté
- Règles de protection versionnées `.github/branch-protection/{main,dev}.json` (relevées sur la protection réelle du 22/10/2026), vérifiées par le workflow `branch-protection.yml` (push sur main/dev, chaque jour) et `scripts/check_branch_protection.py` (socle Mathilde-Team/.github#1, #96).

## [1.0.0] - 2026-10-22

Première version publiée sous forme de release GitHub.

### Ajouté
- **Workflow de release** (#92) : `.github/workflows/release.yml` publie une release GitHub au push d'un tag `vX.Y.Z` sur `main` (tag = version de `pyproject.toml`, notes tirées de la section `## [X.Y.Z]` de ce journal, archive des sources jointe).
