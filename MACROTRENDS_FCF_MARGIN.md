# Macrotrends FCF Margin Scraper - Documentation

## Problème Identifié

Macrotrends **n'affiche pas directement** "Free Cash Flow Margin" sur une page dédiée.

**URL testée (404)**: `https://www.macrotrends.net/stocks/charts/PLTR/palantir-technologies/free-cash-flow-margin`

## Solution Implémentée

### Calcul de FCF Margin

FCF Margin est **calculé** à partir de deux valeurs disponibles sur Macrotrends :

**Formule**: `FCF Margin = (Free Cash Flow / Revenue) × 100`

### Sources des Données

1. **Free Cash Flow** : Récupéré depuis la page `cash-flow-statement`
   - URL: `https://www.macrotrends.net/stocks/charts/PLTR/palantir-technologies/cash-flow-statement`
   - Cherche la ligne "Free Cash Flow" dans le tableau
   - Si non trouvé, calcule: `Operating Cash Flow - Capital Expenditures`

2. **Revenue** : Récupéré depuis la page `financial-statements`
   - URL: `https://www.macrotrends.net/stocks/charts/PLTR/palantir-technologies/financial-statements`
   - Cherche la ligne "Revenue" ou "Total Revenue" dans le tableau

### Pourquoi Cette Approche

- Macrotrends n'affiche pas FCF Margin directement
- Les composants (Free Cash Flow et Revenue) sont disponibles
- Le calcul est standard: FCF Margin = FCF / Revenue × 100
- Cette valeur sera **comparée avec QuickFS et Koyfin** pour vérification

### État Actuel

- ✅ **Code implémenté** : `get_fcf_margin()` dans `macrotrends.py`
- ⚠️ **Test retourne None** : Rate limiting (429) - Macrotrends bloque les requêtes trop fréquentes
- ✅ **Intégré dans API** : Valeur sera disponible pour comparaison avec autres sources
- ✅ **Frontend** : Colonne "Macrotrends" s'affiche, valeur None affichée comme "—"
- ⏳ **Vérification** : À faire quand QuickFS et Koyfin seront implémentés

### Test Résultats

- **PLTR** : Gross Margin = 80.81% ✅, FCF Margin = None (rate limiting)
- **NVDA** : Gross Margin = 69.85% ✅, FCF Margin = None (rate limiting)

**Note** : Le rate limiting (429) est normal avec Macrotrends. Le cache (1 heure) aide à réduire les requêtes. Les valeurs None seront comparées avec QuickFS et Koyfin une fois ces scrapers implémentés.

### Prochaines Étapes

1. Implémenter QuickFS FCF Margin (4.8)
2. Implémenter Koyfin FCF Margin (4.9)
3. Comparer les 3 valeurs (Macrotrends, QuickFS, Koyfin)
4. Si Macrotrends diffère significativement, investiguer la cause

### Note Importante

Cette valeur est **calculée**, pas directement scrapée. Elle doit être vérifiée par comparaison avec les autres sources selon la stratégie du projet.

