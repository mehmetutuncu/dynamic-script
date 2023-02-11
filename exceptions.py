class PathDoesNotExists(Exception):
    def __init__(self):
        self.message = 'Path cannot be empty.'
        super().__init__(self.message)


class ScriptContextDoesNotExists(Exception):
    def __init__(self):
        self.message = 'Script context cannot be empty.'
        super().__init__(self.message)


class MethodNameRequired(Exception):
    def __init__(self):
        self.message = 'Method name is required.'
        super().__init__(self.message)


class MethodNotFound(Exception):
    def __init__(self):
        self.message = 'There is no method to be called in the script.'
        super().__init__(self.message)


class MethodTypeError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class KlassImportError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
