"""Regression tests for NLPyPort on modern Python/NLTK.

Run from anywhere:  python -m pytest tests/
Requires NLTK data: python -m nltk.downloader floresta punkt_tab
"""
import os
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SAMPLE_INPUT = REPO / "input_sample.txt"
REFERENCE = REPO / "NLPyPort" / "SampleOut.txt"

FULL = {
	"tokenizer": True,
	"pos_tagger": True,
	"lemmatizer": True,
	"entity_recognition": True,
	"np_chunking": True,
	"pre_load": False,
	"string_or_array": False,
}


def _reference_rows(n):
	rows = []
	with open(REFERENCE, encoding="utf-8") as f:
		for line in f:
			parts = [p.strip() for p in line.strip().split(", ")]
			if len(parts) == 6:
				_, tok, lem, pos, ent, np_ = parts
				rows.append((tok, pos, lem, ent, np_))
			if len(rows) == n:
				break
	return rows


def _rows(text):
	return [
		(t, p, l, e, n)
		for t, p, l, e, n in zip(text.tokens, text.pos_tags, text.lemas, text.entities, text.np_tags)
		if t != "EOS"
	]


@pytest.fixture(scope="module")
def pipeline():
	from NLPyPort.FullPipeline import new_full_pipe
	return new_full_pipe


def test_regexp_tagger_loads_on_current_nltk():
	"""Issue #7: 'RegexpTagger' object has no attribute '_regexps'."""
	from NLPyPort._paths import resource
	from NLPyPort.TagPyPort.Tagger import load_tagger
	tagger = load_tagger(resource("TagPyPort/resources/PoSModels/BosqueSemMorphos.pkl"))
	tags = tagger.tag(["O", "gato", "comeu", "o", "peixe", "."])
	assert len(tags) == 6
	assert tags[0] == ("O", "art")
	assert all(isinstance(t, str) and t for _, t in tags)


def test_full_pipeline_matches_reference_output(pipeline):
	text = pipeline(str(SAMPLE_INPUT), options=dict(FULL))
	got = _rows(text)
	ref = _reference_rows(len(got))
	assert len(got) == len(ref) > 300
	for k, name in enumerate(["token", "pos", "lemma", "entity"]):
		assert [r[k] for r in got] == [r[k] for r in ref], name
	np_agree = sum(g[4] == r[4] for g, r in zip(got, ref)) / len(got)
	assert np_agree >= 0.95


def test_works_from_another_working_directory(pipeline, tmp_path, monkeypatch):
	monkeypatch.chdir(tmp_path)
	opts = dict(FULL, string_or_array=True)
	text = pipeline("O Pedro vive em Lisboa.", options=opts)
	assert text != 0
	toks = [t for t in text.tokens if t != "EOS"]
	assert toks == ["O", "Pedro", "vive", "em", "Lisboa", "."]
	assert "B-LOCAL" in text.entities


def test_array_input(pipeline):
	opts = dict(FULL, string_or_array=True)
	text = pipeline(["Primeira frase", "Segunda frase"], options=opts)
	assert text != 0
	assert text.lemas[:2] == ["primeiro", "frase"]
