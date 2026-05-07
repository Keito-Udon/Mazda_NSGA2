from pathlib import Path
import subprocess

project_root = Path(__file__).parent
work_dir = project_root / "sample"
exe_path = project_root / "bin" / "win64" / "mazda_mop.exe"
# sim_path = project_root / "sample" / "run.bat"
vars_file = work_dir / "pop_vars_eval.txt"
objs_file = work_dir / "pop_objs_eval.txt"
cons_file = work_dir / "pop_cons_eval.txt"

# ペナルティの重み
weight = 1.0
# 変数74 * 車種3 -> 222次元
Dimension = 222
# 目的関数の数
Objective = 2
# 世代数100
Generation = 100
# 個体数100
Population = 300
# 制約条件54
Constraint = 54

def objective_function(vars):
    with open(vars_file, "w") as w:
        for i in range(Dimension):
            w.write(str(vars[i]))
            w.write('\t')

    # シミュレータ実行
    # subprocess.call(str(sim_path), shell=True)
    subprocess.run(
        [str(exe_path), str(work_dir)],
        cwd=project_root,
        check=True,
    )

    # 評価結果の読み込み
    with open(objs_file, "r") as r:
        objs = r.read()
        data_objs = objs.split("\t")
        f1 = float(data_objs[0])
        f2 = float(data_objs[1])
    
    # 制約違反の読み込み
    count = 0
    with open(cons_file, "r") as r:
        cons = r.read()
        data_cons = cons.split("\t")
        for i in range(Constraint):
            if float(data_cons[i]) < 0:
                count += 1
    
    f1 += float(count * weight)
    f2 += float(count * weight)

    return f1, f2