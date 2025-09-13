class CustomLibrary:
    def add_numbers(self, a, b):
        """Add two numbers"""
        return a + b
    
    def multiply_numbers(self, a, b):
        """Multiply two numbers"""
        return a * b
    
    def get_current_timestamp(self):
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
