# Rebeca Elmudesi Asset Editor

Claude Code plugin for Rebeca Elmudesi — self-service website and brand asset editing via asset-broker

## Prerequisites

- Claude Code v2.1.49+
- Node.js 18+, Python 3.11+ with [uv](https://docs.astral.sh/uv/)
- GitHub access to this repo (`gh auth login`)

## Installation

Via marketplace:
```bash
/plugin marketplace add stromy-org/rebecaelmudesi-marketplace
/plugin install rebeca-elmudesi
```

For local development:
```bash
git clone https://github.com/stromy-org/rebeca-elmudesi.git
cd rebeca-elmudesi
npm install
uv sync
claude --plugin-dir .
```

## Skills

Skills are split between MCP-hosted stubs (fetched at runtime via
`ReadMcpResourceTool`) and locally-authored skills (frontmatter `_local: true`).
See `skills/README.md` for the maintenance workflow. Maintaining this plugin is
an operator task driven by the `plugin-maintain` skill in stromy-org
(`/plugin-maintain`) — it is not shipped in this plugin.

## Updating

```bash
/plugin update rebeca-elmudesi
```

## License

See [LICENSE](LICENSE) for terms.
