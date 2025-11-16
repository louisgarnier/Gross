"""Check P/E Ratio values from different sources."""
from app.services.ratio_fetcher import fetch_analysis

result = fetch_analysis('PLTR')
pe_ratio = [r for r in result.ratios if r.metric == 'P/E Ratio'][0]

print('=== P/E Ratio for PLTR ===')
print('\nValues from each source:')
for v in pe_ratio.values:
    print(f'  {v.source}: {v.value}')

print(f'\nConsensus (average): {pe_ratio.consensus}')
print(f'Spread (max - min): {pe_ratio.spread}')
valid_values = [v.value for v in pe_ratio.values if v.value is not None]
if len(valid_values) >= 2:
    print(f'\nCalculation:')
    print(f'  Consensus: ({valid_values[0]} + {valid_values[1]}) / 2 = {pe_ratio.consensus}')
    print(f'  Spread: {max(valid_values)} - {min(valid_values)} = {pe_ratio.spread}')

