# CustomGas プロジェクト

このプロジェクトは、Ethereum 互換のブロックチェーン（例：Base）上でのガス料金の見積もりと、ブロックチェーンのガス料金情報を取得するためのシンプルなツールです。

## プロジェクトの構成

1. `w3_gas_custom.py`: `CustomGas`クラスを含むメインの Python ファイル
2. `test.py`: `CustomGas`クラスの使用例を示すテストスクリプト

## 基本的な使い方

1. スクリプトは以下の情報を表示します：
   - Uniswap V2 の`swapExactETHForTokens`関数のガス料金見積もり
   - 現在のブロックチェーンのガス料金情報

## CustomGas クラスの主な機能

1. `estimate_gas_limit()`: 特定の関数呼び出しに必要なガス量を見積もります。

2. `get_block_gas_fees()`: 現在のブロックチェーンのガス料金情報を取得します。

## カスタマイズのヒント

# CustomGas プロジェクト - get_block_gas_fees() メソッド

`CustomGas`クラスの`get_block_gas_fees()`メソッドは、現在のブロックチェーンのガス料金情報を取得し、カスタマイズするためのツールです。

## メソッドの定義

```python
def get_block_gas_fees(self,
                       blocks: int = 50,
                       newest: str = "latest",
                       percentiles: List[int] = [25, 50, 75],
                       reward_percentile: int = 50,
                       max_fee_multiplier: float = 2,
                       reward_multiplier: float = 1) -> dict:
```

## パラメータの説明

- `blocks`: 分析する直近のブロック数（デフォルト: 50）
- `newest`: 分析を開始する最新のブロック（デフォルト: "latest"）
- `percentiles`: 報酬のパーセンタイルを計算するための値のリスト（デフォルト: [25, 50, 75]）
- `reward_percentile`: 優先報酬の中央値を計算するためのパーセンタイル（デフォルト: 50）
- `max_fee_multiplier`: 最大手数料を計算する際のベース手数料の乗数（デフォルト: 2）
- `reward_multiplier`: 最大手数料を計算する際の優先報酬の乗数（デフォルト: 1）

## 戻り値

このメソッドは以下の情報を含む辞書を返します：

- `maxFeePerGas`: 推奨される最大ガス料金
- `priorityFeePerGasMedian`: 優先手数料の中央値
- `baseFeeAvg`: ベース手数料の平均値

## カスタマイズの例

1. より長期間のデータを分析する：

   ```python
   gas_fees = custom_gas.get_block_gas_fees(blocks=200)
   ```

2. 異なるパーセンタイルを使用する：

   ```python
   gas_fees = custom_gas.get_block_gas_fees(percentiles=[10, 50, 90])
   ```

3. より積極的な料金設定：
   ```python
   gas_fees = custom_gas.get_block_gas_fees(max_fee_multiplier=2.5, reward_multiplier=1.2)
   ```

このメソッドを使用することで、現在のネットワーク状況に基づいて最適なガス料金を推定し、トランザクションの成功確率を高めることができます。

ツールを使って、Ethereum 互換のブロックチェーン上でのガス料金の動向を簡単に確認できます。今回はアウトプットのため練習で作成しました。
いろいろ追加機能付け加えて強化してください！
