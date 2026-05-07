# Mazda CdMOBP Optimization Project

このプロジェクトは，マツダの多目的ベンチマーク問題（CdMOBP）を対象とした複数車種（SUV，LV，SV）の同時最適化システムです．NSGA-IIアルゴリズムを用いて，車体重量の最小化と部品共通化率の最大化を同時に探索します．

## プロジェクト構成

- `main.py`: 最適化の実行エントリーポイント．アルゴリズムの設定を行います．
- `problem.py`: 最適化問題の定義．設計変数，制約条件，目的関数の構造を管理します．
- `evaluator.py`: シミュレータ（EXE）との連携モジュール．
- `Info_Mazda_CdMOBP.xlsx`: 問題設定の詳細が記載された定義ファイル．

## セットアップ

Python 3.8以上が必要です．
必要なライブラリをインストールしてください．

```bash
pip install platypus-opt openpyxl numpy
```

また，```mazda_mop.exe```が適切なパスに配置されていることを確認してください．

## 使用方法
基本的な実行は，ターミナルから以下のコマンドで行います．
```bash
python main.py
```

### アルゴリズム (NSGA-II)
本プロジェクトの多目的最適化アルゴリズムとして，以下の論文で提案された **NSGA-II (Nondominated Sorting Genetic Algorithm II)** を使用しています．このアルゴリズムは，多目的最適化におけるパレート解の探索において非常に高い実績があります．

- **論文**: K. Deb, A. Pratap, S. Agarwal and T. Meyarivan, "A fast and elitist multiobjective genetic algorithm: NSGA-II," in *IEEE Transactions on Evolutionary Computation*, vol. 6, no. 2, pp. 182-197, April 2002, doi: 10.1109/4235.996017.
- **実装ライブラリ**: [Platypus (A Free and Open Source Library for Multiobjective Optimization)](https://github.com/Project-Platypus/Platypus)

### 問題設定の詳細 (Technical Specifications)
本システムで扱う最適化問題の規模は以下の通りです．

- **設計変数**: 222個（SUV, LV, SV 各車種74個の板厚変数）
- **目的関数**: 2個（総重量の最小化、および部品共通化率の最大化）
- **制約条件**: 54個（各車種の衝突安全性能、剛性、および共通化に関する制約）
- **探索空間**: 各変数は離散的な板厚候補値（Discrete Volume）から選択される実数値として定義されています．

### パラメータの設定
計算条件やパスの設定を変更する場合，各スクリプト内のパラメータ変数を直接編集して調整してください．

### 出力結果
実行か完了すると，```results```フォルダに```pareto.csv```と10世代毎にパレート解を描画した```pareto.png```が記録されています．

## 引用・参照 (Citations & References)

本プロジェクトで使用しているシミュレータ（実行ファイル）および問題設定は，宇宙航空研究開発機構（JAXA）によって公開されている「自動車車体構造の多目的設計最適化ベンチマーク問題（CdMOBP）」に基づいています．

- **ベンチマーク問題詳細**: [自動車車体構造の多目的設計最適化ベンチマーク問題 (JAXA)](https://ladse.eng.isas.jaxa.jp/benchmark/jpn/index.html)
- **実行ファイル**: 上記公式サイトより提供されている `mazda_mop.exe` を使用しています．

本プログラムの実行には，上記サイトよりダウンロードしたバイナリファイルを `./bin/` ディレクトリ配下に配置する必要があります．

---
> **Note**: 本リポジトリには，JAXAより配布されている実行ファイル本体および著作権が含まれるデータは含まれておりません．利用規約については上記公式サイトを直接ご確認ください．
