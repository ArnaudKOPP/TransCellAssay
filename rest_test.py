#!/usr/bin/env python3
# encoding: utf-8

# #### Psicquic REST TEST
# from TransCellAssay.IO.Rest.Psicquic import PSICQUIC

# p = PSICQUIC()
# p.print_status()
# print(p.query("string", "species:10090", firstResult=0, maxResults=100, output="tab25"))
# print(p.query("biogrid", "ZAP70"))
# print(p.query("biogrid", "ZAP70 AND species:10090"))
# res = p.query("intact", "zap70")
# for x in res:
# print(x)
# print(p.queryAll("ZAP70 AND species:9606"))

# #### Biogrid REST TEST
from TransCellAssay.IO.Rest.Biogrid import Biogrid

b = Biogrid()
print(b.get_biogrid_version())
print(b._supported_organism_list())
print(b.SupportedOrganismId)
print(b.SupportedOrganismId["9606"])
res = b.interaction(geneList="31623", searchbiogridids="true", includeInteractors="true", caca="grzefg")
print(res)

import pandas as pd
from io import StringIO

data = pd.read_table(StringIO(res), header=None)
print(data)


# #### UNIPROT REST TEST
# from TransCellAssay.IO.Rest.Uniprot import UniProt
# u = UniProt()
#
# print(u.mapping("ACC", "KEGG_ID", query='P43403 P29317'))
# res = u.search("P43403")
# print(res)
# # Returns sequence on the ZAP70_HUMAN accession Id
# sequence = u.search("ZAP70_HUMAN", columns="sequence")
# print(sequence)
#
# es = u.retrieve("P09958", frmt="xml")
# fasta = u.retrieve([u'P29317', u'Q5BKX8', u'Q8TCD6'], frmt='fasta')
# print(fasta[0])
#
# res = u.get_fasta("P09958")
# print(res)
# print(u.get_fasta_sequence("P09958"))
#
# print(u.search('zap70+AND+organism:9606', frmt='list'))
# print(u.search("zap70+and+taxonomy:9606", frmt="tab", limit=3, columns="entry name,length,id, genes"))

# #### KEGG REST TEST

# from TransCellAssay.IO.Rest.Service import REST
# s = REST("test", "https://www.ebi.ac.uk/chemblws")
# res = s.get_one("targets/CHEMBL5246.json", "json")
# target = res['target']
# print(target['organism'])

# from TransCellAssay.IO.Rest.KEGG import KEGG, KEGGParser
# k = KEGG()
# print(k.Tnumber2code("T01001"))
# print(k.code2Tnumber("hsa"))
# print(k.isOrganism("hsa"))

# print(k.info())
# print(k.info("hsa"))
# print(k.info("T01001"))  # same as above
# print(k.info("pathway"))

# k.list('organism')
# print(k.organismIds)
# k.organism = "hsa"
# print(k.pathwayIds)
# print(k.get("hsa:7535"))
# print(k.list("pathway", organism="hsa"))
# k.reaction
# k.reactionIds

# print(k.list("pathway"))  # returns the list of reference pathways
# print(k.list("pathway", "hsa"))  # returns the list of human pathways
# print(k.list("organism"))  # returns the list of KEGG organisms with taxonomic classification
# print(k.list("hsa"))  # returns the entire list of human genes
# print(k.list("T01001"))  # same as above
# print(k.list("hsa:10458+ece:Z5100"))  # returns the list of a human gene and an E.coli O157 gene
# print(k.list("cpd:C01290+gl:G00092"))  # returns the list of a compound entry and a glycan entry
# print(k.list("C01290+G00092"))  # same as above

# # search for pathways that contain Viral in the definition
# print(k.find("pathway", "Viral"))
# # for keywords "shiga" and "toxin"
# print(k.find("genes", "shiga+toxin"))
# # for keywords "shiga toxin"
# print(k.find("genes", "shiga toxin"))
# # for chemical formula "C7H10O5"
# print(k.find("compound", "C7H10O5", "formula"))
# # for chemical formula containing "O5" and "C7"
# print(k.find("compound", "O5C7", "formula"))
# # for 174.045 =< exact mass < 174.055
# print(k.find("compound", "174.05", "exact_mass"))
# # for 300 =< molecular weight =< 310
# print(k.find("compound", "300-310", "mol_weight"))

# # retrieves a compound entry and a glycan entry
# print(k.get("cpd:C01290+gl:G00092"))
# # same as above
# print(k.get("C01290+G00092"))
# # retrieves a human gene entry and an E.coli O157 gene entry
# print(k.get("hsa:10458+ece:Z5100"))
# # retrieves amino acid sequences of a human gene and an E.coli O157 gene
# print(k.get("hsa:10458+ece:Z5100/aaseq"))

# res = k.get("hsa05130/image")
# # same as : res = s.get("hsa05130","image")
# f = open("test.png", "wb")
# f.write(res)
# f.close()

# # conversion from NCBI GeneID to KEGG ID for E. coli genes
# print(k.conv("eco", "ncbi-geneid"))
# # inverse of the above example
# print(k.conv("eco", "ncbi-geneid"))
# # conversion from KEGG ID to NCBI GI
# print(k.conv("ncbi-gi", "hsa:10458+ece:Z5100"))

# # KEGG pathways linked from each of the human genes
# print(k.link("pathway", "hsa"))
# # human genes linked from each of the KEGG pathways
# print(k.link("hsa", "pathway"))
# # KEGG pathways linked from a human gene and an E. coli O157 gene.
# print(k.link("pathway", "hsa:10458+ece:Z5100"))

# # show a pathway in the browser
# k.show_pathway("path:hsa05416", scale=50)
# # Same as above but also highlights some KEGG Ids (red for all)
# k.show_pathway("path:hsa05416", dcolor="white", keggid=['1525', '1604', '2534'])
# # You can refine the colors using a dictionary:
# k.show_pathway("path:hsa05416", dcolor="white", keggid={'1525': 'yellow,red', '1604': 'blue,green', '2534': "blue"})
# print(k.check_dbentries("hsa:10458+ece:Z5100"))
# print(k.get_pathway_by_gene("7535", "hsa"))

# s = KEGGParser()
# data = s.get("hsa:7535")
# dict_data = s.parse(data)
# print(dict_data)

# data = s.get("hsa04660")
# dict_data = s.parse(data)
# print(dict_data['gene'])

# res = s.get("hsa04660", "kgml")
# print(res)

# res = s.parse_kgml_pathway("hsa04660")
# # print(res)
# res['relations']
# print(res['relations'][0])

# #### REACTOME REST TEST

# from TransCellAssay.IO.Rest.Reactome import Reactome
# r = Reactome()
# print(r.get_list_pathways())
# print(r.get_species())
# print(r.biopax_exporter(109581))

# res = r.highlight_pathway_diagram("68875", genes="CDC2", frmt='PDF')
# f = open("reactome.pdf", "w")
# f.write(res)
# f.close()

# res = r.list_by_query("Pathway", name='Apoptosis')
# identifiers = [x['dbId'] for x in res]
# print(identifiers)

# print(r.pathway_hierarchy("homo sapiens"))
# print(r.pathway_participantes(109581))
# print(r.pathway_complexes(109581))
# print(r.query_by_id("Pathway", "109581"))
# print(r.query_hit_pathways('CDC2'))
# print(r.query_hit_pathways(['CDC2']))

# print(r.species_list())
# print(r.SBML_exporter(109581))