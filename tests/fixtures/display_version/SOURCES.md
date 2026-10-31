# Sorties `display version` réelles (issue #66)

Copiées telles quelles (seuls l'invite `<HPE>display version` et les repères
« Note » des documents HPE ont été retirés). Aucune n'est inventée.

| Fichier | Modèle | Source |
|---|---|---|
| `5510hi_jh145a_r3506p02.txt` | HPE 5510 24G 4SFP+ HI 1-slot Switch JH145A, Release 3506P02 | Switch en production, forum HPE Networking Community, 06/05/2020 : <https://community.networking.hpe.com/discussion/packets-dropped-due-to-full-gbp-or-insufficient-bandwidth> |
| `5510hi_jh147a_r3507p10.txt` | HPE 5510 24G PoE+ 4SFP+ HI 1-slot Switch JH147A, Release 3507P10 | Notes de version HPE 5510HI-CMW710-R3507P18-US : <https://arubanetworking.hpe.com/techdocs/comware/RN/HPE5510HICMW710R3507P18US_RN.pdf> |
| `5520hi_r8m25a_r6536.txt` | HPE 5520 24G 4SFP+ HI Swch R8M25A, Release 6536 | Notes de version HPE 5520HI-CMW710-R6628P35 : <https://arubanetworking.hpe.com/techdocs/comware/RN/HPE5520HICMW710R6628P35RN.pdf> |

Format constaté : la ligne châssis est à espaces (`HPE 5510 24G 4SFP+ HI
1-slot Switch`, `HPE 5520 24G 4SFP+ HI Swch`), ni collée (`5510HI`) ni à
tiret (`5510-28-HI`). La forme collée n'apparaît que dans les noms de
fichiers d'image (`flash:/5510hi-cmw710-boot-….bin`).
