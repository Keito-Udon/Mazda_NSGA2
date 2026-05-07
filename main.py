import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from pathlib import Path
import csv
from platypus import NSGAII

# MazdaProblem
# excelから，探索範囲や設計変数の離散値候補を取得
# evaluator.pyからobject_functionライブラリとしてシミュレータ呼び出し
from problem import MazdaProblem

# ペナルティの重み
w = 1.0
# 変数74 * 車種3 -> 222次元
Dimension = 222
# 目的関数の数
Objective = 2
# 世代数100
Generation = 100
# 個体数100
Population = 100
# 制約条件54
Constraint = 54
# seed
seed = 24

# 出力先
output_dir = Path("results")

# パレート解をCSVファイルに保存
def save_pareto(solutions, output_dir):
        path = output_dir / "pareto.csv"
        with open(path, "w") as f:
            writer = csv.writer(f)
            writer.writerow(["f1_gross_weight", "f2_common_parts"])
            for s in solutions:
                writer.writerow(s.objectives) 
        print(f"パレート解を {path} に保存")

# 最終世代のパレート解を描画して保存
def save_final_pareto_plot(solutions, output_dir):
     path = output_dir / "pareto_final.png"
     fig, ax = plt.subplots(figsize=(8, 6))

     f1_vals = [s.objectives[0] for s in solutions]
     f2_vals = [-s.objectives[1] for s in solutions]
     ax.scatter(f1_vals, f2_vals, color="blue", s=40, alpha=0.8, label=f"Gen {Generation}")

     ax.set_xlabel("f1:Gross Weight")
     ax.set_ylabel("f2:Common Parts")
     ax.set_title("Final Pareto Front")
     ax.legend(loc="best", fontsize=7)
     ax.grid(True, alpha=0.3)
     fig.tight_layout()
     fig.savefig(path, dpi=150)
     plt.close(fig)
     print(f"最終世代のパレート解を {path} に保存")

#  10世代毎のパレート解を描画して保存
def save_pareto_plot(history, output_dir):
        path = output_dir / "pareto.png"
        fig, ax = plt.subplots(figsize=(8, 6))

        gens = sorted(history.keys())
        colors = cm.viridis([i / max(len(gens) - 1, 1) for i in range(len(gens))])

        for color, gen in zip(colors, gens):
            sols = history[gen]
            f1_vals = [s.objectives[0] for s in sols]
            f2_vals = [-s.objectives[1] for s in sols]  # -f2 = 共通部品数（正にする）
            ax.scatter(f1_vals, f2_vals, color=color, s=20, alpha=0.6, label=f"Gen {gen}")

        ax.set_xlabel("f1:Gross Weight")
        ax.set_ylabel("f2:Common Parts")
        ax.set_title("Pareto Front Transition")
        ax.legend(loc="best", fontsize=7, ncol=3)
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        fig.savefig(path, dpi=150)
        plt.close(fig)
        print(f"パレート解トランジションを {path} に保存")


def main():
    random.seed(seed)
    np.random.seed(seed)
    output_dir.mkdir(parents=True, exist_ok=True)

    problem = MazdaProblem()

    algorithm = NSGAII(
        problem,
        population_size=Population
    )

    max_evaluations = Population * Generation
    print(f"最適化開始：個体数={Population}, 世代数={Generation}, 最大評価回数={max_evaluations}")

    history = {}
    interval = max(1, Generation // 10)

    for g in range(1, Generation + 1):
        algorithm.step() 
        print(f"世代 {g}/{Generation} 完了")
        if g % interval == 0 or g == Generation:
            history[g] = list(algorithm.result)
    
    print("最適化完了")

    # パレート解の保存
    save_pareto(algorithm.result, output_dir)
    # 最終世代のパレート解の描画
    save_final_pareto_plot(history[Generation], output_dir)
    # 10世代毎のパレート解の描画
    save_pareto_plot(history, output_dir)

    
if __name__ == "__main__":
    main()