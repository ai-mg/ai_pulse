# Claude Code: From Context Engineering to Autonomous Agents

**A 15-Minute Practitioner's Guide**
*March 2026 — Manu's AI Knowledge-Sharing Group*

---

## Agenda

1. Context Engineering — The New Paradigm
2. Claude Code Basics — Setup & Core Workflow
3. Skills 2.0 — From Markdown to Programmable Agents
4. `/loop` — Autonomous Cron-Style Loops
5. Persistent Memory Systems
6. Running Permission-Free in Containers
7. History, Orchestration & the Ecosystem
8. Key Takeaways

---

## 1. Context Engineering: The New Paradigm

### Why "Context Engineering" > "Prompt Engineering"

The era of crafting perfect single prompts is over. With models now supporting **200K–1M token context windows**, the bottleneck is no longer *what you ask* — it's **what context the model has when it reasons**.

> **Context Engineering** = Designing your *entire workflow* around managing what information the AI sees at each step.

This concept was formalized by **Dex Horthy (HumanLayer)** in his *Advanced Context Engineering for Coding Agents (ACE-FCA)* guide, which introduced **Frequent Intentional Compaction (FIC)**.

### The FIC Methodology (HumanLayer)

**Core idea:** Keep context window utilization at **40–60%** for optimal reasoning quality. Don't fill the window.

**The Research → Plan → Implement workflow:**

| Phase | What Happens | Context Strategy |
|-------|-------------|-----------------|
| **Research** | Agent explores codebase, reads files, gathers info | Produces a `research.md` artifact (~200 lines) |
| **Plan** | Human + agent turn research into phased plan | Produces `plan.md` — reviewed by human |
| **Implement** | Fresh session loads only `plan.md` + code | Plan consumes ~15–20% of window (vs. 60–80% raw) |

**Why this works:** Each phase *compacts* the previous phase's context into a distilled artifact. The implementation agent never sees the messy research — only the clean plan.

**Real-world proof:** An amateur Rust developer fixed a bug in a 300K LOC Rust codebase (BAML) in ~1 hour using this workflow. A 35K LOC feature took 7 hours (3h research/planning, 4h implementation).

### The CLAUDE.md Controversy (ETH Zurich, Feb 2026)

**The research (arXiv:2602.11988 — AGENTbench):**

- Tested 4 agents across 138 real-world Python tasks
- **LLM-generated context files** (from `/init`) → **decreased** success rates, increased costs ~20%
- **Human-written context files** → ~4% improvement on AGENTbench
- **Plot twist:** Claude Code was the *only* agent where even human-written files didn't help vs. no file at all

**What this means for practice:**

- ❌ Don't just run `/init` and forget — auto-generated CLAUDE.md is often noise
- ❌ Don't overload CLAUDE.md with everything — long files burn tokens and dilute signal
- ✅ Keep CLAUDE.md **short**: build commands, non-obvious conventions, critical constraints
- ✅ Only include things the agent **cannot infer** from the code itself
- ✅ Structure with critical rules in the **first 20 lines** (highest impact zone)
- ✅ Use **skills** (loaded on-demand) instead of stuffing everything into CLAUDE.md

### Don't Over-Constrain Advanced Models

Modern models like Opus 4.6 and Sonnet 4.6 are remarkably capable when given appropriate context. Over-constraining them with rigid step-by-step instructions can actually reduce quality. Let them reason — guide, don't micromanage.

---

## 2. Claude Code Basics

### Installation & Setup

```bash
# Install Claude Code CLI
npm install -g @anthropic-ai/claude-code

# Navigate to project and start
cd /your/project
claude

# Or use VS Code extension: search "Claude Code" by Anthropic
```

### Models

| Model | Strength | Use Case |
|-------|----------|----------|
| **Haiku** | Fast, lightweight | Quick queries, simple tasks |
| **Sonnet** | Balanced | Day-to-day development |
| **Opus** | Deep reasoning | Complex architecture, debugging |

Switch models: type `/model` in session. Set default in `settings.json`.

### Core Commands

| Command | What It Does |
|---------|-------------|
| `/init` | Scans project, creates initial CLAUDE.md (use cautiously — see above) |
| `/model` | Switch models mid-session |
| `/compact` | Manually compress context to free up window |
| `/clear` | Reset session completely |
| `/context` | Check context usage and loaded skills |
| `/btw` | Quick question in overlay — doesn't consume context |
| `Esc` | Stop Claude mid-action |
| `Esc + Esc` | Open `/rewind` to selectively compact |
| `!` prefix | Run bash commands directly |

### The CLAUDE.md File (Best Practices)

Think of it as a **README for the AI**. Lives at project root, loaded every session.

```markdown
# CLAUDE.md

## Build & Test
- `npm run build` to compile
- `npm test` runs Vitest suite

## Architecture
- Monorepo: packages/frontend, packages/api
- API uses repository pattern with Drizzle ORM

## Conventions
- TypeScript strict mode, no `any`
- Conventional commits (feat:, fix:, chore:)
- All PRs need passing CI before merge
```

**Hierarchy:** `~/.claude/CLAUDE.md` (global) → `project/CLAUDE.md` (project-level) → subdirectory CLAUDE.md files (scoped)

---

## 3. Skills 2.0: From Markdown to Programmable Agents

### The Evolution

| Era | What Skills Were | Limitation |
|-----|-----------------|------------|
| **v1 (2025)** | Markdown files in `.claude/commands/` | Static instructions, no isolation |
| **v2 (2026)** | Unified skills + commands, YAML frontmatter | Full programmable agent platform |

### What Skills Can Do Now

- **Spawn isolated subagents** with their own context windows
- **Dynamic context injection** — shell commands run *before* Claude sees the prompt
- **Tool restrictions** — limit which tools a skill can use
- **Model override** — use a different model for specific skills
- **Lifecycle hooks** — hook into events
- **Forked contexts** — run in isolated context without polluting main session

### Skill Structure

```
.claude/skills/my-skill/
├── SKILL.md          # Main instructions (required)
├── templates/        # Templates for Claude to fill
├── examples/         # Example outputs
└── scripts/          # Executable scripts
```

**SKILL.md anatomy:**

```yaml
---
name: pr-summary
description: Summarize changes in a pull request
context: fork              # Runs in isolated context
agent: Explore             # Use Explore subagent
allowed-tools: Bash(gh *)  # Only allow GitHub CLI
---

## Pull request context
- PR diff: !`gh pr diff`          # ← Shell runs BEFORE Claude sees this
- PR comments: !`gh pr view --comments`
- Changed files: !`gh pr diff --name-only`

## Your task
Summarize this pull request...
```

The `!backtick` syntax is **preprocessing** — real data replaces placeholders before Claude processes the skill.

### Notable Skills & Plugins to Install

| Plugin | What It Does |
|--------|-------------|
| **Superpowers** | Full SDLC framework: brainstorming, TDD, debugging, subagent-driven dev with code review. The gold standard. |
| **Code Review** | 5 parallel review agents (CLAUDE.md compliance, bug detection, git history, PR comments, code comments). Scores issues 0–100, only flags >80. |
| **Simplify** | Code clarity agent — simplifies recently modified code while preserving functionality |
| **Serena** | Semantic code analysis via LSP — intelligent refactoring, navigation, code understanding |
| **Claude-Mem** | Long-term memory across sessions using SQLite + Chroma vector embeddings |
| **Claude-MD-Management** | Tools to audit, maintain, and keep CLAUDE.md files current |

**Install via Claude plugin marketplace** or manually clone into `.claude/skills/`.

### Bundled Skills (Ship with Claude Code)

Four built-in skills including one that **decomposes large changes and spawns parallel agents in separate git worktrees** — this is production-grade multi-agent out of the box.

---

## 4. `/loop` — Autonomous Cron-Style Loops

The `/loop` command creates **native autonomous loops** that run for hours.

### What It Does

You describe a recurring task in **plain English** — Claude converts it to cron scheduling behind the scenes.

### Use Cases

| Scenario | What `/loop` Does |
|----------|------------------|
| **Deployment monitoring** | Polls deployment status, notifies when finished |
| **PR watcher** | Detects CI failures, auto-fixes them |
| **Test suite monitoring** | Checks long-running tests every 30 minutes |
| **Daily summaries** | Generates daily Slack summary via MCP |

### How to Use

```
/loop Monitor the deployment at staging.myapp.com 
      and notify me when it's complete.
      Check every 5 minutes.

/loop Watch PR #42 — if CI fails, analyze the logs
      and push a fix automatically

/loop Every morning at 9am, summarize yesterday's 
      GitHub activity and post to #engineering Slack
```

**Key insight:** This moves Claude Code from a *reactive* tool to a **proactive autonomous agent**. Combined with MCP servers (GitHub, Slack, etc.), loops become lightweight CI/CD agents.

---

## 5. Persistent Memory Systems

### The Problem

Claude Code has **no memory between sessions**. Every new conversation starts from zero (except CLAUDE.md).

### Memory Hierarchy

| Layer | Mechanism | Persistence |
|-------|-----------|-------------|
| **Session** | Conversation context window | Current session only |
| **CLAUDE.md** | Loaded every session | Until you edit the file |
| **Skills** | Loaded on demand | Always available |
| **External Memory** | Plugins / MCP servers | Across sessions |

### Memory Solutions

**Local options:**

| Tool | Approach | Local? |
|------|----------|--------|
| **QMD** | Structured checkpoints, flush-on-demand | ✅ Yes |
| **Claude-Mem** | SQLite + Chroma hybrid search, vector embeddings | ✅ Yes |
| **Obsidian** (via MCP) | Knowledge graph in your vault | ✅ Yes |
| **Cognee** | Knowledge graph memory layer | ✅ Self-hosted |

**Cloud-based (not fully local):**

| Tool | Approach | Local? |
|------|----------|--------|
| **Mem0** | Universal memory layer for AI agents. API + open-source self-hosted option. Graph + vector memory. | ⚠️ Cloud API or self-hosted |

### Memory Contract Pattern

To avoid the "agent ignoring decisions" problem, enforce a **memory contract**:

1. **Force search before action** — agent must check memory before starting work
2. **Force persist after decisions** — agent must write decisions to memory after agreement
3. **Checkpoint on phase transitions** — flush working-set at each workflow phase

This prevents the common failure where agents "forget" constraints mid-workflow.

---

## 6. Running Permission-Free in Containers

### The Problem

Claude Code asks permission for every file write and command execution. For autonomous work, you need `--dangerously-skip-permissions` — but that's risky on your host machine.

### Solution: Docker Containers

Run Claude Code inside an **isolated container** where it can have full permissions safely.

**Option A: Official Anthropic DevContainer**

```bash
# Clone Anthropic's reference devcontainer
# Open project in VS Code → "Reopen in Container"
# Inside container:
claude --dangerously-skip-permissions
```

Features: firewall with domain allowlist, isolated filesystem, non-root user.

**Option B: code-container (kevinMEH)**

```bash
git clone https://github.com/kevinMEH/code-container.git
cd code-container && ./install.sh

# From any project:
cd /your/project
container           # Enter container
# Inside: run Claude Code with full permissions
```

Features: persistent state across sessions, per-project isolation, simultaneous host+container work.

**Option C: Docker Sandboxes (Docker Official)**

MicroVM-based isolation with network allowlists. Supports Claude Code, Codex, Gemini CLI, Kiro.

**Option D: claudebox (RchGrav)**

```bash
claudebox --dangerously-skip-permissions
```

Per-project Docker images, development profiles (Python, Rust, Go, etc.), persistent configs.

### Key Principle

> **Container isolation is what makes `--dangerously-skip-permissions` safe.**
> The agent can only touch files in mounted volumes. Your host system is protected.

---

## 7. History, Orchestration & Ecosystem

### History Viewer (CCHV)

**Claude Code History Viewer** — a Tauri-based desktop app for browsing conversation history. Completely offline.

```bash
# Install via Homebrew
brew tap jhlee0409/tap
brew install --cask claude-code-history-viewer

# Or as a headless server
brew install jhlee0409/tap/cchv-server
cchv-server --serve  # → http://localhost:3727
```

**Features:** Unified viewer for Claude Code + Codex CLI + OpenCode, full-text search, token usage analytics, activity timeline, cost tracking.

### Agent Orchestrator (Composio)

Manages **fleets of parallel AI coding agents**. Each gets its own git worktree, branch, and PR.

```bash
git clone https://github.com/ComposioHQ/agent-orchestrator.git
cd agent-orchestrator && bash scripts/setup.sh

# One command to start
ao start https://github.com/your-org/your-repo

# Manage agents
ao spawn <project> [issue]    # Spawn an agent
ao send <session> "Fix tests" # Send instructions
ao status                     # Overview of all sessions
ao dashboard                  # Web UI at localhost:3000
```

**Reactive automation:** CI fails → agent fixes. Reviewer requests changes → agent addresses. PR approved + green CI → you get notified.

Agent-agnostic (Claude Code, Codex, Aider), runtime-agnostic (tmux, Docker).

### Awesome Lists — Your Starting Point

| Resource | What's Inside |
|----------|---------------|
| **[awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills)** | 713+ skills in universal SKILL.md format across all major agents |
| **[awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents)** | Subagent patterns, orchestration skills |
| **[awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)** | Curated skills, hooks, commands, plugins, and orchestrators |
| **[claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice)** | 8.7K★ repo with best practices, RPI workflow, tips |
| **[awesome-skills.com](https://awesome-skills.com/)** | Web directory — 125+ curated skills & plugins with categories |

---

## 8. Key Takeaways

### The Mental Model Shift

```
OLD:  Write prompt → Get code → Fix → Repeat
NEW:  Engineer context → Research → Plan → Implement → Compound
```

### Rules of Thumb

1. **Context is everything.** Keep context window at 40–60% utilization. Use subagents to offload exploration.

2. **CLAUDE.md: Less is more.** Only what the agent can't infer. No auto-generated bloat. Critical rules in first 20 lines.

3. **Skills > CLAUDE.md for instructions.** Skills load on-demand and don't burn your context window permanently.

4. **Containers for autonomy.** Never run `--dangerously-skip-permissions` on bare metal. Use Docker.

5. **Memory is your responsibility.** The agent forgets everything between sessions. Engineer persistence with checkpoints, memory plugins, or structured artifacts.

6. **Multi-agent for parallelism.** Use Agent Teams or orchestrators when tasks are truly independent. Single sessions for sequential work.

7. **Don't over-constrain.** Modern models reason better with guidance than with rigid step-by-step scripts.

---

## Quick Reference Card

| Need | Solution |
|------|----------|
| Start a project | `claude` → refine CLAUDE.md manually (skip `/init` bloat) |
| Check context usage | `/context` |
| Free up context | `/compact` or `Esc+Esc` → selective compact |
| Quick question | `/btw` (doesn't consume context) |
| Recurring task | `/loop` with plain English scheduling |
| Code review | Install **Code Review** plugin → `/code-review` |
| Parallel agents | Enable `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` |
| Browse history | Install CCHV → `brew install --cask claude-code-history-viewer` |
| Permission-free runs | Docker container + `--dangerously-skip-permissions` |
| Long-term memory | Claude-Mem plugin or QMD checkpoints |

---

## Resources

- **ACE-FCA Guide:** https://github.com/humanlayer/advanced-context-engineering-for-coding-agents
- **CLAUDE.md Research (ETH Zurich):** arXiv:2602.11988
- **Claude Code Docs:** https://code.claude.com/docs
- **Best Practices:** https://code.claude.com/docs/en/best-practices
- **Skills Docs:** https://code.claude.com/docs/en/skills
- **Plugin Marketplace:** https://claude.com/plugins
- **Agent Teams:** https://code.claude.com/docs/en/agent-teams
- **Claude Code Best Practice Repo:** https://github.com/shanraisshan/claude-code-best-practice
- **Awesome Claude Code:** https://github.com/hesreallyhim/awesome-claude-code

---

*Prepared for the AI Knowledge-Sharing Group — March 2026*
