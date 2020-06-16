# Lambda and Step Functions

A set of AWS Lambda Functions and Step Functions for the automated pipelines for histo.fyi

## Aims

To develop a set of component [AWS Lambda functions](https://aws.amazon.com/lambda/) which will download, split, superimpose, truncate and transform sets of molecules of the same family. This will focus initially on MHC Class I and II molecules of the immune system, but the aim is to develop the functions in as neutral a way possible so as to permit reuse for other families of molecules.

The aim is to use [12 Factor App](https://12factor.net/) principles as much as possible, using configuration stored either in persistent storage with locations injected as environment variables or in environment variables themselves. This will hopefully allow for some reuse with as little work as possible.

The modules will be as small as possible, performing at most one or two tasks, to allow for swapping if underlying systems or libraries change. [AWS Lambda Layers](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html) will be used to allow for management of significant packages.

## Overview


## Functions

### RCSBSearch

This function does two things:

- it runs a pre-defined query on the [RCSB RESTful API](https://data.rcsb.org/redoc/index.html). The default query to run is called `query` but this can be overridden by a named query in the `event` payload of the Lambda function in the variable `selected_query`. Queries sit in the `metadata/queries/rcsb` folder in the bucket you specify in the environment variable `bucket`. Queries are stored as JSON.
- it compares the results with those structures already downloaded or added to the ignore list.
- it writes out a file listing the items to be downloaded if there are new structures not on the downloaded or ignore list.

### PDBDownload

This function does one thing:

- it downloads the PDB file corresponding to the PDB code it is provided in the `event` payload of the Lambda function in the variable `pdb_code` and stores it in a folder, named with the lowercase version of the pdb_code, in the `structures/raw` folder of the bucket you specify in the environment variable `bucket`.

e.g. structures/raw/2hla/raw.pdb

### PDBInformationExtractor

This function does one thing:

- it extracts information about the PDB file in question and stores it the same folder as the raw pdb file.

e.g. structures/raw/2hla/info.json

Full description coming soon

### PDBSplitter

This function does one thing:

- it extracts unique complexes from the PDB file which can have one or many complexes. It stores each complex in the same folder as the raw pdb file.

e.g. structures/raw/2hla/complex_1.pdb

Full description coming soon

### StructureAligner

This function does one thing:

- it aligns the single complex pdb file for one molecule against the alpha1/alpha2 domains of the 2hla structure. It then writes out that aligned file into a folder, named with the lower case version of the pdb_code, the `structures/aligned` folder of the bucket.

e.g. structures/aligned/3hla/complex_1.pdb

Full description coming soon

### StructureTruncator

Full description coming soon

### PeptideExtractor

Full description coming soon

### StructureExploder

Full description coming soon

### AverageStructureCreator

Full description coming soon

### RMSDAnalyser

Full description coming soon
