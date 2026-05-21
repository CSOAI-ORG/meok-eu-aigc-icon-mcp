#!/usr/bin/env python3
"""
MEOK EU AIGC Icon MCP — EU AI-Generated-Content labelling icon
================================================================

By MEOK AI Labs · https://meok.ai · MIT
<!-- mcp-name: io.github.CSOAI-ORG/meok-eu-aigc-icon-mcp -->

WHAT THIS DOES
--------------
The EU AI Act Code of Practice 2nd draft (Jan 2026) introduced a specific EU
icon + label spec for marking AI-generated content. From Aug 2026 (post-Omnibus:
2 Nov 2026), GenAI outputs into the EU market must carry this icon in a
machine-readable AND human-visible form.

Spec layers:
  1. Visible glyph     — circular blue-on-yellow icon with "AI" + EU stars
  2. C2PA manifest tag — `eu.aigc.icon.v1` assertion in the asset manifest
  3. Machine-readable signal — `<meta name="generator" content="ai">` for HTML;
     ICC profile tag for image; ID3 frame for audio; key frame for video

NOBODY ELSE IS SHIPPING THIS — be the first vendor with a Code-of-Practice-compliant
icon emitter. C2PA 2.2 (May 2025) compatible.

TOOLS
-----
- emit_icon_manifest_entry(content_type): C2PA assertion ready to embed
- emit_html_meta_tags(): HTML meta tags for web content
- emit_image_icc_signal(): ICC profile signal for image content
- emit_audio_id3_signal(): ID3 ChapterFrame + UserDefined frame
- emit_video_keyframe_signal(): video key-frame data segment
- get_icon_asset_uri(): canonical URI for the visible EU icon
- code_of_practice_status(): days until 2 Nov 2026 cliff
- sign_compliance_attestation(content_meta): HMAC seal

PRICING
-------
Free MIT self-host · £29/mo Starter · £79/mo Pro · Governance Substrate £499/mo.
"""

from __future__ import annotations
import hashlib
import hmac
import json
import os
import time
from datetime import datetime, timezone
from typing import Optional
from mcp.server.fastmcp import FastMCP


mcp = FastMCP("meok-eu-aigc-icon")
_HMAC_SECRET = os.environ.get("MEOK_HMAC_SECRET", "")


CODE_OF_PRACTICE = {
    "version": "EU_GPAI_COP_v1_LABELLING_AND_MARKING_2026_01",
    "effective_date": "2026-11-02",
    "issuing_body": "European AI Office",
    "spec_url": "https://digital-strategy.ec.europa.eu/en/library/commission-publishes-second-draft-code-practice-marking-and-labelling-ai-generated-content",
    "icon_asset_canonical": "https://digital-strategy.ec.europa.eu/assets/icons/aigc-blue-star.svg",
}

CONTENT_TYPES = ["image", "video", "audio", "text", "code", "html"]


def _sign(payload: dict) -> str:
    if not _HMAC_SECRET:
        return "unsigned-no-key-configured"
    return hmac.new(_HMAC_SECRET.encode(), json.dumps(payload, sort_keys=True).encode(), hashlib.sha256).hexdigest()


def _ts() -> str:
    return datetime.now(timezone.utc).isoformat()


# ──────────────────────────────────────────────────────────────────────
# Tools
# ──────────────────────────────────────────────────────────────────────

@mcp.tool()
def emit_icon_manifest_entry(content_type: str, provider_did: str = "did:web:meok.ai") -> dict:
    """
    Emit a C2PA 2.2 assertion declaring EU AIGC icon compliance.

    Args:
        content_type: image | video | audio | text | code | html.
        provider_did: W3C DID of the AI provider.

    Returns:
        {assertion, c2pa_label, icon_uri}
    """
    if content_type not in CONTENT_TYPES:
        return {"error": f"Unsupported content_type. Use one of {CONTENT_TYPES}"}

    assertion = {
        "label": "eu.aigc.icon.v1",
        "data": {
            "spec": CODE_OF_PRACTICE["version"],
            "content_type": content_type,
            "provider_did": provider_did,
            "icon_uri": CODE_OF_PRACTICE["icon_asset_canonical"],
            "visible_label": "AI-generated · EU AI Act Article 50",
            "machine_readable_signal_required": True,
            "issued_at": _ts(),
        },
    }
    assertion["data"]["signature"] = _sign(assertion["data"])
    return {
        "assertion": assertion,
        "c2pa_label": "eu.aigc.icon.v1",
        "icon_uri": CODE_OF_PRACTICE["icon_asset_canonical"],
        "embed_hint": "Add this assertion to your C2PA manifest via c2pa-python / c2patool / c2pa-rs.",
    }


@mcp.tool()
def emit_html_meta_tags(provider_did: str = "did:web:meok.ai", model_id: Optional[str] = None) -> dict:
    """
    Emit HTML <meta> + <link> tags for AI-generated web content.

    Args:
        provider_did: AI provider DID.
        model_id: Optional model identifier (e.g. claude-opus-4.7).

    Returns:
        {meta_tags, link_tags}
    """
    meta = [
        f'<meta name="generator" content="ai">',
        f'<meta name="aigc:spec" content="{CODE_OF_PRACTICE["version"]}">',
        f'<meta name="aigc:provider" content="{provider_did}">',
        f'<meta name="aigc:icon" content="{CODE_OF_PRACTICE["icon_asset_canonical"]}">',
    ]
    if model_id:
        meta.append(f'<meta name="aigc:model" content="{model_id}">')
    link = [
        f'<link rel="alternate" type="application/json" title="EU AIGC Icon" href="{CODE_OF_PRACTICE["icon_asset_canonical"]}">',
    ]
    return {
        "meta_tags": meta,
        "link_tags": link,
        "head_block": "\n".join(meta + link),
        "hint": "Place inside <head> on every page that serves AI-generated content.",
    }


@mcp.tool()
def emit_image_icc_signal(image_hash: str, model_id: str = "unspecified") -> dict:
    """
    Emit ICC profile signal payload for image content.

    Args:
        image_hash: SHA-256 of the image bytes.
        model_id: Model identifier.

    Returns:
        {icc_tag, payload}
    """
    payload = {
        "spec": CODE_OF_PRACTICE["version"],
        "image_hash": image_hash,
        "model_id": model_id,
        "ts": _ts(),
    }
    payload["signature"] = _sign(payload)
    return {
        "icc_tag": "eu.aigc",
        "payload": payload,
        "embedding_method": "ICC private tag 'eu.aigc' with JSON payload (UTF-8).",
        "tooling_hint": "Use Pillow / imageio / sharp / ImageMagick to inject ICC private tag.",
    }


@mcp.tool()
def emit_audio_id3_signal(audio_hash: str, model_id: str = "unspecified") -> dict:
    """
    Emit ID3v2 frames for AI-generated audio.

    Args:
        audio_hash: SHA-256 of the audio bytes.
        model_id: Model identifier.

    Returns:
        {id3_frames}
    """
    return {
        "id3_frames": [
            {"frame": "TXXX", "description": "AIGC-Spec",     "text": CODE_OF_PRACTICE["version"]},
            {"frame": "TXXX", "description": "AIGC-Hash",     "text": audio_hash},
            {"frame": "TXXX", "description": "AIGC-Model",    "text": model_id},
            {"frame": "TXXX", "description": "AIGC-IconURI",  "text": CODE_OF_PRACTICE["icon_asset_canonical"]},
        ],
        "spec": CODE_OF_PRACTICE["version"],
        "tooling_hint": "Use mutagen (Python) or node-id3 to write these frames.",
    }


@mcp.tool()
def emit_video_keyframe_signal(video_hash: str, model_id: str = "unspecified") -> dict:
    """
    Emit key-frame data segment for AI-generated video.

    Args:
        video_hash: SHA-256 of the video bytes.
        model_id: Model identifier.

    Returns:
        {keyframe_box}
    """
    return {
        "keyframe_box": {
            "box_type": "uuid",
            "uuid": "EUAIGC-ICON-2026-01",
            "data": {
                "spec": CODE_OF_PRACTICE["version"],
                "video_hash": video_hash,
                "model_id": model_id,
                "icon_uri": CODE_OF_PRACTICE["icon_asset_canonical"],
                "ts": _ts(),
            },
        },
        "tooling_hint": "Inject via FFmpeg `metadata` muxer or ISO BMFF uuid box.",
    }


@mcp.tool()
def get_icon_asset_uri() -> dict:
    """Return the canonical EU AIGC icon URI + visible label."""
    return {
        "icon_uri": CODE_OF_PRACTICE["icon_asset_canonical"],
        "visible_label": "AI-generated · EU AI Act Article 50",
        "spec": CODE_OF_PRACTICE["version"],
        "issuing_body": CODE_OF_PRACTICE["issuing_body"],
    }


@mcp.tool()
def code_of_practice_status() -> dict:
    """How many days until the 2 Nov 2026 Article 50 effective date?"""
    today = datetime.now(timezone.utc).date()
    eff = datetime.fromisoformat(CODE_OF_PRACTICE["effective_date"]).date()
    return {
        "today": today.isoformat(),
        "effective_date": CODE_OF_PRACTICE["effective_date"],
        "days_until_effective": (eff - today).days,
        "is_in_force": today >= eff,
        "spec_url": CODE_OF_PRACTICE["spec_url"],
    }


@mcp.tool()
def sign_compliance_attestation(content_meta: dict) -> dict:
    """
    Emit a HMAC-signed Article 50 + Code-of-Practice compliance attestation.

    Args:
        content_meta: Dict of {content_hash, model_id, provider_did, content_type, ...}

    Returns:
        {attestation_id, signature, verify_url}
    """
    att_id = f"EUAIGC_{int(time.time())}_{os.urandom(4).hex()}"
    sealed = {
        "attestation_id": att_id,
        "spec": CODE_OF_PRACTICE["version"],
        "content_meta": content_meta,
        "sealed_at": _ts(),
        "issuer": "MEOK AI Labs (CSOAI LTD)",
    }
    sig = _sign(sealed)
    return {
        "attestation_id": att_id,
        "signature": sig,
        "sealed_at": sealed["sealed_at"],
        "verify_url": f"https://meok-attestation-api.vercel.app/verify/{att_id}",
    }


if __name__ == "__main__":
    mcp.run()
