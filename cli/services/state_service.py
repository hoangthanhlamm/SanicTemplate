from web3 import Web3
from web3.middleware import geth_poa_middleware

from app.utils.logger_utils import get_logger
from cli.services.artifacts.bep20_abi import BEP20_ABI

logger = get_logger('State Service')


class StateService:
    def __init__(self, provider_uri):
        self._w3 = Web3(Web3.HTTPProvider(provider_uri))
        self._w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    def get_latest_block(self):
        return self._w3.eth.block_number

    def to_checksum(self, address):
        return self._w3.toChecksumAddress(address.lower())

    def balance_of(self, address, token, block_number='latest'):
        token_contract = self._w3.eth.contract(self._w3.toChecksumAddress(token), abi=BEP20_ABI)
        decimals = token_contract.functions.decimals().call()
        balance = token_contract.functions.balanceOf(self._w3.toChecksumAddress(address)).call(block_identifier=block_number)
        return balance / 10 ** decimals

    def total_supply(self, token_address, block_number='latest'):
        token_contract = self._w3.eth.contract(self._w3.toChecksumAddress(token_address), abi=BEP20_ABI)
        decimals = token_contract.functions.decimals().call()
        total_supply = token_contract.functions.totalSupply().call(block_identifier=block_number) / 10 ** decimals
        return total_supply
