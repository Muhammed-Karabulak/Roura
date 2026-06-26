class Param:
    def __init__(self, param: list | tuple | set | dict | str = None):
        """Helper container to hold command parameters in various types."""
        self.params = param
        
        self.type = type(param)
                    
    def __str__(self):
        """Converts parameters into a single-line text suitable for display."""
        if self.type == list or self.type == set:
            return " ".join(map(lambda x: str(x), self.params))
        elif self.type == dict:
            return " ".join(map(lambda x: str(x), self.params.keys()))
        else:
            return None
        
    def strForLink(self):
        """Converts parameters to a format usable in URL query strings."""
        if self.type != str:
            return "+".join(self.params)
        else:
            return self.params.replace(" ", "+")            
            
    def __repr__(self):
        """Returns the raw parameter value as the object's representation."""
        return self.params if self.params else None
    
    def __getitem__(self, index):
        """Provides safe indexed access to parameter items."""
        if index < len(self.params):
            if self.type == list or self.type == dict or self.type == str:
                return self.params[index]
            else:
                return None
        return None
    
    def __getattr__(self, name):
        """Proxies string behaviors to provide convenience methods on the parameter."""
        if hasattr(str(self), name):
            return getattr(str(self), name)