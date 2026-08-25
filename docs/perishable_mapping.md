# Perishable Classification - docs/perishable_mapping.md

## Methodology
Perishability is derived primarily from DEPARTMENT. Since GROCERY mixes
perishable and shelf-stable items, its 94 COMMODITY_DESC values were
individually reviewed and reclassified where needed.

## Perishable departments (whole department)
PRODUCE, MEAT, MEAT-PCKGD, MEAT-WHSE, PORK, DELI, DELI/SNACK BAR,
DAIRY DELI, PASTRY, GRO BAKERY, SEAFOOD, SEAFOOD-PCKGD, SALAD BAR,
FLORAL, FROZEN GROCERY

## Perishable commodities within GROCERY 
CHEESE, YOGURT, FLUID MILK PRODUCTS, MILK BY-PRODUCTS,
REFRGRATD DOUGH PRODUCTS, REFRGRATD JUICES/DRNKS, BAKED BREAD/BUNS/ROLLS,
BAKED SWEET GOODS, EGGS, BUTTER, MARGARINES, FRZN MEAT/MEAT DINNERS,
FROZEN PIZZA, FRZN VEGETABLE/VEG DSH, FRZN NOVELTIES/WTR ICE,
FRZN BREAKFAST FOODS, FROZEN PIE/DESSERTS, FRZN POTATOES, 
FROZEN BREAD/DOUGH, FRZN JCE CONC/DRNKS, FRZN FRUITS, FRZN ICE, 
FROZEN CHICKEN, FRZN SEAFOOD

## Non-perishable departments
DRUG GM, COSMETICS, NUTRITION, SPIRITS, GARDEN CENTER, TOYS, AUTOMOTIVE,
HOUSEWARES, PHOTO, VIDEO, VIDEO RENTAL, ELECT &PLUMBING, HBC, RX,
PHARMACY SUPPLY, plus all non-reclassified GROCERY commodities

## Excluded (not real products / noise)
MISC. TRANS., MISC SALES TRAN, COUP/STR & MFG, TRAVEL & LEISUR,
KIOSK-GAS, CHEF SHOPPE, CNTRL/STORE SUP, GM MERCH EXP, POSTAL CENTER,
CHARITABLE CONT, PROD-WHS SALES, RESTAURANT, blank department,
plus pet/household/cleaning items and alcohol within GROCERY

## Judgment calls 
- FROZEN treated as perishable given retail waste-tracking conventions,
  though shelf life is much longer than fresh
- FLORAL included as perishable but is not food waste in the usual sense
- Alcohol (wine/beer/liquor) excluded from perishable despite sitting in
  GROCERY, since spoilage risk is minimal