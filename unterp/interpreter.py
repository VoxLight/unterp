import sys
import io

class Interpreter:
    def __init__(self):
        self.namespace = {}

    def execute_code(self, code):
        old_stdout = sys.stdout
        sys.stdout = mystdout = io.StringIO()
        output = []

        try:
            statements = code.split(';')
            for stmt in statements:
                stmt = stmt.strip()
                if not stmt:
                    continue

                try:
                    result = eval(stmt, self.namespace)
                    if result is not None:
                        self.namespace['_'] = result
                        output.append(str(result))
                except SyntaxError:
                    exec(stmt, self.namespace)
                except Exception as e:
                    output.append(str(e))

        except Exception as e:
            output.append(str(e))

        sys.stdout = old_stdout
        return '\n'.join(output) + '\n' + mystdout.getvalue()

interpreter = Interpreter()
