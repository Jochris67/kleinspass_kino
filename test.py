class A:
    def process(self): print("A")

class B(A):
    def process(self):
        print("B")
        super().process()

class C(A):
    def process(self):
        print("C")
        super().process()

class D(B, C):
    def process(self):
        print("D")
        super().process()
class E(D):
    def process(self):
        print("E")
        super().process()
    
D().process()
print("++++++++")
E().process()