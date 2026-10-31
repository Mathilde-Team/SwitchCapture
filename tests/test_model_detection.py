# SPDX-License-Identifier: GPL-3.0-or-later
"""Tests de `detect_model` / `detect_software_version` / `resolve_feature_bin`
(switch_capture_core).

Couvre trois des six fonctions identifiées comme sans couverture persistante
en session 49 (voir CLAUDE.md, « Prochaine feature »). Recherche exhaustive
préalable (noms de fonctions dans tout `tests/`) confirmée avant d'écrire le
moindre test : aucune des trois n'apparaissait, même indirectement, malgré
leur usage par `SetupAndCaptureThread._prepare_switch` (lui-même déjà décrit
comme critique par `docs/architecture.md`) et par le mode dry run
(`inspect_switch`, qui appelle directement `detect_model`/
`detect_software_version` mais n'est testé que via ses propres réponses
`FakeConn`, jamais ces deux fonctions en isolation).

Détection 5510/5520 (issue #66) : la session 50 verrouillait une limite
connue depuis la session 08 (alias collés « 5510HI » jamais confrontés à une
sortie réelle). Des sorties `display version` réelles sont désormais en
fixtures (`tests/fixtures/display_version/`, sources dans `SOURCES.md`) : la
ligne châssis est à espaces (« HPE 5510 24G 4SFP+ HI 1-slot Switch »), et la
forme collée n'apparaît que dans les noms de fichiers d'image. Les tests
ci-dessous vérifient la détection sur ces sorties exactes, y compris quand
les images ont été renommées.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from switch_capture_core import detect_model, detect_software_version, resolve_feature_bin

# --------------------------------------------------------------------- #
# detect_model — modèles reconnus (alias vérifiés depuis la session 08)
# --------------------------------------------------------------------- #

VERSION_MSR4000 = "HPE Comware Software, Version 7.1.070, Release 8377\nHPE MSR4000 Router\n"

VERSION_5130EI = "HPE Comware Software, Version 7.1.070, Release 6555P05,\nHPE 5130-28-EI Switch\n"

VERSION_5130HI = "HPE Comware Software, Version 7.1.070, Release 6555P05\nHPE 5130-52-HI Switch\n"

VERSION_5140EI = "HPE Comware Software, Version 7.1.070, Release 6635P01\nHPE 5140-28-EI Switch\n"

VERSION_5140HI = "HPE Comware Software, Version 7.1.070, Release 6635P01\nHPE 5140-52-HI Switch\n"

VERSION_3600V2 = "HPE Comware Software, Version 5.20.99, Release 2513\nHPE A3600-24 3600 V2 EI Switch\n"

VERSION_UNKNOWN = "HPE Comware Software, Version 9.9.99, Release 9999\nHPE MystereSwitch\n"


def test_detect_model_msr4000():
    assert detect_model(VERSION_MSR4000) == "MSR4000"


def test_detect_model_5130ei():
    assert detect_model(VERSION_5130EI) == "5130EI"


def test_detect_model_5130hi():
    assert detect_model(VERSION_5130HI) == "5130HI"


def test_detect_model_5130hi_not_confused_with_5130ei():
    """Garde-fou direct : le texte « -HI » ne doit jamais matcher le profil « EI »."""
    assert detect_model(VERSION_5130HI) != "5130EI"


def test_detect_model_5140ei():
    assert detect_model(VERSION_5140EI) == "5140EI"


def test_detect_model_5140hi():
    assert detect_model(VERSION_5140HI) == "5140HI"


def test_detect_model_3600v2():
    assert detect_model(VERSION_3600V2) == "3600v2"


def test_detect_model_unknown_returns_none():
    assert detect_model(VERSION_UNKNOWN) is None


def test_detect_model_case_insensitive():
    """`detect_model` uppercase le texte ET les alias avant comparaison."""
    lowered = VERSION_5130EI.lower()
    assert detect_model(lowered) == "5130EI"


def test_detect_model_empty_string_returns_none():
    assert detect_model("") is None


# --------------------------------------------------------------------- #
# detect_model — 5510/5520 sur sorties réelles (issue #66)
# --------------------------------------------------------------------- #

FIXTURES_DISPLAY_VERSION = Path(__file__).parent / "fixtures" / "display_version"

SORTIES_REELLES = {
    "5510hi_jh145a_r3506p02.txt": "5510",
    "5510hi_jh147a_r3507p10.txt": "5510",
    "5520hi_r8m25a_r6536.txt": "5520",
}


def _lire_fixture(nom: str) -> str:
    return (FIXTURES_DISPLAY_VERSION / nom).read_text(encoding="utf-8")


def _sans_noms_d_image(sortie: str) -> str:
    """Retire les lignes citant un fichier d'image (« flash:/… »), seules à
    contenir la forme collée « 5510hi »/« 5520hi » : simule des images
    renommées et isole la ligne châssis."""
    return "".join(ligne for ligne in sortie.splitlines(keepends=True) if "flash:/" not in ligne)


def test_fixtures_display_version_toutes_utilisees():
    """Chaque fixture est couverte, et chaque fixture citée existe."""
    presentes = {f.name for f in FIXTURES_DISPLAY_VERSION.glob("*.txt")}
    assert presentes == set(SORTIES_REELLES)


@pytest.mark.parametrize(("nom", "attendu"), sorted(SORTIES_REELLES.items()))
def test_detect_model_sortie_reelle(nom, attendu):
    assert detect_model(_lire_fixture(nom)) == attendu


@pytest.mark.parametrize(("nom", "attendu"), sorted(SORTIES_REELLES.items()))
def test_detect_model_sortie_reelle_images_renommees(nom, attendu):
    """Régression #66 : avant correction, ces sorties n'étaient reconnues que
    grâce au nom des fichiers d'image ; sans eux, `detect_model` renvoyait
    None. La ligne châssis seule doit suffire."""
    sortie = _sans_noms_d_image(_lire_fixture(nom))
    assert "flash:/" not in sortie
    assert "HI " in sortie
    assert detect_model(sortie) == attendu


@pytest.mark.parametrize("nom", sorted(SORTIES_REELLES))
def test_detect_model_sortie_reelle_version_logicielle(nom):
    """La release extraite est celle de la première ligne de la sortie."""
    sortie = _lire_fixture(nom)
    attendu = sortie.splitlines()[0].rsplit("Release ", 1)[1].strip()
    assert detect_software_version(sortie) == attendu


def test_detect_model_5510_et_5520_ne_se_confondent_pas():
    assert detect_model(_lire_fixture("5520hi_r8m25a_r6536.txt")) != "5510"
    assert detect_model(_lire_fixture("5510hi_jh145a_r3506p02.txt")) != "5520"


def test_detect_model_5510_alias_colle_seul_toujours_reconnu():
    """La forme collée reste reconnue (noms d'image réels « 5510hi-cmw710-… »)."""
    assert detect_model("Boot image: flash:/5510hi-cmw710-boot-r3507p10.bin\n") == "5510"
    assert detect_model("Boot image: flash:/5520hi-cmw710-boot-r6536.bin\n") == "5520"


# --------------------------------------------------------------------- #
# detect_software_version
# --------------------------------------------------------------------- #


def test_detect_software_version_basic():
    assert detect_software_version("HPE Comware Software, Version 7.1.070, Release 6555P05\n") == "6555P05"


def test_detect_software_version_strips_trailing_comma():
    assert detect_software_version("HPE Comware Software, Version 7.1.070, Release 6555P05,\n") == "6555P05"


def test_detect_software_version_no_release_keyword_returns_none():
    assert detect_software_version("HPE Comware Software, Version 7.1.070\nHPE 5130-28-EI Switch\n") is None


def test_detect_software_version_release_keyword_without_token_returns_none():
    """`Release` présent mais rien de non-blanc juste après (fin de ligne) : pas de match, pas de crash."""
    assert detect_software_version("blabla Release \n") is None


def test_detect_software_version_empty_string_returns_none():
    assert detect_software_version("") is None


def test_detect_software_version_real_world_multiline_output():
    output = (
        "HPE Comware Software, Version 7.1.070, Release 6555P05\n"
        "Copyright (c) 2010-2026 Hewlett Packard Enterprise Development LP\n"
        "HPE 5130-28-EI Switch uptime is 12 weeks, 3 days, 4 hours, 5 minutes\n"
    )
    assert detect_software_version(output) == "6555P05"


# --------------------------------------------------------------------- #
# resolve_feature_bin
# --------------------------------------------------------------------- #


def test_resolve_feature_bin_versioned_dir_match(tmp_path):
    versioned = tmp_path / "5130EI" / "6555P05"
    versioned.mkdir(parents=True)
    bin_file = versioned / "packet-capture-5130-6555p05.bin"
    bin_file.write_bytes(b"\x00")

    result = resolve_feature_bin(str(tmp_path), "5130EI", "6555P05")

    assert result == bin_file


def test_resolve_feature_bin_falls_back_to_model_root_when_version_dir_missing(tmp_path):
    model_dir = tmp_path / "5130EI"
    model_dir.mkdir(parents=True)
    bin_file = model_dir / "packet-capture-5130-generic.bin"
    bin_file.write_bytes(b"\x00")

    result = resolve_feature_bin(str(tmp_path), "5130EI", "9999INCONNUE")

    assert result == bin_file


def test_resolve_feature_bin_falls_back_when_versioned_dir_has_no_match(tmp_path):
    """Le dossier versionné existe mais ne contient aucun `.bin` correspondant
    -> repli sur la racine du modèle, pas un `None` prématuré."""
    versioned = tmp_path / "5130EI" / "6555P05"
    versioned.mkdir(parents=True)
    (versioned / "readme.txt").write_text("pas un .bin")
    model_dir = tmp_path / "5130EI"
    fallback_bin = model_dir / "packet-capture-5130-fallback.bin"
    fallback_bin.write_bytes(b"\x00")

    result = resolve_feature_bin(str(tmp_path), "5130EI", "6555P05")

    assert result == fallback_bin


def test_resolve_feature_bin_no_version_uses_model_root_directly(tmp_path):
    model_dir = tmp_path / "5130EI"
    model_dir.mkdir(parents=True)
    bin_file = model_dir / "packet-capture-5130.bin"
    bin_file.write_bytes(b"\x00")

    result = resolve_feature_bin(str(tmp_path), "5130EI", None)

    assert result == bin_file


def test_resolve_feature_bin_model_dir_missing_returns_none(tmp_path):
    assert resolve_feature_bin(str(tmp_path), "5130EI", "6555P05") is None


def test_resolve_feature_bin_model_dir_exists_but_empty_returns_none(tmp_path):
    (tmp_path / "5130EI").mkdir(parents=True)

    assert resolve_feature_bin(str(tmp_path), "5130EI", None) is None


def test_resolve_feature_bin_ignores_files_not_matching_pattern(tmp_path):
    model_dir = tmp_path / "5130EI"
    model_dir.mkdir(parents=True)
    (model_dir / "readme.txt").write_text("pas un .bin")
    (model_dir / "other-feature-5130.bin").write_bytes(b"\x00")  # ne contient pas "packet-capture"

    assert resolve_feature_bin(str(tmp_path), "5130EI", None) is None


def test_resolve_feature_bin_multiple_matches_returns_sorted_first(tmp_path):
    model_dir = tmp_path / "5130EI"
    model_dir.mkdir(parents=True)
    (model_dir / "packet-capture-5130-v2.bin").write_bytes(b"\x00")
    (model_dir / "packet-capture-5130-v1.bin").write_bytes(b"\x00")

    result = resolve_feature_bin(str(tmp_path), "5130EI", None)

    assert result.name == "packet-capture-5130-v1.bin"
