from backend.operations.math_operation import MathOperation


class DisplayOperation(MathOperation):

    def __init__(self, text: str) -> None:
        super().__init__()
        self.text = text

    def parse(self) -> None:
        pass  # As no parsing is required.

    def process(self) -> None:
        pass  # As no processing is required.

    def render(self) -> None:
        self._render(self.text)

    def print(self) -> None:
        self.pretty_res = f"Input: `{self.text}`"
