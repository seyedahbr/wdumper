import os, sys, json, requests, copy
from argparse import ArgumentParser
from SPARQLWrapper import SPARQLWrapper, JSON
from typing import Optional, Union, List

def genargs(prog: Optional[str] = None) -> ArgumentParser:
    parser = ArgumentParser(prog)
    parser.add_argument("input", help="Input WDumper specification file")
    parser.add_argument("output", help="Output WDumper specification file, enriched with the subclasses")
    parser.add_argument("-dp" , "--desiredproperty", help="Property that we want to include the subclasses of its values", default='P31')
    return parser

def getResults(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    sparql = SPARQLWrapper(endpoint_url,user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

def removeCurrentProperty(prop_array:List, propert: object) -> List:
    for i in range(len(prop_array)):
        if prop_array[i]['property'] == propert['property'] and prop_array[i]['value'] == propert['value']:
            prop_array.pop(i)
            break
    return prop_array

def main(argv: Optional[Union[str, List[str]]] = None, prog: Optional[str] = None) -> int:
    if isinstance(argv, str):
        argv = argv.split()
    opts = genargs(prog).parse_args(argv if argv is not None else sys.argv[1:])
    if not os.path.exists(opts.input):
        print("ERROR - The input file does not exist.")
        return 1
    (outDir, outFilename) = os.path.split(opts.output)
    if not os.path.exists(outDir):
        print("ERROR - The output file does not exist.")
        return 1
    
    wikidataEndpoint = 'https://query.wikidata.org/sparql'
    queryTemplate = """
        PREFIX wd: <http://www.wikidata.org/entity/>
        PREFIX wdt: <http://www.wikidata.org/prop/direct/>
        SELECT ?subtypeQIDs WHERE {{
        ?subtypeQIDs wdt:P279+ {0} .
    }}
    """
    with open(opts.input) as datafile:
        data = json.load(datafile)
    outData=copy.deepcopy(data)
    print('getting subclasses from Wikidata...')
    for entity in data['entities']:
        if entity['type']=='item':
            #print('Entity is: ' + str(entity))
            for propert in entity['properties']:
                if propert['property']==opts.desiredproperty and propert['type']=='entityid':
                    basePad = removeCurrentProperty(entity['properties'], propert)
                    #print('basePad: ' + str(basePad))
                    #print('Property ' + opts.desiredproperty + ' was found with the value: ' + str(propert['value']))
                    query=queryTemplate.format('wd:'+propert['value'])
                    print('Getting subclasses from Wikidata endpoint...')
                    results = getResults(wikidataEndpoint, query)
                    print(len(results['results']['bindings']) , 'subclasses was fetched from Wikdiata')
                    for qid in results['results']['bindings']:
                        value=qid['subtypeQIDs']['value'].replace('http://www.wikidata.org/entity/','')
                        print('Adding subclass: ' + value + ' with all the same-level conditions')
                        tempPad={'type':'item','properties':[]}
                        tempPad['properties']+=basePad
                        tempPad['properties'].append({'type': 'entityid','rank': 'all','value': value,'property': opts.desiredproperty})
                        #print('tempPad: ' + str(tempPad))
                        outData['entities'].append(tempPad)
                        #print('outData: ' + str(outData['entities']))
    print('Writing to the new config file...')
    with open(opts.output, 'w') as outfile:
        json.dump(outData, outfile, indent=3)
    print('done.')
    return 0

if __name__ == '__main__':
    main(sys.argv[1:])