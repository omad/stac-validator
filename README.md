# Spatial Temporal Asset Catalog (STAC) Validator

This utility allows users to validate catalog and/or item json files against the [STAC](https://github.com/radiantearth/stac-spec) spec.

It can be installed as command line utility and passed either a local file path or a url along with the STAC version to validate against.

## Requirements

* Python 3.x
    * Flask
    * Requests
    * Docopt
    * pytest

## Example

```bash
pip install .
stac_validator.py --help

Description: Validate a STAC item or catalog against the STAC specification.

Usage:
    stac_validator.py <stac_file> [-version]

Arguments:
    stac_file  Fully qualified path or url to a STAC file.

Options:
    -v, --version STAC_VERSION   Version to validate against. [default: master]
    -h, --help                   Show this screen.


stac_validator.py https://cbers-stac.s3.amazonaws.com/CBERS4/MUX/057/122/catalog.json -v v0.5.2
```


## TODO
* Clean up Flask app
* Recursively crawl catalog
* Get a deployment running

## Credits
Radiant Earth and Evan Rouault for ideas!