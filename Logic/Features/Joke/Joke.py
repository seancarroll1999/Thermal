''' 
<SUMMARY>
    -   Handles printing for Jokes 
</SUMMARY>
'''
class Joke:
    def __init__(self, setup, punchline):
        self.setup = setup
        self.punchline = punchline
    
    def print(self):
        print(self.setup)
        print(self.punchline)
    