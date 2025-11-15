# Data Period Policy - TTM vs Annual

## Décision : Utiliser Annual (Last Fiscal Year) Partout

**POLITIQUE** : Tous les scrapers doivent utiliser les données **ANNUALES** (dernière année fiscale) pour garantir la cohérence entre sources.

### Raisons
1. **Cohérence** : Toutes les sources utilisent la même période
2. **Comparabilité** : Facilite la comparaison entre sources
3. **Fiabilité** : Données annuelles sont généralement auditées
4. **Standard** : Plus facile à comprendre et vérifier

### Implémentation

- **Finviz** : Utilise les données affichées sur la page (à vérifier si Annual ou TTM, mais on s'aligne sur Annual)
- **Yahoo Finance** : Utilise `financials` (annual) au lieu de `quarterly_financials` (TTM)
- **Autres sources** : À définir lors de l'implémentation

### Changements Requis

1. ✅ **Yahoo Finance Interest Coverage** : Passer de TTM (quarterly) à Annual
2. ✅ **Yahoo Finance P/E Ratio** : Vérifier si `trailingPE` est TTM ou Annual (probablement TTM, mais on peut utiliser annual si disponible)
3. ⏳ **Documenter** : Chaque scraper doit clairement indiquer qu'il utilise Annual

## État Actuel

- **Finviz** : À vérifier manuellement (mais on s'aligne sur Annual)
- **Yahoo Finance** : ⚠️ Actuellement TTM → **À CHANGER pour Annual**

