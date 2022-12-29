#!/usr/bin/env python
from multisigwallet_predeployed import  MultiSigWalletGenerator
import json


def main():
    print(json.dumps(MultiSigWalletGenerator().get_abi(), sort_keys=True, indent=4))


if __name__ == '__main__':
    main()
