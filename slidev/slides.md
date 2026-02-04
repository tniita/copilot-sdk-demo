---
theme: ./github-copilot
background: '#0d1117'
title: MCPは"使う側"で決まる
info: |
  ## MCPクライアントにフォーカスした20分セッション
  GitHub Copilot SDKで作るMCPクライアント
class: text-center
drawings:
  persist: false
transition: slide-left
mdc: true
duration: 20min
---

# MCP は<span class="copilot-gradient-text">"使う側"</span>で決まる!?

## MCP サーバは理解したけど...クライアントは...??

<div class="mt-8 text-gray-400">
Oracle Cloud Hangout Cafe Season 11 #1 Lightning Talk
</div>


---
layout: intro
---

# 自己紹介

<div class="grid grid-cols-5 gap-8 h-full items-center">
  <div class="col-span-2 flex items-center">
    <div class="text-left space-y-6">
      <h2 class="text-4xl font-bold">Takuya Niita</h2>
      <p class="text-xl text-gray-400">Solution Engineer / 某クラウドベンダー</p>
      <div class="mt-6 flex gap-6">
        <a href="https://github.com/tniita" target="_blank" class="text-gray-400 hover:text-blue-400 transition-colors">
          <carbon-logo-github class="text-4xl" />
        </a>
        <a href="https://twitter.com/takuya_0301" target="_blank" class="text-gray-400 hover:text-blue-400 transition-colors">
          <carbon-logo-twitter class="text-4xl" />
        </a>
      </div>
    </div>
  </div>
  <div class="col-span-3 flex items-center justify-center">
```json

{
  "profile": {
    "name": "仁井田 拓也",
    "name_en": "Takuya Niita",
    "title": "Solution Engineer",
    "summary": "昨年まで日本オラクルに所属しており、今は某クラウドベンダーに在籍",
    "contact": {
      "x": "takuya_0301",
      "github": "tniita"
    }
  },
  "skills": {
    "languages": ["Java", "Node.js", "Python", "Go"],
    "tools": ["K8s", "Docker", "VS Code"]
  },
  "vibe": "Ghibli"
}

```
  </div>
</div>

---
---

# 🎬 いつも<span class="text-yellow-400">??</span>のジブリネタ

<div class="flex gap-10 mt-6 items-center">
  <div class="flex-1">
    <img src="../mimi043.jpg" alt="Whisper of the Heart" class="rounded-2xl shadow-2xl" style="border: 2px solid rgba(255,255,255,0.1);" />
  </div>
  <div class="flex-1">
    <div class="bg-slate-800/60 rounded-2xl p-6 border border-slate-700">
      <p class="text-xl text-gray-100 mb-4">「私、書いてみて分かったんです。</p>
      <p class="text-xl">
        <span class="text-pink-400 font-bold">MCP サーバだけじゃダメ</span><span class="text-gray-400">なんだってこと!!</span>
      </p>
      <p class="text-xl mt-2">
        <span class="text-blue-400 font-bold">クライアントも実装しなきゃダメ</span><span class="text-gray-400">だって...!!」</span>
      </p>
    </div>
  </div>
</div>

---
class: text-center
---

# 約半年前にこんなセッションをやっていました

##### https://speakerdeck.com/oracle4engineer/llm-extension-deep-dive

<img src="../llm.png" alt="LLM Deep Dive" style="width: 85%; margin: 0 auto;" />


---
class: text-center
---


# 今日のアジェンダ

<div class="grid grid-cols-2 gap-4 mt-8">

<div class="copilot-card">
  <div class="text-blue-400 text-xl mb-2">①</div>
  <div class="text-xl font-bold">MCP の前提整理</div>
</div>

<div class="copilot-card">
  <div class="text-purple-400 text-xl mb-2">②</div>
  <div class="text-xl font-bold">MCP クライアントの本質</div>
</div>

<div class="copilot-card">
  <div class="text-pink-400 text-xl mb-2">③</div>
  <div class="text-xl font-bold">GitHub Copilot SDK</div>
</div>

<div class="copilot-card">
  <div class="text-green-400 text-xl mb-2">④</div>
  <div class="text-xl font-bold">まとめ</div>
</div>

</div>

---
layout: cover
class: text-center
---

# MCPの前提整理

---

# MCPとは？

<div class="grid grid-cols-3 gap-6 mt-8">

<div class="text-center">
  <div class="i-carbon-application text-6xl text-blue-400 mx-auto mb-4"></div>
  <div class="text-xl font-bold">MCP Host</div>
  <div class="text-gray-400 text-sm">Claude Desktop / VS Code等</div>
</div>

<div class="text-center">
  <div class="i-carbon-connect text-6xl text-purple-400 mx-auto mb-4"></div>
  <div class="text-xl font-bold">MCP Client</div>
  <div class="text-gray-400 text-sm">ツールを利用するクライアント</div>
</div>

<div class="text-center">
  <div class="i-carbon-server-proxy text-6xl text-pink-400 mx-auto mb-4"></div>
  <div class="text-xl font-bold">MCP Server</div>
  <div class="text-gray-400 text-sm">ツール提供</div>
</div>

</div>

<div class="mt-12 text-center text-xl">
  <span class="text-gray-400">MCP = </span>
  <span class="copilot-gradient-text font-bold">MCP クライアント ↔ MCP サーバ間のプロトコル</span>
</div>

---

# MCPサーバの例

<div class="grid grid-cols-3 gap-8 mt-8">

<div class="copilot-card text-center">
  <div class="i-carbon-api text-5xl text-blue-400 mx-auto mb-4"></div>
  <div class="font-bold">API</div>
</div>

<div class="copilot-card text-center">
  <div class="i-carbon-data-base text-5xl text-purple-400 mx-auto mb-4"></div>
  <div class="font-bold">DB / Search</div>
</div>

<div class="copilot-card text-center">
  <div class="i-carbon-enterprise text-5xl text-pink-400 mx-auto mb-4"></div>
  <div class="font-bold">社内ツール</div>
</div>

</div>

<v-click>

<div class="mt-12 p-6 border-2 border-yellow-500 rounded-xl text-center">
  <div class="text-2xl font-bold text-yellow-400">
    🎯 今日話したいことは「サーバ」じゃない
  </div>
</div>

</v-click>

---

# 既存のMCPクライアント

<div class="grid grid-cols-3 gap-6 mt-8">

<div class="copilot-card text-center">
  <div class="i-carbon-chat text-5xl text-blue-400 mx-auto mb-4"></div>
  <div class="font-bold">Claude Desktop</div>
</div>

<div class="copilot-card text-center">
  <div class="i-carbon-code text-5xl text-purple-400 mx-auto mb-4"></div>
  <div class="font-bold">VS Code</div>
  <div class="text-gray-400 text-sm mt-2">(GitHub Copilot)</div>
</div>

<div class="copilot-card text-center">
  <div class="i-carbon-terminal text-5xl text-pink-400 mx-auto mb-4"></div>
  <div class="font-bold">Cursor / Windsurf</div>
</div>

</div>

<v-click>

<div class="mt-8 p-6 bg-orange-900/20 border border-orange-500/50 rounded-xl">
  <div class="text-xl text-orange-400 font-bold mb-2">⚠️ しかし...</div>
  <div class="text-lg text-gray-300">
    MCPクライアントは<strong>MCP ホストに隠蔽</strong>されている<br>
    → <span class="text-orange-400">自由度・カスタマイズ性がない</span>
  </div>
</div>

</v-click>

---
class: text-center
---

# 実は・・・

<div class="mt-16">
  <div class="text-5xl font-bold leading-relaxed">
    MCP の価値は<br>
    <span class="copilot-gradient-text">"クライアント"</span>で決まるのでは...??
  </div>
</div>

---
layout: cover
class: text-center
---

# なぜ MCP クライアントが重要か

---

# よくある誤解

<div class="mt-8 space-y-8">

<div class="flex items-center gap-4">
  <div class="text-4xl">❌</div>
  <div class="text-2xl">MCP サーバを書きまくろう</div>
</div>

<div class="flex items-center gap-4">
  <div class="text-4xl">❌</div>
  <div class="text-2xl">ツールを増やせば賢くなる</div>
</div>

</div>

<v-click>

<div class="mt-12 p-6 bg-red-900/20 border border-red-500/50 rounded-xl">
  <div class="text-xl text-red-400">
    ツールが増えても、<strong>使い方が雑なら</strong>価値は出ない
  </div>
</div>

</v-click>

---

# 現実

<div class="mt-8">

<div class="copilot-card mb-6">
  <div class="text-xl">MCP サーバは...</div>
  <div class="text-2xl font-bold mt-2 text-blue-400">誰かが作る / 既にある</div>
</div>

<v-click>

<div class="text-xl mb-4">差別化ポイントは：</div>

<div class="grid grid-cols-3 gap-4">

<div class="copilot-card text-center">
  <div class="text-3xl mb-2">🎯</div>
  <div class="font-bold">いつ呼ぶか</div>
</div>

<div class="copilot-card text-center">
  <div class="text-3xl mb-2">🧠</div>
  <div class="font-bold">結果をどう解釈するか</div>
</div>

<div class="copilot-card text-center">
  <div class="text-3xl mb-2">📦</div>
  <div class="font-bold">何を LLM に渡すか</div>
</div>


</div>

</v-click>

</div>

---
layout: cover
class: text-center
---

## 自由でカスタマイズ性がある（エコシステムが充実した） MCP クライアントはないのか・・・

---
layout: cover
class: text-center
---

![alt text](../image.png)

## https://github.com/github/copilot-sdk

---

# 何がうれしい??

<div class="mt-8 text-2xl space-y-6">

- 膨大な MCP サーバが返す結果を GitHub Copilot の力を借りて解釈する...!!
- GitHub Copilot CLI や VS Code 拡張機能でできないことを実装できる...!!
- 自分だけの MCP ホストが作れるのでは...!?

</div>

<v-click>

<div class="mt-8 p-6 copilot-border">
  <div class="text-3xl">
    <carbon-idea class="text-yellow-400 inline" /> 
    GitHub Copilot SDK は<strong class="text-blue-400"> MCP クライアント(厳密には MCP ホスト?)を作るための最良のツール(かもしれない)</strong>
  </div>
</div>

</v-click>

---
layout: cover
class: text-center
---

# デモ

---
layout: cover
class: text-center
---

# まとめ

<div class="mt-12 space-y-8">

<div class="text-3xl">
  <span class="text-gray-400">MCP は</span><span class="text-blue-400 font-bold">クライアントも重要</span>
</div>

<div class="text-3xl">
  <span class="text-gray-400">MCP クライアントによる</span><span class="text-purple-400 font-bold">DX(Developer eXperience)</span><span class="text-gray-400">の改善</span>
</div>

<div class="text-3xl">
  <span class="text-gray-400">GitHub Copilot SDK はその</span><span class="text-pink-400 font-bold">最短ルート</span>
</div>

</div>

---
layout: cover
class: text-center
---

<div class="space-y-8">

<h1 class="text-4xl font-bold leading-relaxed">
  <span class="copilot-gradient-text">GitHub Copilot SDK</span> を使って
</h1>

<div class="text-5xl font-bold">
  <span class="text-yellow-400">"ぼくがかんがえたさいきょうの</span><br/>
  <span class="text-yellow-400">MCP クライアント"</span>
</div>

<h1 class="text-4xl font-bold">
  を作りましょう...!! <span class="text-6xl">🚀</span>
</h1>

</div>

---
class: text-center
---

# 📦 今日のデモ

<div class="mt-8 flex justify-center">
  <div class="bg-slate-800/80 rounded-2xl p-8 border border-slate-600 shadow-2xl" style="min-width: 600px;">
    <div class="flex items-center justify-center gap-3 mb-5">
      <carbon-logo-github class="text-5xl text-white" />
      <span class="text-2xl font-bold text-white">GitHub Repository</span>
    </div>
    <a href="https://github.com/tniita/copilot-sdk-demo" target="_blank" class="block">
      <div class="bg-slate-900 rounded-lg p-5 border border-slate-700 hover:border-blue-500 transition-all">
        <p class="text-xl text-blue-400 font-mono">
          github.com/tniita/copilot-sdk-demo
        </p>
      </div>
    </a>
  </div>
</div>

<div class="mt-6 text-base text-gray-500">
  ご清聴ありがとうございました 🙏
</div>

