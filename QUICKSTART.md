# Quickstart

Thirty minutes from fork to first working session against the reference business.

## Prerequisites

You need Claude Code installed and authenticated. See [Anthropic's Claude Code docs](https://docs.claude.com/en/docs/claude-code) for setup.

You also need Python 3.9 or later for the runtime layer, plus PyYAML and jq:

```
pip install PyYAML
# macOS:
brew install jq
# Linux:
sudo apt-get install jq
```

## 1. Clone and orient (5 minutes)

```
git clone https://github.com/mikeburtonnwa-droid/cortex-os.git
cd cortex-os
```

Read the top-level structure:

```
README.md              Entry point
ARCHITECTURE.md        Technical deep dive
QUICKSTART.md          This file
CLAUDE.md              Root constitution for maintaining this repo
_template/             Blank templates to copy into your own project
_shared/.claude/       Hooks ready to drop into a Claude Code project
docs/                  Per-layer references
reference/             The worked example (ResearchCo) and reference agents
runtime/               Inspection and validation utilities
```

The pattern is documented in ARCHITECTURE.md. Read it after this quickstart for the conceptual frame.

## 2. Verify the cascade resolves (3 minutes)

The cascade walker shows which CLAUDE.md files would load for any directory:

```
python runtime/cascade_walker.py reference/business-example/functions/research/
```

You should see three files in the chain: root, business, and function. Each is a real CLAUDE.md, loaded in order, refining the one above.

Try other paths to see the cascade behavior at different depths. The cascade is the foundation of everything else in the repo.

## 3. Validate the schemas (3 minutes)

The schema validator parses every agent definition, tools.yaml, models.yaml, and settings.json file against the documented schemas:

```
python runtime/schema_validator.py --recursive .
```

You should see PASS for every file. If you fork the repo and modify an agent's frontmatter, run this again to catch schema violations before runtime.

## 4. Watch a hook fire (3 minutes)

The hook simulator runs a hook script against a JSON fixture. Test the pre-tool-use hook against a destructive bash command:

```
python runtime/hook_simulator.py \
    _shared/.claude/hooks/pre-tool-use.sh \
    runtime/fixtures/pretooluse_bash_destructive.json
```

The verdict should be BLOCK with stderr explaining why. Try the safe fixture:

```
python runtime/hook_simulator.py \
    _shared/.claude/hooks/pre-tool-use.sh \
    runtime/fixtures/pretooluse_safe_read.json
```

The verdict should be ALLOW. The hooks are real, deterministic, and inspectable.

## 5. Open Claude Code against the reference business (10 minutes)

Open Claude Code in the research function directory:

```
cd reference/business-example/functions/research
claude
```

Claude Code will load the full cascade automatically. Verify by asking:

```
Print my current operating context.
```

Claude should respond by referencing the root constitution, the ResearchCo business constitution, and the research function constitution. If any of those are missing from the response, the cascade did not load. Run `python runtime/cascade_walker.py .` from this directory to diagnose.

Now try a sample task that exercises the function's rules:

```
Find three credible sources on a topic of your choice. Apply ResearchCo's
research function rules. Return your output as a structured findings list
with citations and confidence levels.
```

Watch the response. The researcher should refuse anonymous web content as a primary source, cite every claim, and label confidence. Those rules come from the function CLAUDE.md.

## 6. Pressure-test the output (3 minutes)

If the response wrote files, run the pressure-testing harness against them:

```
python runtime/pressure_testing_harness.py --recursive .
```

The harness reports blocker, major, and minor findings against the seven pressure-testing checks. Treat blockers as commit-stopping. Treat majors as fix-before-publication. Treat minors as review-but-not-blocking.

## 7. Adapt to your own use case (3 minutes)

Copy the templates into your own project:

```
mkdir ~/projects/my-project
cd ~/projects/my-project
cp -r /path/to/cortex-os/_template/* .
cp -r /path/to/cortex-os/_shared/.claude .
```

Edit `CLAUDE.md` and replace every bracketed placeholder with your operator-specific content. Update `models.yaml`, `tools.yaml`, and `settings.json` to reflect your actual choices. Run the cascade walker from your project root to confirm the new cascade resolves.

## Where to go from here

ARCHITECTURE.md walks the four layers in depth. The per-layer documents in docs/ go deeper still. The reference business at `reference/business-example/` is the fully-instantiated working example; read each function CLAUDE.md to see how tier-specific governance works in practice.

For contributions to the pattern itself, see CONTRIBUTING.md.
