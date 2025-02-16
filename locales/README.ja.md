# GrowledgePilot: AIパワード個人学習アシスタント

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/release/python-390/)

---

## 🚀 はじめに

GrowledgePilotは、複数の分野での効率的で楽しい学習をサポートするAIパワードの個人学習アシスタントです。プログラミングとAIの力を組み合わせて、インテリジェントな学習ワークフロー、パーソナライズされたコンテンツ、インタラクティブな体験を提供し、学習課題を克服して継続的な知識の成長を実現します。

## ✨ 主な機能

- 🎯 **パーソナライズされた学習プラン**: AIが興味、目標、現在の習熟度に基づいて学習パスを動的に調整します。
- 🤖 **インタラクティブなAIチュータリング**: テキストまたは音声を通じてAIとカスタマイズされた学習ガイダンスを行います。
- 🔍 **リアルタイム知識更新**: 統合APIを通じて最新ニュース、株価、データインサイトを取得します。
- 📊 **進捗管理**: SQLiteを使用して学習の進捗を保存および可視化します。

## 📚 仕組み

GrowledgePilotは以下の主要な戦略を用いて学習体験を向上させます：

1. **アクティブリコール**: AIアシスタントが定期的に学習内容について質問し、記憶から情報を積極的に取り出すことを促します。これにより神経経路が強化され、長期記憶が改善されます。
2. **間隔反復**: (将来の機能) システムは特定の概念との最後のインタラクション時期を追跡し、記憶の定着を最適化するために戦略的にレビューをスケジュールします。
3. **インターリービング**: GrowledgePilotは学習セッション内で異なる科目やトピックを切り替えることを推奨します。これにより概念間のつながりが強化され、新しい状況への知識の転移能力が向上します。
4. **精緻化**: AIが概念を自分の言葉で説明し、既存の知識と結びつけ、例を生成するよう促します。これにより理解が深まり、批判的思考が促進されます。

## 🛠 インストール

リポジトリをクローンし、依存関係をインストールします：

git clone https://github.com/yourname/GrowledgePilot.git
cd GrowledgePilot
pip install -r requirements.txt

## 🚀 クイックスタート

メインスクリプトを実行：

python main.py

またはGradioベースのUIを起動：

python -m ui_pages.run

## 📂 プロジェクト構造

GrowledgePilot/
│── models/ # データモデル
│── ai_agents/ # AI学習エージェント
│── controllers/ # API連携とロジック制御
│── data/ # SQLiteデータベース
│── ui_pages/ # GradioベースのUI
│── utils/ # ユーティリティ関数
│── settings.py # 設定
│── logger_conf.py # ログ設定 (Loguru)
│── main.py # エントリーポイント

## 🤝 コントリビューション

コントリビューションを歓迎します！リポジトリをフォークし、PRを提出し、ディスカッションに参加してください。

## 📜 ライセンス

MITライセンスの下で公開されています。詳細は`LICENSE`をご覧ください。