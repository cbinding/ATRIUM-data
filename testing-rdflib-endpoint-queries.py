import os
from pathlib import Path
from rdflib import Graph
from SPARQLWrapper import SPARQLWrapper, RDFXML


# set up file names as constants
DATA_PATH = (Path(__file__).parent / "data").resolve()
SSH_LCSH = os.path.join(DATA_PATH, "SSH-LCSH.nt")
AAT_PREFLABELS = os.path.join(DATA_PATH, "AAT-PREFLABELS.nt")
LCSH_CLOSEMATCH_AAT = os.path.join(DATA_PATH, "LCSH-CLOSEMATCH-AAT.nt")
SSH_LCSH_CLOSEMATCH_AAT = os.path.join(DATA_PATH, "SSH-LCSH-CLOSEMATCH-AAT.nt")
SSH_LCSH_BROADMATCH_AAT = os.path.join(DATA_PATH, "SSH-LCSH-BROADMATCH-AAT.nt")
SSH_LCSH_BROADBROADMATCH_AAT = os.path.join(DATA_PATH, "SSH-LCSH-BROADBROADMATCH-AAT.nt")
SSH_LCSH_MATCHED_AAT = os.path.join(DATA_PATH, "SSH-LCSH-MATCHED-AAT.csv")
SSH_LCSH_NOMATCH_AAT = os.path.join(DATA_PATH, "SSH-LCSH-NOMATCH-AAT.csv")


# function to run SPARQL query against specified endpoint
# returnFormat supports "xml", "n3", "turtle", "nt", "pretty-xml", "trix", "trig", "nquads", "json-ld" and "hext"
def querySparqlEndpoint(endpointURI: str="", sparqlQuery: str="", returnFormat: str="nt"):
  sparql = SPARQLWrapper(endpointURI)
  sparql.setQuery(sparqlQuery)
  sparql.setMethod("POST")
  sparql.setReturnFormat(RDFXML)
  results = sparql.queryAndConvert()
  return results.serialize(format=returnFormat)  
  

# Wikidata SPARQL query to generate LCSH-closeMatch-AAT mappings (NTriples output)
query = """
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX gvp: <http://vocab.getty.edu/ontology#>
CONSTRUCT { ?lcsh_uri skos:closeMatch ?aat_uri }
WHERE { 
  ?wd_uri wdt:P244 ?lcsh_id; wdtn:P1014 ?aat_uri .
  BIND(IRI(CONCAT('http://id.loc.gov/authorities/subjects/', ?lcsh_id)) AS ?lcsh_uri) .
}
#LIMIT 5
"""
results = querySparqlEndpoint(endpointURI="https://query.wikidata.org/sparql", sparqlQuery=query)
with open(LCSH_CLOSEMATCH_AAT, "w") as file:
  file.write(results)


# Getty AAT SPARQL query to get prefLabels (English) for each Concept
query = """
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX gvp: <http://vocab.getty.edu/ontology#>
CONSTRUCT { 
  ?uri skos:prefLabel ?lbl . 
  ?uri a gvp:Concept .
}
#SELECT ?uri (STR(?lbl) AS ?label) 
WHERE {
 ?uri a gvp:Concept; skos:inScheme aat:; 
	gvp:prefLabelGVP [gvp:term ?lbl] .
 FILTER(langMatches(lang(?lbl), "en"))
}
#LIMIT 5
"""
results = querySparqlEndpoint(endpointURI="https://vocab.getty.edu/sparql", sparqlQuery=query)
#with open(AAT_PREFLABELS, "w", encoding="utf-8-sig") as file:
with open(AAT_PREFLABELS, "w") as file:
  file.write(results)


# Create a Graph containing the combined RDF files
g = Graph()
g.parse(SSH_LCSH, format="nt")
g.parse(AAT_PREFLABELS, format="nt")
g.parse(LCSH_CLOSEMATCH_AAT, format="nt")

q = """
  PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
  PREFIX gvp: <http://vocab.getty.edu/ontology#>
  CONSTRUCT { ?uri skos:closeMatch ?aat }
  WHERE {
  ?uri a skos:Concept; skos:exactMatch ?lcsh .
  ?lcsh skos:closeMatch ?aat .
  ?aat a gvp:Concept .
}
"""
results = g.query(q)
results.serialize(destination=SSH_LCSH_CLOSEMATCH_AAT, format="nt")
# add the mappings to the graph


# print(g.serialize(format='turtle'))
