"""Figures scientifiques calculées uniquement depuis les résultats sauvegardés."""
import argparse
import json
from pathlib import Path


def plot(root, output):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    root, output = Path(root), Path(output)
    output.mkdir(parents=True, exist_ok=True)
    names = ["random", "base", "lora_easy", "lora_easy_h0", "lora_mixed", "oracle"]
    labels = ["Aléatoire*", "Qwen initial", "LoRA simple", "LoRA sans historique", "LoRA mixte", "Oracle*"]
    fig, axes = plt.subplots(1, 2, figsize=(13, 5), sharey=True, layout="constrained")
    found = False
    for ax, level in zip(axes, ["easy", "advanced"]):
        for i, (name, label) in enumerate(zip(names, labels)):
            path = root / f"{name}_{level}" / "summary.json"
            if not path.exists():
                continue
            summary = json.loads(path.read_text())
            if not summary.get("complete"):
                continue
            found = True
            m = summary["metrics"]
            p = m["success_rate"]
            low, high = m["success_ci95"]
            ax.bar(i, 100*p, color="#198c84" if name.startswith("lora") else "#72869a")
            ax.errorbar(i, 100*p, yerr=[[max(0,100*(p-low))], [max(0,100*(high-p))]],
                        fmt="none", ecolor="#172b40", capsize=4)
            ax.annotate(f"{m['successes']}/{m['n_games']}", (i, 100*high+1),
                        ha="center", fontsize=9)
        ax.set(title="Quêtes simples" if level == "easy" else "Quêtes avancées", ylim=(0, 112))
        ax.set_xticks(range(len(names)), labels, rotation=30, ha="right")
        ax.spines[["top", "right"]].set_visible(False)
    axes[0].set_ylabel("Quêtes gagnées (%) ; IC de Wilson à 95 %")
    fig.suptitle("Évaluation sur jeux non vus — * baselines avec information privilégiée")
    if not found:
        plt.close(fig)
        raise ValueError("Aucun résultat complet : aucune figure de performance produite")
    fig.savefig(output / "reussite.png", dpi=180)
    fig.savefig(output / "reussite.pdf")
    plt.close(fig)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--root", default="artifacts/eval/test")
    p.add_argument("--output", default="results/figures")
    plot(**vars(p.parse_args()))
