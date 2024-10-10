from .base_tool_dialog import ToolDialog

class DeptWorkDialog(ToolDialog):
    def __init__(self, parent=None):
        super().__init__("Sampana", ["Anarana sampana"], parent)
        self.btnImport.setVisible(False)