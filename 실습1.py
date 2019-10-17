def pyramid(f) :
    if f < 1 : 
        return print("floors should be greater than zero")
    else:
        floor=0
        def build(floor):
            floor+=1
            def B(n,floor):
                if floor==1:
                    return 1
                else:
                    return B(n,floor-1)+2
    
            def S(n,floor):
                if floor==1:
                    return n-1
                else:
                    return S(n,floor-1)-1
            blocks=B(f,floor)
            spaces=S(f,floor)
            print("{}{}{}".format("□"*spaces, '■'*blocks, "□"*spaces))
           
        while floor<f:
            build(floor)
        
for i in range(3,18,2):
    pyramid(i)
    print()
