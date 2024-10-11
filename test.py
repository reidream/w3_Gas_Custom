import os
from dotenv import load_dotenv
from w3_gas_custom import CustomGas

load_dotenv()

def main():
    rpc_url = os.getenv("INFURA_URL")
    rpc_key = os.getenv("RPC_KEY")
    chain = "base"
    contract_address = "0x4752ba5DBc23f44D87826276BF6Fd6b1C372aD24"  # Uniswap V2 
    user_address = os.getenv("ADDRESS")
    import json
    with open("uniswap_v2_abi.json") as file:
        uniswap_v2_abi = json.load(file)

    # Create CustomGas instance
    custom_gas = CustomGas(
        rpc_url=rpc_url,
        rpc_key=rpc_key,
        chain=chain,
        contract_address=contract_address,
        abi=uniswap_v2_abi,
        user_address=user_address
    )

    # Test estimate_gas_limit
    weth_address = "0x4200000000000000000000000000000000000006"
    usdc_address = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
    eth_amount = int(0.0001 * (10 ** 18)) # (10 ** 18)
    min_tokens_out = 10000  # 0.1 usdc (10 ** 6)
    token_path = [weth_address, usdc_address]
    recipient_address = user_address
    import time
    deadline = int(time.time() + 300)

    estimated_gas = custom_gas.estimate_gas_limit(
        min_tokens_out,
        token_path,
        recipient_address,
        deadline,
        function_name="swapExactETHForTokens",
        value=eth_amount
    )
    print(f"Estimated gas limit: {estimated_gas} wei")

    # Test get_block_gas_fees
    gas_fees = custom_gas.get_block_gas_fees() 
    print("Block gas fees:")
    for key, value in gas_fees.items():
        print(f"  {key}: {value} wei")

if __name__ == "__main__":
    main()

    