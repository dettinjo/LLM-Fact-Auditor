import requests
from SPARQLWrapper import SPARQLWrapper, JSON

class WikipediaAPIError(Exception):
        pass

class Candidate:

    def __init__(self, entity_name, short_desc, wiki_article, link_count=0, correlation_count=0, kb_link=""):
        self.entity_name = entity_name
        self.short_desc = short_desc
        self.wiki_article = wiki_article
        self.link_count = link_count
        self.kb_link = kb_link
        self.__wiki_fisrt_para = None

        self.correlation_count = correlation_count

    def __str__(self) -> str:
        ret = ""
        ret += f"Entity Name: {self.entity_name}\n"
        ret += f"Description: {self.short_desc}\n"
        ret += f"Wiki Article: {self.wiki_article}\n"
        ret += f"Link Count: {self.link_count}\n"
        ret += f"KB Link: {self.kb_link}"
        return ret
    
    def __repr__(self) -> str:
        return self.__str__()

    def get_wiki_first_para(self):
        if self.__wiki_fisrt_para != None:
            return self.__wiki_fisrt_para

        title = self.wiki_article.split("/")[-1]
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
        response = requests.get(url)

        if response.status_code != 200:
            raise WikipediaAPIError(f"Wikipage:{self.wiki_article} Endpoint:{url} Error: {response.status_code}")

        data = response.json()
        self.__wiki_fisrt_para = data["extract"]
        return self.__wiki_fisrt_para

         

class CandidateGeneration:
    def __init__(self):
        # currently nothing to initialize
        return

    def query_wikidata(self, keyword):
        """
        Generate candidate entity from Wikidata

        Args:
            keyword (str): keyword to search
        
        Returns:
            candidates (list): Candidate objects
        """
        sparql = SPARQLWrapper(
            "https://query.wikidata.org/sparql", agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
        )

        query = (
            """
            SELECT
                ?item 
                ?itemLabel
                ?itemDescription
                (COUNT(DISTINCT ?sitelink) AS ?linkCount) 
                ?article
            WHERE {
                # find entities
                # refer to Find all entities with labels "cheese" and get their types
                # https://www.wikidata.org/wiki/Wikidata:SPARQL_query_service/queries/examples  
                SERVICE wikibase:mwapi {
                    bd:serviceParam wikibase:api "EntitySearch".
                    bd:serviceParam wikibase:endpoint "www.wikidata.org".
                    bd:serviceParam mwapi:search "%s".
                    bd:serviceParam mwapi:language "en".
                    ?item wikibase:apiOutputItem mwapi:item.
                }

                ?item rdfs:label ?itemLabel; schema:description ?itemDescription. 
                ?sitelink schema:about ?item.

                # at least have en wiki
                # retrieve en wiki link
                # refer to "Items with a Wikispecies sitelink"
                # https://www.wikidata.org/wiki/Wikidata:SPARQL_query_service/queries/examples
                ?article schema:about ?item; schema:isPartOf <https://en.wikipedia.org/>. 

                # language filter
                # refer to "Names of African countries in all their official languages and English
                # https://www.wikidata.org/wiki/Wikidata:SPARQL_query_service/queries/examples
                FILTER(LANG(?itemLabel) = "en").
                FILTER(LANG(?itemDescription) = "en").

                # avoid pathological behavior for acronym/names
                FILTER NOT EXISTS {?item wdt:P31/wdt:P279* wd:Q4167410}. # avoid DOD -> DOD(disambiguation)
                FILTER NOT EXISTS {?item wdt:P31/wdt:P279* wd:Q101352}. # avoid DOD -> Dodd(last name)
                FILTER NOT EXISTS {?item wdt:P31/wdt:P279* wd:Q202444}. # similar reason, no first name page
            }
            GROUP BY ?item ?itemLabel ?itemDescription ?article
            ORDER BY DESC(?linkCount)
            LIMIT 10
            """
            % keyword
        )

        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)

        resp = sparql.query().convert()


        result = resp["results"]["bindings"]
        ret = []
        for r in result:
            ret.append(
                Candidate(
                    r["itemLabel"]["value"],
                    r["itemDescription"]["value"],
                    r["article"]["value"],
                    link_count = int(r["linkCount"]["value"]),
                    kb_link = r["item"]["value"]
                ),
            )

        return ret
    

    def query_correlation_wikidata(self, keyword, confirmed_entities):
        """
        Generates candidate entities from Wikidata based on a keyword and leverages linkage between entities.
        In the program this function is used when BERT can't decide the perfect entity link.

        Args:
        keyword (str): The keyword to search.
        confirmed_entities (list[Candidate]): The list of confirmed entities.

        Returns:
        list[Candidate]: A list of Candidate objects.
        """
        sparql = SPARQLWrapper(
            "https://query.wikidata.org/sparql", agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
        )

        entity_ids = [x.kb_link.split("/")[-1] for x in confirmed_entities]
        entity_ids = ["wd:"+x for x in entity_ids if x]
        correlation_contraints = "\n".join([f"OPTIONAL {{?item ?correlationlink {x}.}}\nOPTIONAL {{{x} ?correlationlink ?item.}}" for x in entity_ids])

        query = (
            """
            SELECT ?item ?itemLabel ?itemDescription
                (COUNT(DISTINCT ?sitelink) AS ?linkCount) 
                (COUNT(DISTINCT ?correlationlink) AS ?correlationCount) 
                ?article
            WHERE {
                # find entities
                # refer to Find all entities with labels "cheese" and get their types
                # https://www.wikidata.org/wiki/Wikidata:SPARQL_query_service/queries/examples  
                SERVICE wikibase:mwapi {
                    bd:serviceParam wikibase:api "EntitySearch".
                    bd:serviceParam wikibase:endpoint "www.wikidata.org".
                    bd:serviceParam mwapi:search "%s".
                    bd:serviceParam mwapi:language "en".
                    ?item wikibase:apiOutputItem mwapi:item.
                }
                
                ?item rdfs:label ?itemLabel; schema:description ?itemDescription. 
                ?sitelink schema:about ?item.
                
                # optional correlation constraints
                %s

                # at least have en wiki
                # retrieve en wiki link
                # refer to "Items with a Wikispecies sitelink"
                # https://www.wikidata.org/wiki/Wikidata:SPARQL_query_service/queries/examples
                ?article schema:about ?item; schema:isPartOf <https://en.wikipedia.org/>. 
                
                # language filter
                # refer to "Names of African countries in all their official languages and English
                # https://www.wikidata.org/wiki/Wikidata:SPARQL_query_service/queries/examples
                FILTER(LANG(?itemLabel) = "en").
                FILTER(LANG(?itemDescription) = "en").
            
                # avoid pathological behavior for acronym/names
                FILTER NOT EXISTS {?item wdt:P31/wdt:P279* wd:Q4167410}. # avoid DOD -> DOD(disambiguation)
                FILTER NOT EXISTS {?item wdt:P31/wdt:P279* wd:Q101352}. # avoid DOD -> Dodd(last name)
                FILTER NOT EXISTS {?item wdt:P31/wdt:P279* wd:Q202444}. # similar reason, no first name page
            }
            GROUP BY ?item ?itemLabel ?itemDescription ?article 
            ORDER BY DESC(?correlationCount) DESC(?linkCount)
            LIMIT 10
            """
            % (keyword, correlation_contraints)
        )

        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)

        resp = sparql.query().convert()


        result = resp["results"]["bindings"]
        ret = []
        for r in result:
            ret.append(
                Candidate(
                    r["itemLabel"]["value"],
                    r["itemDescription"]["value"],
                    r["article"]["value"],
                    link_count = int(r["linkCount"]["value"]),
                    correlation_count = int(r["correlationCount"]["value"]),
                    kb_link = r["item"]["value"]
                ),
            )

        return ret
    
    

if __name__ == "__main__":
    cg = CandidateGeneration()
    ret = cg.query_wikidata("Cayde-6")
    candidate = ret[0]
    print(candidate.get_wiki_first_para())

    ret = cg.query_correlation_wikidata("Destiny", [candidate])
    print(ret[0].correlation_count)
    # print(ret)