'''Module for generaration of MultiSigWallet predeployed smart contract'''

from os.path import dirname, join
from typing import Dict

from predeployed_generator.contract_generator import ContractGenerator

class MultiSigWalletGenerator(ContractGenerator):
    '''Generates MultiSigWallet
    '''

    ARTIFACT_FILENAME = 'MultiSigWallet.json'
    MAX_OWNER_COUNT = 50
    ZERO_ADDRESS = '0x'+'0'*40

     # ---------- storage ----------
    # -------MultiSigWallet-------
    # 0: transactions
    # 1: confirmations
    # 2: isOwner
    # 3: owners
    # 4: required
    # 5: transactionCount

    TRANSACTIONS_SLOT = 0
    CONFIRMATIONS_SLOT = ContractGenerator.next_slot(TRANSACTIONS_SLOT)
    IS_OWNER_SLOT = ContractGenerator.next_slot(CONFIRMATIONS_SLOT)
    OWNERS_SLOT = ContractGenerator.next_slot(IS_OWNER_SLOT)
    REQUIRED_SLOT = ContractGenerator.next_slot(OWNERS_SLOT)
    TRANSACTIONS_COUNT_SLOT = ContractGenerator.next_slot(REQUIRED_SLOT)

    def __init__(self):
        generator = MultiSigWalletGenerator.from_hardhat_artifact(join(
            dirname(__file__),
            'artifacts',
            self.ARTIFACT_FILENAME))
        super().__init__(bytecode=generator.bytecode)

    @classmethod
    def generate_storage(cls, **kwargs) -> Dict[str, str]:
        erector_addresses = kwargs['erector_addresses']
        try:
            required_confirmations = kwargs['required_confirmations']
        except KeyError:
            required_confirmations = 1

        if len(erector_addresses) > cls.MAX_OWNER_COUNT:
            raise Exception('Number of erectors must not be more than 50')
        if required_confirmations > len(erector_addresses):
            raise Exception('Number of required confirmations must be less'
                            'or equal than number of erectors')

        storage: Dict[str, str] = {}
        for erector_address in erector_addresses:
            if erector_address == cls.ZERO_ADDRESS:
                raise Exception('Erector address must not be zero')
            is_owner_value_slot = cls.calculate_mapping_value_slot(
                cls.IS_OWNER_SLOT,
                erector_address,
                'address')
            cls._write_uint256(storage, is_owner_value_slot, 1)
        cls._write_addresses_array(storage, cls.OWNERS_SLOT, erector_addresses)
        cls._write_uint256(storage, cls.REQUIRED_SLOT, required_confirmations)
        return storage
