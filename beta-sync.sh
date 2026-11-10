#!/bin/bash
# next dalının çalışan dosyalarını main dalındaki beta/ klasörüne kopyalar (yönetici her zaman en güncel sürümü görür).
# Kullanım: ./beta-sync.sh   (next dalında, commit+push yapılmış olmalı). APP_VERSION değişmez, yalnızca beta/ klasörü güncellenir.
set -e
cd "$(dirname "$0")"
# veri parçalarını (d/) ve index.html betik bloğunu güncelle; değiştiyse next'e işle (kullanıcılar yalnız değişen parçaları indirir)
python3 tools/release/assets.py
if ! git diff --quiet -- index.html d || [ -n "$(git ls-files --others --exclude-standard d)" ]; then
  git add index.html d
  git -c user.name="${GIT_AUTHOR_NAME:-claude}" -c user.email="${GIT_AUTHOR_EMAIL:-noreply@anthropic.com}" commit -q -m "Veri parçaları güncellendi (tools/release/assets.py)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_013Jg88Frs1mRvA72RG2WGa7"
  git push -q origin HEAD:next && echo "parçalar güncellendi ve next'e gönderildi"
fi
SRC=$(git rev-parse --short HEAD)
WT=$(mktemp -d)
git fetch -q origin main
git worktree add -q --detach "$WT" FETCH_HEAD
FILES="index.html grammar.js sinav.js phrases.js words.js extr.js examples.js senses.js gloss.js reading.js reading-tr.js reading2.js reading3.js reading-fix.js exam.js mock.js supabase.js sw.js manifest.webmanifest icon-192.png icon-512.png icon-maskable-512.png apple-touch-icon.png duel-nav.svg duel-swords.svg"
mkdir -p "$WT/beta"
for f in $FILES; do [ -f "$f" ] && cp "$f" "$WT/beta/$f"; done
rm -rf "$WT/beta/d"; cp -r d "$WT/beta/d"
rm -rf "$WT/beta/audio" "$WT/beta/img"; cp -r audio "$WT/beta/audio"; [ -d img ] && cp -r img "$WT/beta/img"
sed -i "s#fetch('maintenance.json?t=#fetch('../maintenance.json?t=#" "$WT/beta/index.html"   # bakım durumu tek yerden (main) okunur
cd "$WT"
git add beta
if git diff --cached --quiet; then echo "beta zaten güncel"; else
  git -c user.name="${GIT_AUTHOR_NAME:-claude}" -c user.email="${GIT_AUTHOR_EMAIL:-noreply@anthropic.com}" commit -q -m "beta: next@$SRC (yalnızca beta/ klasörü, sürüm değişmez)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_013Jg88Frs1mRvA72RG2WGa7"
  git push -q origin HEAD:main && echo "beta güncellendi: next@$SRC"
fi
cd - >/dev/null
git worktree remove --force "$WT"
