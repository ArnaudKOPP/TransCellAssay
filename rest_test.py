#!/usr/bin/env python3
# encoding: utf-8

from TransCellAssay.IO.Rest.Service import REST

s = REST("test", "https://www.ebi.ac.uk/chemblws")
res = s.get_one("targets/CHEMBL5246.json", "json")
target = res['target']
print(target['organism'])

from TransCellAssay.IO.Rest.KEGG import KEGG, KEGGParser

k = KEGG()
k.list('organism')
print(k.organismIds)
k.organism = "hsa"
print(k.pathwayIds)
print(k.get("hsa:7535"))

s = KEGGParser()
data = s.get("hsa:7535")
dict_data = s.parse(data)
print(dict_data)

data = s.get("hsa04660")
dict_data = s.parse(data)
print(dict_data['gene'])

res = s.get("hsa04660", "kgml")
print(res)

res = s.parse_kgml_pathway("hsa04660")
# print(res)
res['relations']
print(res['relations'][0])
