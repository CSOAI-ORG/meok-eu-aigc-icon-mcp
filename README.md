# MEOK EU AIGC Icon MCP

> ## 🧱 Part of the MEOK Governance Substrate (£499/mo)
> See [meok.ai/article-50-kit](https://meok.ai/article-50-kit).

# EU AI Act Article 50 + Code of Practice AIGC icon emitter

<!-- mcp-name: io.github.CSOAI-ORG/meok-eu-aigc-icon-mcp -->

[![PyPI](https://img.shields.io/pypi/v/meok-eu-aigc-icon-mcp)](https://pypi.org/project/meok-eu-aigc-icon-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## What this does

The EU AI Act Code of Practice 2nd draft (Jan 2026) introduced a specific **EU icon + label spec** for AI-generated content. From **2 Nov 2026** (post-Omnibus), GenAI outputs into the EU market must carry this icon in both human-visible AND machine-readable form across the asset's lifecycle.

This MCP emits the icon manifest entry in the format each content type needs:

- **C2PA 2.2 assertion** — `eu.aigc.icon.v1`
- **HTML meta + link tags** — `<meta name="generator" content="ai">` + AIGC variants
- **Image ICC private tag** — `eu.aigc` JSON payload
- **Audio ID3v2 frames** — `TXXX` user-defined frames
- **Video keyframe box** — ISO BMFF `uuid` box

No other MCP is currently shipping this. First-mover.

## Tools

| Tool | Purpose |
|---|---|
| `emit_icon_manifest_entry(content_type, provider_did)` | C2PA 2.2 assertion |
| `emit_html_meta_tags(provider_did, model_id?)` | HTML head block |
| `emit_image_icc_signal(image_hash, model_id?)` | ICC private tag |
| `emit_audio_id3_signal(audio_hash, model_id?)` | ID3v2 frames |
| `emit_video_keyframe_signal(video_hash, model_id?)` | Key-frame uuid box |
| `get_icon_asset_uri()` | Canonical icon URI |
| `code_of_practice_status()` | Days until 2 Nov 2026 |
| `sign_compliance_attestation(content_meta)` | HMAC-signed Article 50 attestation |

## Sister MCPs

- `agent-content-watermark-mcp` — dedicated Article 50(2) watermark
- `watermarking-authenticity-mcp` — broader C2PA + Article 50 + Article 73 dispatch
- `eu-ai-act-compliance-mcp` — Article 50 text + thresholds
- `agent-incident-relay-mcp` — missing-icon incident broadcaster

Full catalogue: [meok.ai/anthropic-registry](https://meok.ai/anthropic-registry)

## Pricing

| Option | Price |
|---|---|
| Self-host MIT | £0 |
| Universal PAYG | £29/mo + £0.0002/call |
| Governance Substrate | £499/mo |
| A2A Substrate | £999/mo |
| Defence | £4,990/mo |

Buy: https://meok.ai/governance

## Sources

- [EU Code of Practice 2nd draft (Jan 2026)](https://digital-strategy.ec.europa.eu/en/library/commission-publishes-second-draft-code-practice-marking-and-labelling-ai-generated-content)
- [C2PA 2.2 spec](https://spec.c2pa.org/specifications/specifications/2.2/specs/C2PA_Specification.html)
- [EU AI Act Article 50](https://artificialintelligenceact.eu/article/50/)

## Licence

MIT. By [MEOK AI Labs](https://meok.ai) (CSOAI LTD, UK Companies House 16939677).
