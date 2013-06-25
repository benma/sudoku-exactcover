import six
from exact_cover import SparseBooleanMatrix, Node, Column 

class SudokuCell(Node):
    def __init__(self, row_number, column_number, cell_number):
        super(SudokuCell, self).__init__()
        
        self.row_number = row_number
        self.column_number = column_number
        self.cell_number = cell_number

class Sudoku(SparseBooleanMatrix):
    """
    Sudoku cast as an exact cover problem.
    See https://en.wikipedia.org/wiki/Exact_cover#Sudoku
    """
    
    def __init__(self, constraints=None):
        """
        Constraints: dictionary where key = (row_number, column_number) and value=cell_number, each value ranging from 1 to 9.
        """

        super(Sudoku, self).__init__()
        
        constraints = constraints or {}
        
        # construct sudoku matrix
        for i in six.moves.xrange(9**2 * 4):
            self.add_column(Column())
        
        columns = list(self)
        for row in range(9):    
            for col in range(9):
                box = row//3 * 3 + col//3
                for cell_number in range(9):
                    args = (row+1, col+1, cell_number+1)
                    r0, r1, r2, r3 = SudokuCell(*args), SudokuCell(*args), SudokuCell(*args), SudokuCell(*args)
                    r0.left, r0.right = r3, r1
                    r1.left, r1.right = r0, r2
                    r2.left, r2.right = r1, r3
                    r3.left, r3.right = r2, r0
                    constraint_key = (row+1, col+1)
                    if constraint_key not in constraints or constraints[constraint_key] == cell_number + 1:
                        columns[81 * 0 + row * 9 + col].add_data_object(r0)
                    else:
                        r0.remove_h()
                    
                    columns[81 * 1 + row * 9 + cell_number].add_data_object(r1)

                    columns[81 * 2 + col * 9 + cell_number].add_data_object(r2)
                    columns[81 * 3 + box * 9 + cell_number].add_data_object(r3)

    def get_solutions(self):
        for solution in self.exact_cover():
            yield dict(((cell.row_number, cell.column_number), 
                        cell.cell_number)
                       for cell in solution)

    @staticmethod
    def from_string(sudoku_string):
        numbers = six.moves.map(int, list(sudoku_string.replace('.', '0')))
        constraints = {}
        for row in range(9):
            for col in range(9):
                n = six.next(numbers)
                if n is not 0:
                    constraints.update({(row + 1, col + 1): n})
        return Sudoku(constraints)
        
def euler96():
    # euler 96
    with open('sudoku.txt', 'r') as f:
        sudoku_text = f.read()
    lines = sudoku_text.splitlines()

    sudoku_strings = [''.join(lines[i+1:i+10]) for i in six.moves.xrange(0, len(lines), 10)]

    # parsing done, solve the sudokus and sum first three digits.

    s = 0
    for s_string in sudoku_strings:
        solution = six.next(Sudoku.from_string(s_string).get_solutions())
        s += solution[(1, 1)]*100 + solution[(1, 2)] * 10 + solution[(1,3)]
    return s

def pretty(dic):
    ret = []
    for i in range(9):
        if i in (3, 6):
            ret.append('|-----------------------------|\n')
        ret.append('|')
        for j in range(9):
            if j in (3, 6):
                ret.append('|')
            ret.append(' %s ' % dic[(i+1,j+1)])
        ret.append('|')
        ret.append('\n')

    return ''.join(ret)

if __name__ == '__main__':
    # for solution in Sudoku.from_string(".......39.....1..5..3.5.8....8.9...6.7...2...1..4.......9.8..5..2....6..4..7.....").get_solutions():
    #    six.print_(pretty(solution))

    for solution in Sudoku.from_string("............56....3......12.....2...........6..7...5.8.26.........4..9......21.3.").get_solutions():
        six.print_(pretty(solution))
        break

    #print euler96()
