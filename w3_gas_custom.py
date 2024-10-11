import os
import statistics
from dotenv import load_dotenv
from typing import List, Dict, Union
from web3 import Web3
load_dotenv("web3.env")

class CustomGas:
    def __init__(self, 
                 rpc_url: str = None, 
                 rpc_key: str = None,
                 chain: str = None, 
                 contract_address: str = None,
                 abi: list[dict] = None,
                 user_address: str = None):
        try:
            full_rpc_url = rpc_url.replace("choice_chain", chain) + rpc_key
            self.w3 = Web3(Web3.HTTPProvider(full_rpc_url))
            self.target_contract = self.w3.to_checksum_address(contract_address)
            self.user_address = self.w3.to_checksum_address(user_address)
            self.contract = self.w3.eth.contract(address=self.target_contract, abi=abi)
             
            if (self.w3.is_address(self.target_contract) 
                and self.w3.is_address(self.user_address) 
                and self.w3.is_connected()):
                print("CustomGas initialized successfully.")
            else:    
                raise ConnectionError("Initialization failed. Check your parameters.")    
        except Exception as e:
            print(f"Input argument error for CustomGas: {e}") 

    def estimate_gas_limit(self, *args, function_name: str = None, value: int = None) -> int:
        contract_function = getattr(self.contract.functions, function_name)
        try:
            if value is not None:
                estimated_gas = contract_function(*args).estimate_gas({"from": self.user_address, "value": value})
            else:    
                estimated_gas = contract_function(*args).estimate_gas({"from": self.user_address})
            return int(estimated_gas)
        except Exception as e:
            print(f"Function error in estimate_gas_limit: {e}")  

    def get_block_gas_fees(self, 
                           blocks: int = 50, 
                           newest: str = "latest",
                           percentiles: List[int] = [25, 50, 75], 
                           reward_percentile: int = 50, 
                           max_fee_multiplier: float = 2,
                           reward_multiplier: float = 1) -> dict:  
        block_fee_data = self.w3.eth.fee_history(block_count=blocks, newest_block=newest, reward_percentiles=percentiles)
        base_fee_avg = statistics.mean(block_fee_data["baseFeePerGas"][:-1])
        priority_fee_median = statistics.median(fee[percentiles.index(reward_percentile)] for fee in block_fee_data["reward"])

        max_fee = (base_fee_avg * max_fee_multiplier) + priority_fee_median * reward_multiplier
        return {
            'maxFeePerGas': int(max_fee),
            'priorityFeePerGasMedian': int(priority_fee_median),
            'baseFeeAvg': int(base_fee_avg),
        }  

if __name__ == "__main__":
    import json
    with open("uniswap_v2_abi.json") as file:
        uniswap_v2_abi = json.load(file)
    chain = "base"    
    user_address = os.getenv("ADDRESS") 
    rpc_url = os.getenv("INFURA_URL")  # Example: INFURA_URL=https://choice_chain-mainnet.infura.io/v3/ (replace 'choice_chain' with the desired chain, e.g., 'base')
    rpc_key = os.getenv("RPC_KEY")  # Combining the above RPC_URL and RPC_KEY allows for a customizable RPC in the class initialization.
    uniswap_v2_address = "0x4752ba5DBc23f44D87826276BF6Fd6b1C372aD24"
    
    # Creating an instance of CustomGas Class
    uniswap_v2 = CustomGas(rpc_url=rpc_url, 
                           rpc_key=rpc_key,
                           chain=chain, 
                           contract_address=uniswap_v2_address, 
                           abi=uniswap_v2_abi, 
                           user_address=user_address)

    #Calculate gas using estimate_gas_limit
    import time
    function_name = "swapExactETHForTokens"  # Example: Calculating gas for swapExactETHForTokens function, swapping 0.1 dollar worth of ETH
    weth_address = "0x4200000000000000000000000000000000000006"
    usdc_address = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
    eth_amount = int(0.0001 * (10 ** 18))
    min_tokens_out = 10000  # 0.1 usdc
    token_path = [weth_address, usdc_address]
    recipient_address = uniswap_v2.user_address
    deadline = int(time.time() + 300)
    
    estimated_gas = uniswap_v2.estimate_gas_limit(
        min_tokens_out,
        token_path,
        recipient_address,
        deadline,
        function_name=function_name,
        value=eth_amount,
    )
    print(f"Estimated gas limit for swapExactETHForTokens function: {estimated_gas} wei")
    print(uniswap_v2.get_block_gas_fees())