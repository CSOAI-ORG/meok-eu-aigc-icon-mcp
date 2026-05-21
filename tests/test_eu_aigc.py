"""Smoke tests for meok-eu-aigc-icon-mcp."""
import sys, os, inspect, traceback
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import (
    emit_icon_manifest_entry,
    emit_html_meta_tags,
    emit_image_icc_signal,
    emit_audio_id3_signal,
    emit_video_keyframe_signal,
    get_icon_asset_uri,
    code_of_practice_status,
    sign_compliance_attestation,
    CODE_OF_PRACTICE,
)


def test_emit_icon_manifest_entry():
    r = emit_icon_manifest_entry("image")
    assert r["assertion"]["label"] == "eu.aigc.icon.v1"
    assert r["c2pa_label"] == "eu.aigc.icon.v1"
    assert "icon_uri" in r


def test_emit_icon_manifest_unsupported():
    r = emit_icon_manifest_entry("smell")
    assert "error" in r


def test_emit_html_meta_tags():
    r = emit_html_meta_tags(model_id="claude-opus-4.7")
    assert any('name="generator"' in t for t in r["meta_tags"])
    assert any("aigc:model" in t for t in r["meta_tags"])


def test_emit_image_icc_signal():
    r = emit_image_icc_signal("a" * 64, "model-x")
    assert r["icc_tag"] == "eu.aigc"
    assert r["payload"]["image_hash"] == "a" * 64


def test_emit_audio_id3_signal():
    r = emit_audio_id3_signal("h" * 64, "model-y")
    labels = [f["description"] for f in r["id3_frames"]]
    assert "AIGC-Spec" in labels
    assert "AIGC-Model" in labels


def test_emit_video_keyframe_signal():
    r = emit_video_keyframe_signal("v" * 64, "model-z")
    assert r["keyframe_box"]["uuid"] == "EUAIGC-ICON-2026-01"


def test_get_icon_asset_uri_returns_canonical():
    r = get_icon_asset_uri()
    assert "icon_uri" in r
    assert "EU AI Act Article 50" in r["visible_label"]


def test_code_of_practice_status():
    r = code_of_practice_status()
    assert "days_until_effective" in r
    assert r["effective_date"] == "2026-11-02"


def test_sign_compliance_attestation():
    r = sign_compliance_attestation({"content_hash": "abc"})
    assert r["attestation_id"].startswith("EUAIGC_")
    assert "signature" in r


if __name__ == "__main__":
    g = dict(globals())
    fns = [v for k, v in g.items() if k.startswith("test_") and inspect.isfunction(v)]
    p = f = 0
    for fn in fns:
        try:
            fn(); print(f"OK {fn.__name__}"); p += 1
        except Exception as e:
            print(f"X  {fn.__name__}: {type(e).__name__}: {e}"); traceback.print_exc(); f += 1
    print(f"\n{p} passed, {f} failed")
