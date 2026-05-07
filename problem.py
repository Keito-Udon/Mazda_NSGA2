from platypus import Problem, Integer
from pathlib import Path
import openpyxl
from evaluator import objective_function

xlsx_path = Path(__file__).parent / "Info_Mazda_CdMOBP.xlsx"

class MazdaProblem(Problem):
    def __init__(self, xlsx_path: Path = xlsx_path):
        super().__init__(222, 2, 0)
        wb = openpyxl.load_workbook(xlsx_path, read_only=True, data_only=True)
        ws = wb["Explain_DV_and_Const."]

        self._candidates = []
        for i, column in enumerate(ws.iter_rows(min_row=9, values_only=True)):
            design_variable, lower, upper, vals = column[2], column[4], column[5], column[7]
            # print(f"lower: {lower}")

            candidates = [float(v.strip()) for v in vals.split(",")]  # Discrete Volumeをリスト化
            self.types[i] = Integer(0, len(candidates) - 1)  # 候補のインデックスを整数で表現
            self._candidates.append(candidates)
            if len(self._candidates) == 222:
                break
        # self.directions[:] = [Problem.MINIMIZE, Problem.MAXIMIZE] # f1は最小化、f2は最大化
    
    def evaluate(self, solution):
        real_vars = [self._candidates[i][int(solution.variables[i])] for i in range(222)]
        f1, f2 = objective_function(real_vars)
        solution.objectives[:] = [f1, f2]