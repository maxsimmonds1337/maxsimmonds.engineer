---
---

# Building a Self-Maintaining Second Brain with Claude Code and Obsidian

Based on Andrej Karpathy's LLM-Wiki pattern. One evening of setup. A vault that files itself, a model that opens every session already knowing your work.

---

## The Problem

I had my best thinking scattered across five places: a notes app, 30 browser tabs, a Notion board I stopped opening, and 40 archived Claude chats I would never find again. Every project started the same way — 20 minutes rebuilding context from memory, then losing most of it by Friday.

The fix is not a better notes app. It is stopping pasting your life into a chat box and starting pointing Claude at a folder.

---

## How It Works

Three layers, three owners:

| Layer | Path | Owner |
|---|---|---|
| Sources | `raw/` | You — drop files here, never edited after |
| Wiki | `wiki/` | Claude — all compiled knowledge, Claude writes and maintains it |
| Schema | `CLAUDE.md` | Both — the rulebook |

This is not RAG (Retrieval Augmented Generation). RAG re-derives answers from raw files on every query and accumulates nothing. Here, sources are compiled once into structured, interlinked wiki pages. Knowledge compounds. The analogy: `raw/` is source code, `wiki/` is the compiled binary.

---

## The Setup

### 1. Tools

- **[Obsidian](https://obsidian.md)** — free, local-first markdown app. Opens the vault folder, renders `[[wikilinks]]` as clickable links, shows a graph of the whole knowledge network.
- **[Claude Code](https://claude.ai/download)** — the version of Claude that reads and writes files on your machine. Requires a paid plan ($20/month Claude Pro).

### 2. Folder Structure

```
second-brain/
├── CLAUDE.md          # Schema + your personal profile
├── index.md           # Navigation hub — model reads this first on every query
├── log.md             # Append-only history of ingests, queries, lints
├── raw/               # Immutable sources — you drop things here
├── wiki/              # Model-maintained compiled knowledge
└── .claude/
    └── skills/        # Obsidian-aware writing skills (kepano/obsidian-skills)
```

Create it:

```bash
mkdir -p second-brain/raw second-brain/wiki second-brain/.claude/skills
```

### 3. Install Obsidian Skills

These teach Claude to write proper Obsidian markdown — correct wikilink syntax, callouts, frontmatter — rather than generic markdown.

```bash
git clone https://github.com/kepano/obsidian-skills.git /tmp/obsidian-skills
cp -r /tmp/obsidian-skills/skills/* second-brain/.claude/skills/
```

### 4. Write Your Schema

`CLAUDE.md` at the vault root has two jobs: tell Claude the wiki rules, and tell Claude who you are. The model reads this file at the start of every session.

Key rules to include:
- Sources in `raw/` are immutable — never edited after landing
- Claude owns `wiki/` — you browse it, you don't write it by hand
- Compile, don't retrieve — answer queries by reading `index.md` and following wikilinks, not scanning `raw/` every time
- Link everything — every wiki page connects to others via `[[wikilinks]]`; the value is in the edges, not the nodes
- Lint periodically — find contradictions, orphan pages, stale claims

### 5. Open as an Obsidian Vault

Open Obsidian → Open folder as vault → pick the `second-brain/` folder. Done. Wikilinks are now clickable, backlinks panel shows what links to each page, graph view shows the whole network.

### 6. Back It Up

The wiki is plain markdown — tiny files, ideal for git. The raw sources can be large (PDFs, zips), so exclude them from git and back them up to iCloud instead.

```bash
cd second-brain
git init
echo "raw/" > .gitignore
echo ".DS_Store" >> .gitignore
git add .
git commit -m "init second brain"
```

For phone access, move the vault folder into iCloud Drive. The git repo works fine from inside iCloud Drive.

---

## The Workflow

### Ingesting a Source

Drop any file into `raw/` — PDF, article, screenshot, your own notes, a transcript. Then tell Claude:

> "Ingest `raw/filename.pdf`"

Claude reads it, writes or updates the matching wiki pages, updates `index.md`, cross-links 5–15 related pages, and appends to `log.md`. One source at a time — batch imports produce a pile, not a wiki.

**Personal notes** are first-class sources even if partially wrong. Tag them at the top:

```
<!-- source-type: personal-note | confidence-default: low -->
```

Claude will flag low-confidence claims rather than silently merging your theory with a paper's conclusion.

### Querying

> "What do I know about X?"

Claude reads `index.md`, follows relevant pages, synthesises. If the answer is novel and reusable, it files back as a new wiki page.

### Project Nodes

Projects are hub pages in `wiki/project-<slug>.md` that link to every related person, concept, tool, and decision. Other pages link back. In Obsidian's graph view this renders as a clear hub-and-spoke cluster.

The wiki tracks *what you know*, not *what you plan to do*. Plans go in a separate tool.

### Linting

> "Lint the wiki."

Claude scans for contradictions between pages, orphan pages (nothing links to them), low-confidence claims missing a flag, and entity names that drifted into two spellings. A contradiction is information — it means two sources disagree and you now know where to look.

---

## Ingesting Your Codebase

To keep the wiki aware of your projects without dumping entire codebases into `raw/`, use a digest script. It extracts only the useful signal: README, CLAUDE.md, recent git history, file structure.

```bash
#!/bin/bash
# Usage: ./digest-repo.sh <repo-path>
REPO=$1
NAME=$(basename "$REPO")
DATE=$(date +%Y-%m-%d)
OUT="raw/${DATE}_code-digest_${NAME}.md"

echo "# Repo Digest: $NAME" > "$OUT"
echo "Generated: $DATE" >> "$OUT"
echo "" >> "$OUT"

if [ -f "$REPO/README.md" ]; then
  echo "## README" >> "$OUT"
  cat "$REPO/README.md" >> "$OUT"
  echo "" >> "$OUT"
fi

if [ -f "$REPO/CLAUDE.md" ]; then
  echo "## CLAUDE.md" >> "$OUT"
  cat "$REPO/CLAUDE.md" >> "$OUT"
  echo "" >> "$OUT"
fi

echo "## Recent Activity (last 20 commits)" >> "$OUT"
git -C "$REPO" log --oneline -20 >> "$OUT"
echo "" >> "$OUT"

echo "## File Structure" >> "$OUT"
find "$REPO" -maxdepth 2 -not -path '*/.git/*' -not -path '*/node_modules/*' | \
  sed "s|$REPO/||" | sort >> "$OUT"

echo "Digest written to $OUT"
```

Run it whenever a repo changes significantly:

```bash
./digest-repo.sh ~/repos/krattworks
```

Then ingest the digest as normal. The wiki page for that project gets updated with current context.

---

## What's Still Pending

This setup works, but there are a few things left to wire in:

- **MCP + Obsidian REST API** — right now Claude accesses the vault via the filesystem directly. Wiring in the `mcp-obsidian` plugin and Local REST API would let Claude interact with Obsidian's own search index, making queries richer and faster across a large vault.

- **Automated ingestion** — a 7am scheduled Claude Code task that scans `raw/` for new files, ingests them, runs a lint pass, and writes an overnight summary to `log.md`. Currently ingestion is manual (you tell Claude to do it). The schedule tab in Claude Code makes this hands-free.

- **Local LLM** — the whole system runs on Claude Pro ($20/month). Swapping in a local model (Ollama + a capable open-weights model) would make it free to run and fully air-gapped. The vault is plain markdown so it's model-agnostic — point a different model at the folder and it works. Quality of wiki maintenance will vary by model.

- **Local backups** — the wiki is currently backed up to iCloud. A self-hosted git server (Gitea on a Raspberry Pi or home server) would give full version history, no cloud dependency, and a browsable web interface on the local network. Raw sources stay in iCloud; compiled wiki goes to the local server.

---

## What You End Up With

Run it for a week and it is a notes app. Run it for a month and it is a reference system. Run it for six months and it is a knowledge engine no amount of Googling replaces — because every new note connects to everything already there.

Same Claude subscription. A completely different machine.
