# SPDX-License-Identifier: GPL-3.0-or-later
"""Licence du dépôt et des paquets : GPL-3.0-or-later (SOCLE §1, issue #105)."""

import re
import subprocess
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
SPDX = "SPDX-License-Identifier: GPL-3.0-or-later"
SCRIPTS_SANS_EXTENSION = {
    "src/switch-capture",
    "packaging/debian/DEBIAN/postinst",
    "packaging/debian/DEBIAN/postrm",
}


def _lire(chemin: str) -> str:
    """Contenu texte d'un fichier du dépôt."""
    return (RACINE / chemin).read_text(encoding="utf-8")


def _fichiers_de_code() -> list[str]:
    """Fichiers de code suivis par git (.py, .sh, .c et scripts sans extension)."""
    sortie = subprocess.run(["git", "ls-files"], cwd=RACINE, capture_output=True, text=True, check=True).stdout.split()
    return [f for f in sortie if re.search(r"\.(py|sh|c)$", f) or f in SCRIPTS_SANS_EXTENSION]


def test_licence_est_le_texte_gplv3():
    """LICENSE contient le texte officiel de la GPLv3."""
    texte = _lire("LICENSE")
    assert texte.lstrip().startswith("GNU GENERAL PUBLIC LICENSE")
    assert "Version 3, 29 June 2007" in texte


def test_pyproject_declare_gpl_or_later():
    """pyproject.toml déclare GPL-3.0-or-later."""
    assert re.search(r'^license = "GPL-3\.0-or-later"$', _lire("pyproject.toml"), re.MULTILINE)


def test_spec_rpm():
    """Le spec RPM déclare la licence et installe LICENSE, que build_rpm.sh met dans le tarball."""
    spec = _lire("packaging-rpm/switch-capture.spec")
    assert re.search(r"^License:\s+GPL-3\.0-or-later$", spec, re.MULTILINE)
    assert re.search(r"^%files\n%license LICENSE$", spec, re.MULTILINE)
    assert '"$ROOT_DIR/LICENSE" "$STAGE_DIR/LICENSE"' in _lire("packaging-rpm/build_rpm.sh")


def test_copyright_debian():
    """Le .deb installe un copyright DEP-5 en GPL-3+."""
    copyright_deb = _lire("packaging/debian/copyright")
    assert copyright_deb.startswith("Format: https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/")
    assert "License: GPL-3+" in copyright_deb
    assert "/usr/share/common-licenses/GPL-3" in copyright_deb
    assert '"$BUILD_DIR/usr/share/doc/switch-capture/copyright"' in _lire("packaging/build_deb.sh")


def test_versions_alignees():
    """pyproject.toml, control Debian et spec RPM portent la même version."""
    version = re.search(r'^version = "([^"]+)"$', _lire("pyproject.toml"), re.MULTILINE).group(1)
    assert re.search(rf"^Version: {re.escape(version)}$", _lire("packaging/debian/DEBIAN/control"), re.MULTILINE)
    assert re.search(rf"^Version:\s+{re.escape(version)}$", _lire("packaging-rpm/switch-capture.spec"), re.MULTILINE)


def test_chaque_fichier_de_code_porte_l_en_tete_spdx():
    """Chaque fichier de code porte l'en-tête SPDX dans ses trois premières lignes."""
    fichiers = _fichiers_de_code()
    assert "src/switch_capture_core.py" in fichiers
    manquants = [f for f in fichiers if not any(SPDX in ligne for ligne in _lire(f).splitlines()[:3])]
    assert manquants == []
