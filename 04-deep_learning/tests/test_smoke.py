from __future__ import annotations

from pathlib import Path

import torch
from transformers import AutoConfig

from tools.execute_notebooks import notebook_paths
from tools.text_corpus import corpus_files, corpus_stats


def test_torch_and_transformers_minimal_usage() -> None:
    layer = torch.nn.Linear(4, 2)
    batch = torch.randn(3, 4)
    output = layer(batch)
    config = AutoConfig.for_model("bert")
    assert output.shape == (3, 2)
    assert config.hidden_size > 0


def test_module_assets_exist() -> None:
    module_root = Path(__file__).resolve().parents[1]
    expected = [
        "01_fundamentos_redes_neuronales/01_anns_desde_cero.ipynb",
        "02_pytorch_fundamentos/01_pytorch_pipeline_entrenamiento.ipynb",
        "03_entrenamiento_redes_profundas/01_estabilidad_y_regularizacion.ipynb",
        "04_vision_por_computadora_cnns/01_cnns_y_reconocimiento_visual.ipynb",
        "05_modelado_de_secuencias/01_rnns_lstm_gru_y_cnns_temporales.ipynb",
        "06_nlp_con_atencion/01_nlp_con_atencion_las_mil_y_una_noches.ipynb",
        "07_transformers_y_chatbots/01_transformers_y_chat_local.ipynb",
        "tools/execute_notebooks.py",
        "tools/text_corpus.py",
    ]
    for relative_path in expected:
        assert (module_root / relative_path).exists(), relative_path


def test_corpus_exists_and_has_content() -> None:
    stats = corpus_stats()
    assert len(corpus_files()) >= 5
    assert stats["documents"] >= 5
    assert stats["tokens"] >= 1000
    assert stats["chunks"] >= 10


def test_notebook_groups_cover_all_assets() -> None:
    all_paths = notebook_paths("all")
    assert len(all_paths) == 7
    assert notebook_paths("nlp")[0].name == "01_nlp_con_atencion_las_mil_y_una_noches.ipynb"
    assert notebook_paths("transformers")[0].name == "01_transformers_y_chat_local.ipynb"
