"""
notebook_utils.py

Objetivo del script: 
Script description goes here.

Copyright 2026 Henry Academy.
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from __future__ import annotations

import os
import random
from dataclasses import dataclass
from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np
import torch

SMOKE_ENV_VAR = "HENRY_DL_SMOKE"
ONLINE_ENV_VAR = "HENRY_DL_ONLINE_MODE"


@dataclass(frozen=True)
class RuntimeConfig:
    seed: int
    smoke: bool
    online_mode: bool
    device: torch.device

    def summary(self) -> str:
        return (
            f"seed={self.seed} | smoke={self.smoke} | "
            f"online_mode={self.online_mode} | device={self.device.type}"
        )


def is_smoke_mode() -> bool:
    return os.getenv(SMOKE_ENV_VAR, "0") == "1"


def online_mode_enabled() -> bool:
    return os.getenv(ONLINE_ENV_VAR, "0") == "1"


def detect_device() -> torch.device:
    if torch.cuda.is_available():
        return torch.device("cuda")
    mps_backend = getattr(torch.backends, "mps", None)
    if mps_backend is not None and torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


def set_seed(seed: int = 42) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def configure_runtime(seed: int = 42) -> RuntimeConfig:
    set_seed(seed)
    plt.style.use("seaborn-v0_8-whitegrid")
    plt.rcParams["figure.figsize"] = (8, 4)
    return RuntimeConfig(
        seed=seed,
        smoke=is_smoke_mode(),
        online_mode=online_mode_enabled(),
        device=detect_device(),
    )


def choose_value(standard: int | float, smoke: int | float) -> int | float:
    return smoke if is_smoke_mode() else standard


def count_parameters(model: torch.nn.Module) -> int:
    return sum(parameter.numel() for parameter in model.parameters() if parameter.requires_grad)


def plot_history(
    history: dict[str, list[float]],
    metrics: Iterable[str] = ("train_loss", "val_loss"),
    title: str = "Historia de entrenamiento",
) -> None:
    plt.figure()
    for metric in metrics:
        values = history.get(metric)
        if values:
            plt.plot(values, label=metric)
    plt.title(title)
    plt.xlabel("Epoca")
    plt.ylabel("Valor")
    plt.legend()
    plt.tight_layout()


def describe_tensor(name: str, tensor: torch.Tensor) -> str:
    return (
        f"{name}: shape={tuple(tensor.shape)}, dtype={tensor.dtype}, "
        f"device={tensor.device}, mean={tensor.float().mean():.4f}"
    )
