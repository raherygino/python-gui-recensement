from .base_tool_dialog import ToolDialog

class DiaconDialog(ToolDialog):
    def __init__(self, parent=None):
        super().__init__("Diakona", ["Anarana"], parent)