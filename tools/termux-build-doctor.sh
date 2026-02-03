#!/usr/bin/env bash
set -e

echo "🩺 termux-build doctor"
echo "======================"

ok()   { echo "✔ $1"; }
warn() { echo "⚠ $1"; }
fail() { echo "❌ $1"; }

command -v pkg      &>/dev/null && ok "pkg available"      || fail "pkg not found"
command -v dpkg-deb &>/dev/null && ok "dpkg-deb available" || warn "dpkg-deb missing"
command -v curl     &>/dev/null && ok "curl available"     || fail "curl missing"
command -v git      &>/dev/null && ok "git available"      || warn "git missing"

echo
echo "Architecture : $(uname -m)"
echo "PREFIX       : ${PREFIX:-/data/data/com.termux/files/usr}"

echo
echo "Doctor check finished (no changes made)."
