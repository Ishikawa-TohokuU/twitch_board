# TwiBOX
TwiBOXのページは[こちら](http://18.178.38.84/)

## TwiBOXの概要・意義
TwiBOXは、配信プラットフォーム「 Twitch 」における配信やストリーマーを愛するユーザーの交流を目的としたコンテンツです。

TwiBOXのユーザーは、Twitchで配信されるストリームやそのアーカイブに対して自動的に生成される掲示板にコメントを投稿することができます。

Twitchでは、ユーザーは配信中にコメントを入力することができますが、終了した配信に対してコメントを残せるような機能はありません。TwiBOXでは配信中・配信終了後問わず掲示板にコメントを投稿することができるため、ユーザー同士の感想の共有が時間的要因により妨げられることがありません。

## 用いている技術
- Python3
- Django 4.1.5
- HTML + CSS
- PostgreSQL
- Amazon EC2
- Nginx
- Gunicorn

## 利用方法
ナビゲーションバーから利用したいページに移動できます。

### 配信中
その時点で実施されている配信がリアルタイムで表示されます。(通信の間隔の都合上、1~2分程度のラグは生じます)

ここでユーザーは以下の事項を確認することができます。

- 配信者名
- 配信のサムネイル
- 配信タイトル
- リアルタイムの視聴者数
- 投稿数(TwiBOXで生成された掲示板に対するコメントの総数)
- 配信開始時刻

配信サムネイルもしくは配信タイトルをクリックすることで、その配信の掲示板のページへ移動できます。掲示板のページではこれまでに投稿されたコメントの一覧を確認することができます。そして、「投稿する」のボタンから新たなコメントを投稿することができます。

### アーカイブ
既に終了した配信が表示されます。

ここでもユーザーは配信についての情報を見ることができます。

また、ページ上部にある検索欄により、

- 配信タイトル
- ストリーマー名

によるアーカイブの検索をすることができます。この機能は「配信中」のページでも同様に利用することができます。

アーカイブでは配信タイトルをクリックすることで掲示板ページに遷移することができます。

### ストリーマー
**TwiBOX側が現時点で登録している**ストリーマーの一覧が表示されます。登録するストリーマーは主に[2022年の人気ランキング](https://gamefavo.com/news/gamer/twitch-most-streamer-2022/)から選ばせて頂いております。現在は25名(2023年2月21日現在)のストリーマーが登録されていますが、今後も追加していく予定です。

このページではストリーマー名と彼らのアイコン画像を確認することができます。また、ステータスが「live」であるストリーマーのアイコン画像は紫色の枠と共に表示されますが、それをクリックすることで彼らの配信ページへ遷移することができます。

ストリーマー名をクリックすると、彼らのプロフィールページへ遷移できます。そこではストリーマー自身の、配信中の配信およびアーカイブの一覧が表示されます。そこから各掲示板へ遷移することも可能になっています。

## コンタクト
何かございましたら twibox.board@gmail.com までご連絡下さい。